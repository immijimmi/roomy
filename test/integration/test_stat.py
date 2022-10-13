from roomy.stats import GenericStat


class TestStat:
    def test_can_model_equation_with_stats(self):
        # Setup
        work_done = GenericStat(base_value=1.5, secondary_value=2, secondary_summed_factor=3)  # 1.5 + (2 * 3) = 7.5
        velocity = GenericStat(base_value=3, secondary_summed_factor=3)  # 3 + (0 * 3) = 3
        acceleration = GenericStat(base_multiplied_factor=1.5, secondary_value=2, secondary_summed_factor=2.5)  # (0 * 1.5) + (2 * 2.5) = 5
        distance_travelled = GenericStat(1, 2, 2, 2, 1.5, 1, 3, 0.5)  # ((1 * 2 * 2) + (2 * 1.5 * 1)) * 3 * 0.5 = 10.5

        # Modelling an equation to find momentum
        force = work_done / distance_travelled  # 7.5 / 10.5 = 0.71...
        mass = force / acceleration  # 0.71... / 5 = 0.14...
        momentum = mass * velocity  # 0.14... * 3 = 0.43...

        assert round(momentum.total, 2) == 0.43

        work_done.overall_multiplied_factor *= 2  # work_done *2 -> force *2 -> mass *2 -> momentum *2
        assert round(momentum.total, 2) == 0.86
