from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LongTrack400m:
    """Simplified ISU-style long track model.

    Geometry (conceptual):
    - Total lap distance fixed to 400m.
    - Two curves of 100m each.
    - Two straights of 100m each.
    - One crossover straight; skaters switch lanes once per lap.
    """

    lap_distance_m: float = 400.0
    lane_width_m: float = 4.0

    def lap_segments(self) -> tuple[float, float, float, float]:
        """Return two curves + two straights."""
        return (100.0, 100.0, 100.0, 100.0)

    def crossover_points(self, total_distance_m: float) -> list[float]:
        """Return lane switch distances: one crossover per 400m lap.

        For simplicity we place crossover at the end of each lap distance marker,
        excluding the final finish marker.
        """
        switches = []
        marker = self.lap_distance_m
        while marker < total_distance_m:
            switches.append(float(marker))
            marker += self.lap_distance_m
        return switches
