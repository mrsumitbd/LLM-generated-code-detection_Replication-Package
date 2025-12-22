import os
import json
from typing import Any, Dict, List, Optional
from src.utils.image import encode_image

def process_single_directory(basedir: str, episode_dir: str, load_image: bool) -> Optional[Dict[str, Any]]:
    if episode_dir.startswith(".DS_Store"):
        return None
    raw_traj: Dict[str, Any] = {"episode_id": episode_dir}
    task_name_path = os.path.join(basedir, episode_dir, "task_name.json")
    try:
        with open(task_name_path, encoding="utf-8-sig") as f:
            content = f.read().strip()
            if not content:
                return None
            taskname = json.loads(content)["task_name"]
            raw_traj["task_name"] = taskname
    except Exception:
        return None

    metadata_path = os.path.join(basedir, episode_dir, "metadata.json")
    try:
        with open(metadata_path, encoding="utf-8-sig") as f:
            metadata = json.load(f)
            raw_traj["metadata"] = metadata
    except Exception:
        return None

    vis_events_path = os.path.join(basedir, episode_dir, "reduced_events_vis.jsonl")
    complete_events_path = os.path.join(basedir, episode_dir, "reduced_events_complete.jsonl")

    try:
        video_name = [f for f in os.listdir(os.path.join(basedir, episode_dir)) if f.endswith(".mp4")][0]
        video_path = os.path.join(basedir, episode_dir, video_name)
    except Exception:
        return None

    try:
        events: List[Dict[str, Any]] = []
        with open(complete_events_path, encoding="utf-8-sig") as f:
            complete_events = [json.loads(line) for line in f if line.strip()]

        with open(vis_events_path, encoding="utf-8-sig") as f:
            num_lines = sum(1 for _ in f)
            if num_lines != len(complete_events):
                return None

        last_time_stamp = None
        with open(vis_events_path, encoding="utf-8-sig") as f:
            for index, line in enumerate(f):
                if not line.strip():
                    continue
                event = json.loads(line)
                if event["description"] != complete_events[index]["description"]:
                    event["description"] = complete_events[index]["description"]
                if "\n" in event["description"]:
                    event["description"] = event["description"].split("\n")[0]
                if (
                    "click" in complete_events[index]["action"].lower()
                    or "mouse_press" in complete_events[index]["action"].lower()
                    or "click" in complete_events[index]["description"].lower()
                ) and "(" not in event["description"]:
                    event["description"] = (
                        event["description"]
                        + f" ({complete_events[index]['coordinate']['x']}, {complete_events[index]['coordinate']['y']})"
                    )
                elif "scroll" in complete_events[index]["action"].lower():
                    event["trace"] = complete_events[index]["trace"]

                video_length = get_duration(video_path)
                if complete_events[index]["action"].lower() in ["click", "mouse_press", "drag"] and "pre_move" in complete_events[index]:
                    timestamp, _ = find_loading_complete_time(
                        video_path,
                        start_time=complete_events[index]["pre_move"]["start_time"],
                        end_time=event["start_time"],
                        video_start_timestamp=raw_traj["metadata"]["video_start_timestamp"],
                    )
                else:
                    timestamp = max(0.01, event["start_time"] - raw_traj["metadata"]["video_start_timestamp"] - 0.5)

                if timestamp >= video_length:
                    timestamp = max(0.0, video_length - 0.01)

                try:
                    frame = extract_frame_at_timestamp(video_path, timestamp)
                    if frame and load_image:
                        event["frame"] = f"data:image/png;base64,{encode_image(frame)}"
                    else:
                        event["frame"] = None
                except Exception:
                    event["frame"] = None

                last_time_stamp = event["end_time"]
                event["axtree"] = None
                events.append(event)

        video_length = get_duration(video_path)
        if last_time_stamp is not None:
            if video_length + raw_traj["metadata"]["video_start_timestamp"] > last_time_stamp:
                terminate_time_stamp, _ = find_terminate_time(
                    video_path,
                    start_time=last_time_stamp,
                    end_time=video_length + raw_traj["metadata"]["video_start_timestamp"],
                    video_start_timestamp=raw_traj["metadata"]["video_start_timestamp"],
                )
            else:
                terminate_time_stamp = max(0.0, video_length - 0.01)
            try:
                terminate_frame = extract_frame_at_timestamp(video_path, terminate_time_stamp)
                terminate_event = {
                    "action": "terminate",
                    "description": "terminate the task",
                    "end_time": terminate_time_stamp,
                    "id": len(events),
                    "start_time": terminate_time_stamp,
                    "target": None,
                    "time_stamp": terminate_time_stamp,
                    "frame": f"data:image/png;base64,{encode_image(terminate_frame)}" if (terminate_frame and load_image) else None,
                    "axtree": None,
                }
                events.append(terminate_event)
            except Exception:
                pass

        raw_traj["events"] = events
        if len(events) == 0:
            return None
        return raw_traj
    except Exception:
        return None