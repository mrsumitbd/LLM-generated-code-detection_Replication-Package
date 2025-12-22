import threading
import time
import logging
from typing import Optional, Dict, List, Any
from dataclasses import dataclass, field

# Minimal placeholder types
@dataclass
class ContainerConfig:
    name: str
    labels: Dict[str, str] = field(default_factory=dict)
    monitor: bool = True

@dataclass
class MonitoredContainerContext:
    container_id: str
    config: ContainerConfig
    thread: Optional[threading.Thread] = None
    stop_event: threading.Event = field(default_factory=threading.Event)

@dataclass
class GlobalConfig:
    hosts: Dict[str, Any] = field(default_factory=dict)

class DockerLogMonitor:
    """
    Monitors Docker containers and events for a given host.

    Starts a thread for each monitored container and a thread for Docker event monitoring.
    Handles config reloads, container start/stop, and log processing.
    """

    def __init__(self, config: GlobalConfig, hostname: str, host: str):
        self.config = config
        self.hostname = hostname
        self.host = host
        self.logger = None
        self._init_logging()
        self.threads: List[threading.Thread] = []
        self.monitored_containers: Dict[str, MonitoredContainerContext] = {}
        self.event_thread: Optional[threading.Thread] = None
        self.stop_event = threading.Event()

    def _init_logging(self):
        self.logger = logging.getLogger(f"DockerLogMonitor-{self.hostname}")
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def _add_thread(self, thread: threading.Thread):
        self.threads.append(thread)
        thread.start()

    def _get_host_config(self) -> Dict[str, Any]:
        return self.config.hosts.get(self.hostname, {})

    def _get_selected_containers(self) -> List[str]:
        host_cfg = self._get_host_config()
        return host_cfg.get("containers", [])

    def _should_monitor(self, container: Dict[str, Any], skip_labels: bool = False) -> Optional[ContainerConfig]:
        labels = container.get("Labels", {})
        if skip_labels:
            return ContainerConfig(name=container["Name"], monitor=True)
        monitor = labels.get("monitor", "true").lower() == "true"
        if not monitor:
            return None
        return ContainerConfig(name=container["Name"], labels=labels, monitor=True)

    def _maybe_monitor_container(self, container: Dict[str, Any], skip_labels: bool = False) -> bool:
        cfg = self._should_monitor(container, skip_labels)
        if cfg is None:
            return False
        container_id = container["Id"]
        if container_id in self.monitored_containers:
            return False
        context = self._prepare_monitored_container_context(container, cfg)
        self._start_monitoring_thread(container, context)
        self.monitored_containers[container_id] = context
        return True

    def _prepare_monitored_container_context(self, container: Dict[str, Any], container_config: ContainerConfig) -> MonitoredContainerContext:
        return MonitoredContainerContext(
            container_id=container["Id"],
            config=container_config,
        )

    def _close_stream_connection(self, container_id: str):
        ctx = self.monitored_containers.get(container_id)
        if ctx:
            ctx.stop_event.set()

    def start(self, client) -> str:
        self.logger.info("Starting DockerLogMonitor")
        # Start container monitoring threads
        for container in client.containers.list():
            self._maybe_monitor_container(container.attrs)
        # Start event monitoring thread
        self.event_thread = threading.Thread(target=self._watch_events, daemon=True)
        self.event_thread.start()
        return self._start_message()

    def reload_config(self, config: GlobalConfig) -> str:
        self.logger.info("Reloading configuration")
        self.config = config
        # Stop all current monitoring threads
        for ctx in self.monitored_containers.values():
            ctx.stop_event.set()
        self.monitored_containers.clear()
        # Restart monitoring with new config
        # (Assumes client is available globally or passed in)
        return "Configuration reloaded"

    def _start_message(self) -> str:
        return f"Monitoring started on host {self.hostname}"

    def _handle_error(self, error_count: int, last_error_time: float, container_name: Optional[str] = None):
        self.logger.error(
            f"Error #{error_count} after {time.time() - last_error_time:.2f}s "
            f"for container {container_name}"
        )

    def _start_monitoring_thread(self, container: Dict[str, Any], container_context: MonitoredContainerContext):
        def monitor():
            self.logger.info(f"Started monitoring {container_context.config.name}")
            while not container_context.stop_event.is_set():
                # Dummy log processing
                time.sleep(1)
            self.logger.info(f"Stopped monitoring {container_context.config.name}")

        thread = threading.Thread(target=monitor, daemon=True)
        container_context.thread = thread
        self._add_thread(thread)

    def _watch_events(self):
        self.logger.info("Event watcher started")
        while not self.stop_event.is_set():
            # Dummy event loop
            time.sleep(5)
        self.logger.info("Event watcher stopped")

    def cleanup(self, timeout: float = 1.5):
        self.logger.info("Cleaning up")
        self.stop_event.set()
        for ctx in self.monitored_containers.values():
            ctx.stop_event.set()
        for thread in self.threads:
            thread.join(timeout)
        if self.event_thread:
            self.event_thread.join(timeout)
        self.logger.info("Cleanup complete")

    def tail_logs(self, unit_name: str, monitor_type: str, lines: int = 10) -> Optional[str]:
        ctx = next(
            (c for c in self.monitored_containers.values() if c.config.name == unit_name),
            None,
        )
        if not ctx:
            return None
        # Dummy log tail
        return f"Last {lines} lines of {unit_name} ({monitor_type})"

    def container_action(self, monitor_type: str, unit_name: str, action: str):
        ctx = next(
            (c for c in self.monitored_containers.values() if c.config.name == unit_name),
            None,
        )
        if not ctx:
            self.logger.warning(f"Container {unit_name} not monitored")
            return
        if action == "stop":
            ctx.stop_event.set()
            self.logger.info(f"Stopped monitoring {unit_name}")
        elif action == "start":
            if not ctx.thread or not ctx.thread.is_alive():
                self._start_monitoring_thread(ctx.config, ctx)
                self.logger.info(f"Restarted monitoring {unit_name}")
        else:
            self.logger.warning(f"Unknown action {action} for {unit_name}")