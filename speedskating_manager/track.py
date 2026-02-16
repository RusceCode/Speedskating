from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LongTrack400m:
    """Simplified ISU-style long track model.

    - Total lap distance is fixed to 400 m.
    - Two racing lanes (inner/outer).
    - Skaters cross and switch lanes on the designated crossover points.
    """

    lap_distance_m: float = 400.0
    lane_width_m: float = 4.0

    def lap_segments(self) -> tuple[float, float]:
        """Return half-lap segments where lane-switch can happen (200m + 200m)."""
        return (200.0, 200.0)

    def crossover_points(self, total_distance_m: float) -> list[float]:
        """Return all distances (in meters from start) where a lane switch occurs."""
        switches = []
        marker = 200.0
        while marker < total_distance_m:
            switches.append(marker)
            marker += 200.0
        return switches
