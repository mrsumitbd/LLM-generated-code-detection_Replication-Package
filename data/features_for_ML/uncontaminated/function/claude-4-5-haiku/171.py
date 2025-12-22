def delete_task_by_video(video_id: str, platform: str):
    """
    Delete a task associated with a specific video.
    
    Args:
        video_id: The ID of the video
        platform: The platform where the video is hosted (e.g., 'youtube', 'tiktok')
    """
    import sqlite3
    
    try:
        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()
        
        cursor.execute(
            'DELETE FROM tasks WHERE video_id = ? AND platform = ?',
            (video_id, platform)
        )
        
        conn.commit()
        conn.close()
        
        return True
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    except Exception as e:
        print(f"Error deleting task: {e}")
        return False