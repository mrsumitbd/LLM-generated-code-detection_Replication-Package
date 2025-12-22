from collections import Counter
from typing import Dict, List

class OnlineNaiveBayes:
    def __init__(self, alpha: float = 0.5, beta: float = 0.5, gamma: float = 1.0, vocab_size: int = 200000):
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.vocab_size = vocab_size
        self.class_counts = {}
        self.word_counts = {}
        self.class_log_z = {}

    def _invalidate(self, cid: str):
        if cid in self.class_log_z:
            del self.class_log_z[cid]

    def _logZ_c(self, cid: str) -> float:
        if cid not in self.class_log_z:
            self.class_log_z[cid] = sum(self.word_counts.get((cid, w), self.alpha) for w in range(self.vocab_size)) + self.class_counts[cid] * self.beta
        return self.class_log_z[cid]

    def score_batch(self, tf: Counter, cids: List[str]) -> Dict[str, float]:
        scores = {}
        for cid in cids:
            score = sum(self.word_counts.get((cid, w), self.alpha) * tf[w] for w in tf) + self.class_counts[cid] * self.gamma
            score -= self._logZ_c(cid)
            scores[cid] = score
        return scores

    def update_positive(self, tf: Counter, cid: str):
        for w, count in tf.items():
            self.word_counts[(cid, w)] = self.word_counts.get((cid, w), self.alpha) + count
        self.class_counts[cid] = self.class_counts.get(cid, 0) + 1
        self._invalidate(cid)

    def decay(self, factor: float = None):
        if factor is None:
            factor = self.gamma
        self.word_counts = {k: v * factor for k, v in self.word_counts.items()}
        self.class_counts = {k: v * factor for k, v in self.class_counts.items()}
        self.class_log_z = {k: v * factor for k, v in self.class_log_z.items()}