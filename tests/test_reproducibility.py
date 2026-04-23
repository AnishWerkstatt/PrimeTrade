import numpy as np

from src.primetrade.reproducibility import set_global_seed


def test_set_global_seed_deterministic_numpy() -> None:
    set_global_seed(42)
    a = np.random.rand(3)

    set_global_seed(42)
    b = np.random.rand(3)

    assert np.array_equal(a, b)
