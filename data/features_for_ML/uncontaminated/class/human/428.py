import asyncio
from .tools.social_media_tools import SocialMediaConfig, TwitterAPI, LinkedInAPI, InstagramAPI

class SchedulerService:
    """Background service that monitors and publishes scheduled posts"""

    def __init__(self, scheduler: SocialMediaScheduler):
        self.scheduler = scheduler
        self.running = False

    async def start(self):
        """Start the scheduler service"""
        self.running = True
        logger.info("Scheduler service started")

        while self.running:
            try:
                # Check for posts due in the next 5 minutes
                posts = self.scheduler.get_posts_due(within_minutes=5)

                for post in posts:
                    await self._publish_post(post)

                # Wait 1 minute before checking again
                await asyncio.sleep(60)

            except Exception as e:
                logger.error(f"Error in scheduler service: {e}")
                await asyncio.sleep(60)

    async def _publish_post(self, post: ScheduledPost):
        """Publish a scheduled post"""
        logger.info(f"Publishing post {post.id} to {post.platform}")

        try:
            # Here you would integrate with the actual social media APIs
            # For now, we'll simulate publishing
            from .tools.social_media_tools import SocialMediaConfig, TwitterAPI, LinkedInAPI, InstagramAPI

            config = SocialMediaConfig()

            if post.platform == "twitter":
                api = TwitterAPI(config)
                result = await api.post_tweet(post.content)
            elif post.platform == "linkedin":
                api = LinkedInAPI(config)
                result = await api.post_update(post.content)
            elif post.platform == "instagram":
                api = InstagramAPI(config)
                if post.media_urls:
                    result = await api.post_photo(post.media_urls[0], post.content)
                else:
                    raise ValueError("Instagram requires media URLs")
            else:
                raise ValueError(f"Unsupported platform: {post.platform}")

            # Update status to published
            self.scheduler.update_post_status(post.id, PostStatus.PUBLISHED)
            logger.info(f"Successfully published post {post.id}")

        except Exception as e:
            logger.error(f"Failed to publish post {post.id}: {e}")
            self.scheduler.update_post_status(post.id, PostStatus.FAILED, str(e))

    def stop(self):
        """Stop the scheduler service"""
        self.running = False
        logger.info("Scheduler service stopped")