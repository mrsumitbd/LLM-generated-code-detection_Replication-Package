from typing import List

class SEDTask:
    pass

class Problem:

    def create_task(self) -> SEDTask:
        pass

    @property
    def train_samples(self) -> List:
        pass

    @property
    def test_samples(self) -> List:
        pass

    @property
    def ood_test_samples(self) -> List:
        pass