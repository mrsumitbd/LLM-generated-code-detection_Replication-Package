class Problem:
    def __init__(self):
        self._train_samples = None
        self._test_samples = None
        self._ood_test_samples = None
        self._task = None

    def create_task(self) -> 'SEDTask':
        if self._task is None:
            self._task = SEDTask()
        return self._task

    @property
    def train_samples(self):
        if self._train_samples is None:
            self._train_samples = []
        return self._train_samples

    @property
    def test_samples(self):
        if self._test_samples is None:
            self._test_samples = []
        return self._test_samples

    @property
    def ood_test_samples(self):
        if self._ood_test_samples is None:
            self._ood_test_samples = []
        return self._ood_test_samples


class SEDTask:
    pass