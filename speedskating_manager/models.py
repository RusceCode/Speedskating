from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Distance(Enum):
    """Official long-track race distances in meters."""

    M500 = 500
    M1000 = 1000
    M1500 = 1500
    M3000 = 3000
    M5000 = 5000
    M10000 = 10000


@dataclass(slots=True)
class Skater:
    name: str
    stamina: float
    technique: float
    sprint: float
    form: float = 70.0

    def quality_score(self) -> float:
        return self.stamina * 0.38 + self.technique * 0.34 + self.sprint * 0.28 + self.form * 0.15


@dataclass(slots=True)
class Team:
    name: str
    budget: int = 500_000
    morale: float = 70.0
    facility_level: int = 1
    skaters: list[Skater] = field(default_factory=list)

    def train_week(self, focus: str) -> None:
        if self.budget < 5_000:
            return

        self.budget -= 5_000
        self.morale = min(100.0, self.morale + 1.5)

        for skater in self.skaters:
            bonus = 0.8 + (self.facility_level * 0.25)
            if focus == "stamina":
                skater.stamina = min(99.0, skater.stamina + 1.8 * bonus)
            elif focus == "technique":
                skater.technique = min(99.0, skater.technique + 1.8 * bonus)
            elif focus == "sprint":
                skater.sprint = min(99.0, skater.sprint + 1.8 * bonus)
            else:
                skater.stamina = min(99.0, skater.stamina + 0.6 * bonus)
                skater.technique = min(99.0, skater.technique + 0.6 * bonus)
                skater.sprint = min(99.0, skater.sprint + 0.6 * bonus)

    def upgrade_facility(self) -> bool:
        if self.budget < 100_000:
            return False
        self.budget -= 100_000
        self.facility_level += 1
        self.morale = min(100.0, self.morale + 4.0)
        return True
