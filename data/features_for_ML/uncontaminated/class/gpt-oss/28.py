import time
from __future__ import annotations
from typing import Any, Dict, Optional


class JaneCoreSkillStrikeCritRateBonusRecord:
    """
    A record that stores a critical‑rate bonus applied to a skill strike.
    """

    def __init__(
        self,
        skill_id: Optional[int] = None,
        crit_rate_bonus: float = 0.0,
        source: Optional[str] = None,
        timestamp: Optional[float] = None,
    ) -> None:
        """
        Parameters
        ----------
        skill_id
            Identifier of the skill to which the bonus applies.
        crit_rate_bonus
            The bonus to the critical rate (in percentage points).
        source
            Optional description of the origin of the bonus.
        timestamp
            Unix timestamp of when the record was created. If omitted,
            the current time is used.
        """
        self.skill_id = skill_id
        self.crit_rate_bonus = float(crit_rate_bonus)
        self.source = source
        self.timestamp = timestamp if timestamp is not None else time.time()

    # ------------------------------------------------------------------
    # Basic representation and comparison
    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"skill_id={self.skill_id!r}, "
            f"crit_rate_bonus={self.crit_rate_bonus!r}, "
            f"source={self.source!r}, "
            f"timestamp={self.timestamp!r})"
        )

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, JaneCoreSkillStrikeCritRateBonusRecord):
            return NotImplemented
        return (
            self.skill_id == other.skill_id
            and self.crit_rate_bonus == other.crit_rate_bonus
            and self.source == other.source
            and self.timestamp == other.timestamp
        )

    # ------------------------------------------------------------------
    # Serialization helpers
    # ------------------------------------------------------------------
    def to_dict(self) -> Dict[str, Any]:
        """Return a dictionary representation of the record."""
        return {
            "skill_id": self.skill_id,
            "crit_rate_bonus": self.crit_rate_bonus,
            "source": self.source,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "JaneCoreSkillStrikeCritRateBonusRecord":
        """Create a record from a dictionary."""
        return cls(
            skill_id=data.get("skill_id"),
            crit_rate_bonus=data.get("crit_rate_bonus", 0.0),
            source=data.get("source"),
            timestamp=data.get("timestamp"),
        )

    # ------------------------------------------------------------------
    # Functional helpers
    # ------------------------------------------------------------------
    def apply_to(self, base_crit_rate: float) -> float:
        """
        Apply the bonus to a base critical rate.

        Parameters
        ----------
        base_crit_rate
            The original critical rate (in percentage points).

        Returns
        -------
        float
            The new critical rate after adding the bonus.
        """
        return float(base_crit_rate) + self.crit_rate_bonus

    def merge(self, other: "JaneCoreSkillStrikeCritRateBonusRecord") -> "JaneCoreSkillStrikeCritRateBonusRecord":
        """
        Merge this record with another, summing the bonuses.

        Parameters
        ----------
        other
            Another record to merge with. Must have the same skill_id.

        Returns
        -------
        JaneCoreSkillStrikeCritRateBonusRecord
            A new record containing the combined bonus.

        Raises
        ------
        ValueError
            If the skill_id of the two records differs.
        """
        if self.skill_id != other.skill_id:
            raise ValueError("Cannot merge records with different skill_id values")

        combined_source = (
            f"{self.source}+{other.source}" if self.source and other.source else self.source or other.source
        )
        return JaneCoreSkillStrikeCritRateBonusRecord(
            skill_id=self.skill_id,
            crit_rate_bonus=self.crit_rate_bonus + other.crit_rate_bonus,
            source=combined_source,
            timestamp=max(self.timestamp, other.timestamp),
        )

    # ------------------------------------------------------------------
    # Validation helpers
    # ------------------------------------------------------------------
    def validate(self) -> None:
        """
        Validate the record's data.

        Raises
        ------
        ValueError
            If any field contains an invalid value.
        """
        if self.skill_id is not None and not isinstance(self.skill_id, int):
            raise ValueError("skill_id must be an integer or None")
        if not isinstance(self.crit_rate_bonus, (int, float)):
            raise ValueError("crit_rate_bonus must be numeric")
        if self.source is not None and not isinstance(self.source, str):
            raise ValueError("source must be a string or None")
        if not isinstance(self.timestamp, (int, float)):
            raise ValueError("timestamp must be numeric")