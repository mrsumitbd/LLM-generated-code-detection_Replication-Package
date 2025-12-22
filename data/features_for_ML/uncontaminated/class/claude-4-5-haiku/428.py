class SchedulerService:
    """Background service that monitors and publishes scheduled posts"""

    def __init__(self, scheduler: SocialMediaScheduler):
        self.scheduler = scheduler
        self._running = False
        self._thread = None

    def stop(self):
        self._running = False
        if self._thread is not None:
            self._thread.join()