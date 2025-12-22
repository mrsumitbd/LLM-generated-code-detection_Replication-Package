def delete_task_by_video(video_id: str, platform: str):
    import sqlite3

    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()

    c.execute("DELETE FROM tasks WHERE video_id = ? AND platform = ?", (video_id, platform))
    conn.commit()
    conn.close()