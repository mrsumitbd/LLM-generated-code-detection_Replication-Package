from typing import List
from dataclasses import dataclass

@dataclass
class SEDTask:
    train_samples: List
    test_samples: List
    ood_test_samples: List

class Problem:
    def __init__(self, train_data, test_data, ood_test_data):
        self._train_samples = train_data
        self._test_samples = test_data
        self._ood_test_samples = ood_test_data

    def create_task(self) -> SEDTask:
        return SEDTask(self._train_samples, self._test_samples, self._ood_test_samples)

    @property
    def train_samples(self):
        return self._train_samples

    @property
    def test_samples(self):
        return self._test_samples

    @property
    def ood_test_samples(self):
        return self._ood_test_samples