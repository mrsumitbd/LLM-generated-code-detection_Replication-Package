import anthropic
import json
import re


class MusicPlayer:
    def __init__(self):
        self.client = anthropic.Anthropic()
        self.playlist = []
        self.current_track_index = 0
        self.is_playing = False
        self.volume = 50

    def add_track(self, title: str, artist: str, duration: int) -> dict:
        """Add a track to the playlist."""
        track = {
            "title": title,
            "artist": artist,
            "duration": duration,
            "id": len(self.playlist) + 1
        }
        self.playlist.append(track)
        return track

    def remove_track(self, track_id: int) -> bool:
        """Remove a track from the playlist by ID."""
        for i, track in enumerate(self.playlist):
            if track["id"] == track_id:
                self.playlist.pop(i)
                if self.current_track_index >= len(self.playlist) and self.current_track_index > 0:
                    self.current_track_index -= 1
                return True
        return False

    def play(self) -> str:
        """Start playing the current track."""
        if not self.playlist:
            return "Playlist is empty"
        self.is_playing = True
        current_track = self.playlist[self.current_track_index]
        return f"Now playing: {current_track['title']} by {current_track['artist']}"

    def pause(self) -> str:
        """Pause the current track."""
        self.is_playing = False
        return "Playback paused"

    def next_track(self) -> str:
        """Skip to the next track."""
        if not self.playlist:
            return "Playlist is empty"
        self.current_track_index = (self.current_track_index + 1) % len(self.playlist)
        current_track = self.playlist[self.current_track_index]
        return f"Skipped to: {current_track['title']} by {current_track['artist']}"

    def previous_track(self) -> str:
        """Go back to the previous track."""
        if not self.playlist:
            return "Playlist is empty"
        self.current_track_index = (self.current_track_index - 1) % len(self.playlist)
        current_track = self.playlist[self.current_track_index]
        return f"Going back to: {current_track['title']} by {current_track['artist']}"

    def set_volume(self, level: int) -> str:
        """Set the volume level (0-100)."""
        if level < 0:
            self.volume = 0
        elif level > 100:
            self.volume = 100
        else:
            self.volume = level
        return f"Volume set to {self.volume}%"

    def get_current_track(self) -> dict | None:
        """Get the current track information."""
        if not self.playlist:
            return None
        return self.playlist[self.current_track_index]

    def get_playlist(self) -> list:
        """Get the entire playlist."""
        return self.playlist

    def process_command(self, command: str) -> str:
        """Process natural language commands using Claude."""
        tools = [
            {
                "name": "add_track",
                "description": "Add a new track to the playlist",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "The title of the track"},
                        "artist": {"type": "string", "description": "The artist name"},
                        "duration": {"type": "integer", "description": "Duration in seconds"}
                    },
                    "required": ["title", "artist", "duration"]
                }
            },
            {
                "name": "remove_track",
                "description": "Remove a track from the playlist by ID",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "track_id": {"type": "integer", "description": "The ID of the track to remove"}
                    },
                    "required": ["track_id"]
                }
            },
            {
                "name": "play",
                "description": "Start playing the current track",
                "input_schema": {"type": "object", "properties": {}}
            },
            {
                "name": "pause",
                "description": "Pause the current track",
                "input_schema": {"type": "object", "properties": {}}
            },
            {
                "name": "next_track",
                "description": "Skip to the next track",
                "input_schema": {"type": "object", "properties": {}}
            },
            {
                "name": "previous_track",
                "description": "Go back to the previous track",
                "input_schema": {"type": "object", "properties": {}}
            },
            {
                "name": "set_volume",
                "description": "Set the volume level",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "level": {"type": "integer", "description": "Volume level from 0 to 100"}
                    },
                    "required": ["level"]
                }
            },
            {
                "name": "get_current_track",
                "description": "Get information about the current track",
                "input_schema": {"type": "object", "properties": {}}
            },
            {
                "name": "get_playlist",
                "description": "Get the entire playlist",
                "input_schema": {"type": "object", "properties": {}}
            }
        ]

        messages = [
            {"role": "user", "content": command}
        ]

        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            tools=tools,
            messages=messages
        )

        while response.stop_reason == "tool_use":
            tool_use_block = None
            for block in response.content:
                if block.type == "tool_use":
                    tool_use_block = block
                    break

            if not tool_use_block:
                break

            tool_name = tool_use_block.name
            tool_input = tool_use_block.input

            if tool_name == "add_track":
                result = self.add_track(
                    tool_input["title"],
                    tool_input["artist"],
                    tool_input["duration"]
                )
                result_str = f"Added track: {result['title']} by {result['artist']}"
            elif tool_name == "remove_track":
                success = self.remove_track(tool_input["track_id"])
                result_str = f"Track removed successfully" if success else "Track not found"
            elif tool_name == "play":
                result_str = self.play()
            elif tool_name == "pause":
                result_str = self.pause()
            elif tool_name == "next_track":
                result_str = self.next_track()
            elif tool_name == "previous_track":
                result_str = self.previous_track()
            elif tool_name == "set_volume":
                result_str = self.set_volume(tool_input["level"])
            elif tool_name == "get_current_track":
                track = self.get_current_track()
                result_str = json.dumps(track) if track else "No track currently selected"
            elif tool_name == "get_playlist":
                result_str = json.dumps(self.get_playlist())
            else:
                result_str = f"Unknown tool: {tool_name}"

            messages.append({"role": "assistant", "content": response.content})
            messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_use_block.id,
                        "content": result_str
                    }
                ]
            })

            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                tools=tools,
                messages=messages
            )

        final_response = ""
        for block in response.content:
            if hasattr(block, "text"):
                final_response = block.text
                break

        return final_response