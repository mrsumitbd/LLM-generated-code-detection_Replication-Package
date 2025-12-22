from collections import Counter
from typing import List, Dict

class OnlineNaiveBayes:

    def __init__(self, alpha: float = 0.5, beta: float = 0.5, gamma: float = 1.0, vocab_size: int = 200000):
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.vocab_size = vocab_size
        self.class_word_counts = {}
        self.class_total_counts = {}
        self.class_doc_counts = {}
        self.total_doc_count = 0

    def _invalidate(self, cid: str):
        if cid in self.class_word_counts:
            del self.class_word_counts[cid]
            del self.class_total_counts[cid]
            del self.class_doc_counts[cid]

    def _logZ_c(self, cid: str) -> float:
        return sum(self.class_word_counts[cid].values())

    def score_batch(self, tf: Counter, cids: List[str]) -> Dict[str, float]:
        scores = {}
        for cid in cids:
            score = 0.0
            for word, count in tf.items():
                score += count * (self.class_word_counts.get(cid, {}).get(word, 0) + self.alpha) / (self.class_total_counts.get(cid, 0) + self.alpha * self.vocab_size)
            scores[cid] = score + self._logZ_c(cid)
        return scores

    def update_positive(self, tf: Counter, cid: str):
        for word, count in tf.items():
            self.class_word_counts.setdefault(cid, Counter())[word] += count
            self.class_total_counts[cid] += count
        self.class_doc_counts[cid] += 1
        self.total_doc_count += 1

    def decay(self, factor: float = None):
        if factor is None:
            factor = self.gamma
        for cid in self.class_doc_counts:
            self.class_total_counts[cid] *= factor
            self.class_doc_counts[cid] *= factor