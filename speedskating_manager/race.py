from __future__ import annotations

from dataclasses import dataclass
from random import Random

from .models import Distance, Skater
from .track import LongTrack400m


@dataclass(slots=True)
class Split:
    distance_m: float
    lane_a: str
    lane_b: str
    time_a_s: float
    time_b_s: float


@dataclass(slots=True)
class RaceResult:
    distance_m: int
    skater_a: str
    skater_b: str
    finish_a_s: float
    finish_b_s: float
    winner: str
    lane_switch_points_m: list[float]
    splits: list[Split]


def _base_pace_seconds_per_100m(skater: Skater, distance: Distance) -> float:
    """Very rough long-track pacing profile per 100m."""
    d = distance.value
    quality = skater.quality_score()

    # Lower is better pace.
    sprint_weight = 1.35 if d <= 1000 else 0.75
    stamina_weight = 1.35 if d >= 3000 else 0.85
    technique_weight = 1.0

    ability = (
        skater.sprint * sprint_weight
        + skater.stamina * stamina_weight
        + skater.technique * technique_weight
        + quality * 0.45
    )

    baseline = 13.8 - (ability / 120.0)
    return max(8.2, baseline)


def simulate_head_to_head_race(
    skater_a: Skater,
    skater_b: Skater,
    distance: Distance,
    seed: int | None = None,
) -> RaceResult:
    """Simulate a 2-skater long-track race with fixed official distance and lane switches.

    Rules represented:
    - race is always exactly two skaters
    - fixed long-track distances (Distance enum)
    - 400m oval model with lane crossovers every 200m
    """
    rng = Random(seed)
    track = LongTrack400m()
    total = distance.value

    switch_points = track.crossover_points(total)

    lane_a = "inner"
    lane_b = "outer"

    pace_a = _base_pace_seconds_per_100m(skater_a, distance)
    pace_b = _base_pace_seconds_per_100m(skater_b, distance)

    fatigue_steps = max(1, total // 400)
    fatigue_a = 0.06 * (100 - skater_a.stamina) / 100.0 / fatigue_steps
    fatigue_b = 0.06 * (100 - skater_b.stamina) / 100.0 / fatigue_steps

    time_a = 0.0
    time_b = 0.0
    splits: list[Split] = []

    covered = 0
    while covered < total:
        step = min(100, total - covered)
        variation_a = rng.uniform(-0.08, 0.08)
        variation_b = rng.uniform(-0.08, 0.08)

        lane_penalty_a = 0.04 if lane_a == "outer" else 0.0
        lane_penalty_b = 0.04 if lane_b == "outer" else 0.0

        seg_a = (pace_a + lane_penalty_a + variation_a) * (step / 100)
        seg_b = (pace_b + lane_penalty_b + variation_b) * (step / 100)

        time_a += seg_a
        time_b += seg_b

        covered += step

        if covered % 400 == 0:
            pace_a += fatigue_a
            pace_b += fatigue_b

        if covered in switch_points:
            lane_a, lane_b = lane_b, lane_a

        splits.append(
            Split(
                distance_m=float(covered),
                lane_a=lane_a,
                lane_b=lane_b,
                time_a_s=round(time_a, 3),
                time_b_s=round(time_b, 3),
            )
        )

    winner = skater_a.name if time_a <= time_b else skater_b.name

    return RaceResult(
        distance_m=total,
        skater_a=skater_a.name,
        skater_b=skater_b.name,
        finish_a_s=round(time_a, 3),
        finish_b_s=round(time_b, 3),
        winner=winner,
        lane_switch_points_m=switch_points,
        splits=splits,
    )
