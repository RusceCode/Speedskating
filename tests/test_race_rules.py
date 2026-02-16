from speedskating_manager.models import Distance, Skater
from speedskating_manager.race import simulate_head_to_head_race


def test_race_is_head_to_head_and_fixed_distance():
    a = Skater("A", stamina=80, technique=75, sprint=70)
    b = Skater("B", stamina=78, technique=76, sprint=72)

    result = simulate_head_to_head_race(a, b, Distance.M5000, seed=123)

    assert result.distance_m == 5000
    assert result.skater_a == "A"
    assert result.skater_b == "B"
    assert result.winner in {"A", "B"}


def test_lane_switching_happens_once_per_400m_lap():
    a = Skater("A", stamina=80, technique=80, sprint=80)
    b = Skater("B", stamina=80, technique=80, sprint=80)

    result = simulate_head_to_head_race(a, b, Distance.M1000, seed=1)

    assert result.lane_switch_points_m == [400.0, 800.0]


def test_distance_catalog_is_official_style_long_track_set():
    distances = {d.value for d in Distance}
    assert distances == {500, 1000, 1500, 3000, 5000, 10000}
