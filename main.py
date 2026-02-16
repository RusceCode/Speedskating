from speedskating_manager.models import Distance, Skater, Team
from speedskating_manager.race import simulate_head_to_head_race


def demo() -> None:
    team = Team(
        name="Noord IJs Pro Team",
        skaters=[
            Skater("Noa de Vries", stamina=76, technique=79, sprint=73),
            Skater("Lars Bos", stamina=81, technique=72, sprint=76),
            Skater("Mila Kuipers", stamina=70, technique=84, sprint=72),
        ],
    )

    team.train_week("technique")
    team.upgrade_facility()

    # Long-track is ridden in pairs (2 skaters), distances are fixed official values.
    result = simulate_head_to_head_race(team.skaters[0], team.skaters[1], Distance.M1500, seed=7)

    print(f"Team: {team.name}")
    print(f"Budget: €{team.budget:,}")
    print(f"Race: {result.distance_m}m | {result.skater_a} vs {result.skater_b}")
    print(f"Crossover points: {result.lane_switch_points_m}")
    print(f"Finish: {result.skater_a} {result.finish_a_s}s | {result.skater_b} {result.finish_b_s}s")
    print(f"Winner: {result.winner}")


if __name__ == "__main__":
    demo()
