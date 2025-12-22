import logging
import threading
import time
from typing import Optional

from .config import ContainerConfig, GlobalConfig
from .context import MonitoredContainerContext

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
        self._init_logging()
        self.threads = []

    def _init_logging(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def _add_thread(self, thread):
        self.threads.append(thread)
        thread.start()

    def _get_host_config(self):
        return self.config.get_host_config(self.hostname)

    def _get_selected_containers(self):
        host_config = self._get_host_config()
        return host_config.get_selected_containers()

    def _should_monitor(self, container, skip_labels=False) -> ContainerConfig | None:
        host_config = self._get_host_config()
        return host_config.should_monitor(container, skip_labels)

    def _maybe_monitor_container(self, container, skip_labels=False) -> bool:
        container_config = self._should_monitor(container, skip_labels)
        if container_config:
            container_context = self._prepare_monitored_container_context(container, container_config)
            self._start_monitoring_thread(container, container_context)
            return True
        return False

    def _prepare_monitored_container_context(self, container, container_config: ContainerConfig) -> MonitoredContainerContext:
        return MonitoredContainerContext(container, container_config)

    def _close_stream_connection(self, container_id):
        pass

    def start(self, client) -> str:
        self.logger.info("Starting Docker log monitoring...")
        selected_containers = self._get_selected_containers()
        for container in selected_containers:
            self._maybe_monitor_container(container)
        self._add_thread(threading.Thread(target=self._watch_events))
        return self._start_message()

    def reload_config(self, config: GlobalConfig) -> str:
        self.config = config
        self.cleanup()
        return self.start(None)

    def _start_message(self) -> str:
        return f"Docker log monitoring started for host: {self.hostname}"

    def _handle_error(self, error_count, last_error_time, container_name=None):
        pass

    def _start_monitoring_thread(self, container, container_context: MonitoredContainerContext):
        thread = threading.Thread(target=self._monitor_container, args=(container, container_context))
        self._add_thread(thread)

    def _watch_events(self):
        pass

    def cleanup(self, timeout=1.5):
        for thread in self.threads:
            thread.join(timeout)

    def tail_logs(self, unit_name, monitor_type, lines=10) -> Optional[str]:
        pass

    def container_action(self, monitor_type, unit_name, action):
        pass