import sqlite3
from typing import Optional

def delete_task_by_video(video_id: str, platform: str) -> Optional[int]:
    """
    Delete a task from the `tasks` table that matches the given video_id and platform.
    Returns the number of rows deleted, or None if an error occurs.
    """
    try:
        # Connect to the SQLite database (adjust path as needed)
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()

        # Perform the deletion
        cursor.execute(
            """
            DELETE FROM tasks
            WHERE video_id = ? AND platform = ?
            """,
            (video_id, platform),
        )

        # Commit changes and close connection
        conn.commit()
        deleted_rows = cursor.rowcount
    except Exception:
        deleted_rows = None
    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass

    return deleted_rows