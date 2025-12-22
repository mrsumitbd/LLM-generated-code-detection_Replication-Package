class DockerLogMonitor:
    """
    Monitors Docker containers and events for a given host.

    Starts a thread for each monitored container and a thread for Docker event monitoring.
    Handles config reloads, container start/stop, and log processing.
    """

    def __init__(self, config, hostname, host):
        self.config = config
        self.hostname = hostname
        self.host = host
        self.client = None
        self.monitored_containers = {}
        self.threads = []
        self.stop_event = threading.Event()
        self.logger = None
        self._init_logging()

    def _init_logging(self):
        self.logger = logging.getLogger(f"DockerLogMonitor-{self.hostname}")
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                f'%(asctime)s - {self.hostname} - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    def _add_thread(self, thread):
        self.threads.append(thread)
        thread.start()

    def _get_host_config(self):
        for host_config in self.config.hosts:
            if host_config.hostname == self.hostname:
                return host_config
        return None

    def _get_selected_containers(self):
        host_config = self._get_host_config()
        if not host_config:
            return []
        
        try:
            containers = self.client.containers.list(all=True)
            selected = []
            for container in containers:
                if self._maybe_monitor_container(container):
                    selected.append(container)
            return selected
        except Exception as e:
            self.logger.error(f"Error getting containers: {e}")
            return []

    def _should_monitor(self, container, skip_labels=False) -> ContainerConfig | None:
        host_config = self._get_host_config()
        if not host_config:
            return None
        
        container_name = container.name
        
        for container_config in host_config.containers:
            if container_config.name == container_name:
                if skip_labels or self._check_labels(container, container_config):
                    return container_config
        
        return None

    def _check_labels(self, container, container_config):
        if not container_config.labels:
            return True
        
        container_labels = container.labels or {}
        for label_key, label_value in container_config.labels.items():
            if container_labels.get(label_key) != label_value:
                return False
        return True

    def _maybe_monitor_container(self, container, skip_labels=False) -> bool:
        container_config = self._should_monitor(container, skip_labels)
        return container_config is not None

    def _prepare_monitored_container_context(self, container, container_config: ContainerConfig) -> MonitoredContainerContext:
        return MonitoredContainerContext(
            container_id=container.id,
            container_name=container.name,
            container_config=container_config,
            stream=None,
            error_count=0,
            last_error_time=None
        )

    def _close_stream_connection(self, container_id):
        if container_id in self.monitored_containers:
            context = self.monitored_containers[container_id]
            if context.stream:
                try:
                    context.stream.close()
                except Exception as e:
                    self.logger.debug(f"Error closing stream for {container_id}: {e}")
                context.stream = None

    def start(self, client) -> str:
        self.client = client
        self.stop_event.clear()
        
        try:
            containers = self._get_selected_containers()
            for container in containers:
                container_config = self._should_monitor(container, skip_labels=True)
                if container_config:
                    context = self._prepare_monitored_container_context(container, container_config)
                    self.monitored_containers[container.id] = context
                    self._start_monitoring_thread(container, context)
            
            event_thread = threading.Thread(target=self._watch_events, daemon=True)
            self._add_thread(event_thread)
            
            return self._start_message()
        except Exception as e:
            self.logger.error(f"Error starting monitor: {e}")
            return f"Error starting monitor: {e}"

    def reload_config(self, config: GlobalConfig) -> str:
        self.config = config
        self.stop_event.set()
        
        for container_id in list(self.monitored_containers.keys()):
            self._close_stream_connection(container_id)
        
        self.monitored_containers.clear()
        self.stop_event.clear()
        
        try:
            containers = self._get_selected_containers()
            for container in containers:
                container_config = self._should_monitor(container, skip_labels=True)
                if container_config:
                    context = self._prepare_monitored_container_context(container, container_config)
                    self.monitored_containers[container.id] = context
                    self._start_monitoring_thread(container, context)
            
            return f"Config reloaded for {self.hostname}"
        except Exception as e:
            self.logger.error(f"Error reloading config: {e}")
            return f"Error reloading config: {e}"

    def _start_message(self) -> str:
        count = len(self.monitored_containers)
        return f"Started monitoring {count} containers on {self.hostname}"

    def _handle_error(self, error_count, last_error_time, container_name=None):
        error_count += 1
        last_error_time = time.time()
        
        if error_count > 5:
            self.logger.warning(
                f"Container {container_name} has {error_count} consecutive errors"
            )
        
        return error_count, last_error_time

    def _start_monitoring_thread(self, container, container_context: MonitoredContainerContext):
        def monitor_logs():
            error_count = 0
            last_error_time = None
            
            while not self.stop_event.is_set():
                try:
                    if container_context.stream is None:
                        container_context.stream = self.client.containers.get(
                            container_context.container_id
                        ).logs(stream=True, follow=True)
                    
                    for line in container_context.stream:
                        if self.stop_event.is_set():
                            break
                        self.logger.info(f"[{container_context.container_name}] {line.decode().strip()}")
                    
                    error_count = 0
                    last_error_time = None
                    
                except Exception as e:
                    error_count, last_error_time = self._handle_error(
                        error_count, last_error_time, container_context.container_name
                    )
                    self._close_stream_connection(container_context.container_id)
                    time.sleep(min(2 ** error_count, 30))
        
        thread = threading.Thread(target=monitor_logs, daemon=True)
        self._add_thread(thread)

    def _watch_events(self):
        while not self.stop_event.is_set():
            try:
                for event in self.client.events(decode=True):
                    if self.stop_event.is_set():
                        break
                    
                    if event.get('Type') == 'container':
                        action = event.get('Action')
                        container_id = event.get('Actor', {}).get('ID')
                        
                        if action == 'start':
                            try:
                                container = self.client.containers.get(container_id)
                                if self._maybe_monitor_container(container):
                                    container_config = self._should_monitor(container, skip_labels=True)
                                    if container_config and container_id not in self.monitored_containers:
                                        context = self._prepare_monitored_container_context(container, container_config)
                                        self.monitored_containers[container_id] = context
                                        self._start_monitoring_thread(container, context)
                            except Exception as e:
                                self.logger.debug(f"Error handling container start: {e}")
                        
                        elif action == 'stop':
                            if container_id in self.monitored_containers:
                                self._close_stream_connection(container_id)
                                del self.monitored_containers[container_id]
            
            except Exception as e:
                self.logger.error(f"Error watching events: {e}")
                time.sleep(5)

    def cleanup(self, timeout=1.5):
        self.stop_event.set()
        
        for container_id in list(self.monitored_containers.keys()):
            self._close_stream_connection(container_id)
        
        for thread in self.threads:
            thread.join(timeout=timeout)
        
        self.monitored_containers.clear()
        self.threads.clear()

    def tail_logs(self, unit_name, monitor_type, lines=10) -> Optional[str]:
        try:
            for container_id, context in self.monitored_containers.items():
                if context.container_name == unit_name:
                    container = self.client.containers.get(container_id)
                    logs = container.logs(tail=lines)
                    return logs.decode()
        except Exception as e:
            self.logger.error(f"Error tailing logs: {e}")
        
        return None

    def container_action(self, monitor_type, unit_name, action):
        try:
            for container_id, context in self.monitored_containers.items():
                if context.container_name == unit_name:
                    container = self.client.containers.get(container_id)
                    if action == 'start':
                        container.start()
                    elif action == 'stop':
                        container.stop()
                    elif action == 'restart':
                        container.restart()
                    return f"Action {action} performed on {unit_name}"
        except Exception as e:
            self.logger.error(f"Error performing action: {e}")
        
        return f"Failed to perform action {action} on {unit_name}"