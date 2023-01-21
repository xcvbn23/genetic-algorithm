import random
import pytest

from main import genetic_algorithm

# Seed the random number generator
random.seed(42)


@pytest.mark.skip
def test_genetic_algorithm():
    # Test with default parameters
    best_individual, best_fitness = genetic_algorithm(
        100, 0.1, "single_point", "elitist"
    )
    assert best_individual == 12.386709845283113
    assert best_fitness == 153.43058079123358

    # Test with different crossover strategy
    best_individual, best_fitness = genetic_algorithm(100, 0.1, "two_point", "elitist")
    assert best_individual == 13.16879974938745
    assert best_fitness == 173.41728683946695

    # Test with different selection strategy
    best_individual, best_fitness = genetic_algorithm(
        100, 0.1, "single_point", "roulette_wheel"
    )
    assert best_individual == 9.592228288578983
    assert best_fitness == 92.01084354021489

    # Test with different mutation rate
    best_individual, best_fitness = genetic_algorithm(
        100, 0.2, "single_point", "elitist"
    )
    assert best_individual == 13.169982029983936
    assert best_fitness == 173.4484266700998

    # Test with invalid crossover strategy
    with pytest.raises(ValueError):
        best_individual, best_fitness = genetic_algorithm(
            100, 0.1, "invalid_strategy", "elitist"
        )

    # Test with invalid selection strategy
    with pytest.raises(ValueError):
        best_individual, best_fitness = genetic_algorithm(
            100, 0.1, "single_point", "invalid_strategy"
        )
