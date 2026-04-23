import os
import random

import numpy as np


def set_global_seed(seed: int) -> None:
    if seed < 0:
        raise ValueError("Seed must be a non-negative integer")

    random.seed(seed)
    np.random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)

    try:
        import torch  # type: ignore

        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        torch.use_deterministic_algorithms(True)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
    except Exception:
        # Torch is optional.
        pass
