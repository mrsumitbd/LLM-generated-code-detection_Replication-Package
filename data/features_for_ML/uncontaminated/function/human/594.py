def timestamp_to_seconds(timestamp):
      if not timestamp:
        return 0

      # Parse timestamp format HH:MM:SS:MS.
      parts = timestamp.split(":")
      if len(parts) != 4:
        raise ValueError("Timestamp must be in format HH:MM:SS:MS")

      hours = int(parts[0])
      minutes = int(parts[1])
      seconds = int(parts[2])
      milliseconds = int(parts[3])

      return hours * 3600 + minutes * 60 + seconds + milliseconds / 1000