"""Core simulation package for a desktop-oriented speedskating manager prototype."""

from .models import Distance, Skater, Team
from .race import RaceResult, simulate_head_to_head_race

__all__ = [
    "Distance",
    "Skater",
    "Team",
    "RaceResult",
    "simulate_head_to_head_race",
]
