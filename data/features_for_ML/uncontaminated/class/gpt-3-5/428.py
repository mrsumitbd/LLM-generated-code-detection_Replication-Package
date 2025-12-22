from typing import List

class SchedulerService:
    """Background service that monitors and publishes scheduled posts"""

    def __init__(self, scheduler: SocialMediaScheduler):
        self.scheduler = scheduler

    def stop(self):
        self.scheduler.stop_scheduling()

class SocialMediaScheduler:
    def __init__(self):
        self.scheduled_posts = []

    def schedule_post(self, post):
        self.scheduled_posts.append(post)

    def stop_scheduling(self):
        self.scheduled_posts.clear()

# Example usage
scheduler = SocialMediaScheduler()
scheduler.schedule_post("Post 1")
scheduler.schedule_post("Post 2")

service = SchedulerService(scheduler)
service.stop()

print(scheduler.scheduled_posts)  # Output: []