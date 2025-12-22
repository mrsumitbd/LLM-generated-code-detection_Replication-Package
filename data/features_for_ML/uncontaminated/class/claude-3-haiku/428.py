import threading
import time

class SchedulerService:
    """Background service that monitors and publishes scheduled posts"""

    def __init__(self, scheduler: SocialMediaScheduler):
        self.scheduler = scheduler
        self.running = True
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        while self.running:
            scheduled_posts = self.scheduler.get_scheduled_posts()
            for post in scheduled_posts:
                if post.should_publish():
                    self.scheduler.publish_post(post)
            time.sleep(60)  # Check for new scheduled posts every minute

    def stop(self):
        self.running = False
        self.thread.join()