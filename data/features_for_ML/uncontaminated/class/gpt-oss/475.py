import datetime
from typing import List, Dict, Optional, Tuple


class Schedule:
    """
    RemindType
        提醒类型 id    描述
        0   不提醒
        1   开始时提醒
        2   开始前 5 分钟提醒
        3   开始前 15 分钟提醒
        4   开始前 30 分钟提醒
        5   开始前 60 分钟提醒
    """

    REMIND_MAP: Dict[int, int] = {
        0: 0,   # 不提醒
        1: 0,   # 开始时提醒
        2: 5,   # 开始前 5 分钟提醒
        3: 15,  # 开始前 15 分钟提醒
        4: 30,  # 开始前 30 分钟提醒
        5: 60,  # 开始前 60 分钟提醒
    }

    def __init__(self) -> None:
        self._events: List[Dict] = []

    def add_event(
        self,
        name: str,
        start_time: datetime.datetime,
        remind_type: int = 0,
    ) -> None:
        """
        Add an event to the schedule.

        :param name: Name or description of the event.
        :param start_time: The datetime when the event starts.
        :param remind_type: One of the keys in REMIND_MAP.
        """
        if remind_type not in self.REMIND_MAP:
            raise ValueError(f"Invalid remind_type {remind_type}")
        if not isinstance(start_time, datetime.datetime):
            raise TypeError("start_time must be a datetime.datetime instance")
        self._events.append(
            {
                "name": name,
                "start_time": start_time,
                "remind_type": remind_type,
            }
        )

    def remove_event(self, name: str) -> bool:
        """
        Remove an event by name.

        :return: True if an event was removed, False otherwise.
        """
        for i, ev in enumerate(self._events):
            if ev["name"] == name:
                del self._events[i]
                return True
        return False

    def _reminder_time(self, event: Dict) -> datetime.datetime:
        minutes_before = self.REMIND_MAP[event["remind_type"]]
        return event["start_time"] - datetime.timedelta(minutes=minutes_before)

    def get_due_reminders(
        self, current_time: datetime.datetime
    ) -> List[Dict]:
        """
        Return a list of events that should trigger a reminder at the given
        current_time. The comparison is inclusive of the exact reminder moment
        and exclusive of the next second to avoid duplicate triggers.

        :param current_time: The current datetime to check against.
        :return: List of event dictionaries that are due.
        """
        if not isinstance(current_time, datetime.datetime):
            raise TypeError("current_time must be a datetime.datetime instance")
        due = []
        for ev in self._events:
            remind_time = self._reminder_time(ev)
            if remind_time <= current_time < remind_time + datetime.timedelta(seconds=1):
                due.append(ev)
        return due

    def next_reminder(self, current_time: datetime.datetime) -> Optional[Tuple[datetime.datetime, Dict]]:
        """
        Find the next upcoming reminder after current_time.

        :param current_time: The current datetime.
        :return: A tuple of (reminder_time, event_dict) or None if none.
        """
        if not isinstance(current_time, datetime.datetime):
            raise TypeError("current_time must be a datetime.datetime instance")
        upcoming: List[Tuple[datetime.datetime, Dict]] = []
        for ev in self._events:
            remind_time = self._reminder_time(ev)
            if remind_time > current_time:
                upcoming.append((remind_time, ev))
        if not upcoming:
            return None
        return min(upcoming, key=lambda x: x[0])

    def __repr__(self) -> str:
        return f"<Schedule events={len(self._events)}>"

    def __len__(self) -> int:
        return len(self._events)

    def __iter__(self):
        return iter(self._events)