from Networkfunction.Utility.Utilities import Whole

import numpy as np
import pytest

A = np.array([[0, 1, 0, 1, 1], [1, 0, 0, 1, 0], [0, 0, 0, 1, 1], [1, 1, 1, 0, 1], [1, 0, 1, 1, 0]])
C = np.array([[0, 0.3, 0.4, 0.5, 0.3], [0.4, 0, 0.3, 0.4, 0.5],
              [0.3, 0.2, 0, 0.4, 0.5], [0.5, 0.6, 0.4, 0, 0.7], [0.5, 0.6, 0.3, 0.7, 0]])
B = {0: 0, 1: 4, 2: 3, 3: 2, 4: 1}


def test_network_utility():

    W=Whole(A, B, C)
    assert W.wholeutility() == 67.5



