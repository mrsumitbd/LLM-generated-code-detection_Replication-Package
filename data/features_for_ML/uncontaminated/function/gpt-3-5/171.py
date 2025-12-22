def delete_task_by_video(video_id: str, platform: str):
    # Implementation to delete task by video
    if platform == 'YouTube':
        # Delete task for YouTube platform
        print(f"Deleting task for video {video_id} on YouTube platform")
    elif platform == 'Vimeo':
        # Delete task for Vimeo platform
        print(f"Deleting task for video {video_id} on Vimeo platform")
    else:
        print(f"Platform {platform} not supported")