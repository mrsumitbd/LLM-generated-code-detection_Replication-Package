from collections import Counter, defaultdict
from math import log
from typing import Dict, List


class OnlineNaiveBayes:
    """
    A simple online Naïve Bayes classifier with Laplace smoothing.
    """

    def __init__(self, alpha: float = 0.5, beta: float = 0.5, gamma: float = 1.0, vocab_size: int = 200000):
        """
        Parameters
        ----------
        alpha : float
            Laplace smoothing for word likelihoods.
        beta : float
            Laplace smoothing for class priors.
        gamma : float
            Not used in this implementation but kept for API compatibility.
        vocab_size : int
            Size of the vocabulary (used for smoothing denominator).
        """
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.vocab_size = vocab_size

        # Counts
        self.class_word_counts: Dict[str, Counter] = defaultdict(Counter)  # word -> count per class
        self.class_total_words: Dict[str, float] = defaultdict(float)      # total word count per class
        self.class_prior_counts: Dict[str, float] = defaultdict(float)     # document count per class
        self.total_docs: float = 0.0

        # Cache for log prior
        self._log_prior_cache: Dict[str, float] = {}

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _invalidate(self, cid: str):
        """Invalidate cached values for a class."""
        if cid in self._log_prior_cache:
            del self._log_prior_cache[cid]

    def _log_prior(self, cid: str) -> float:
        """Return log prior probability of class cid."""
        if cid not in self._log_prior_cache:
            num_classes = len(self.class_prior_counts)
            # Avoid division by zero
            denom = self.total_docs + self.beta * num_classes
            if denom == 0:
                log_prior = -float('inf')
            else:
                log_prior = log(self.class_prior_counts[cid] + self.beta) - log(denom)
            self._log_prior_cache[cid] = log_prior
        return self._log_prior_cache[cid]

    def _log_likelihood(self, cid: str, word: str) -> float:
        """Return log P(word | cid)."""
        word_count = self.class_word_counts[cid][word]
        denom = self.class_total_words[cid] + self.alpha * self.vocab_size
        if denom == 0:
            return -float('inf')
        return log(word_count + self.alpha) - log(denom)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def score_batch(self, tf: Counter, cids: List[str]) -> Dict[str, float]:
        """
        Compute log posterior scores for a batch of classes given a term frequency vector.

        Parameters
        ----------
        tf : Counter
            Term frequency vector of the document.
        cids : List[str]
            List of class identifiers to score.

        Returns
        -------
        Dict[str, float]
            Mapping from class id to log posterior probability (unnormalized).
        """
        scores: Dict[str, float] = {}
        for cid in cids:
            log_p = self._log_prior(cid)
            for word, freq in tf.items():
                log_p += freq * self._log_likelihood(cid, word)
            scores[cid] = log_p
        return scores

    def update_positive(self, tf: Counter, cid: str):
        """
        Update the model with a new positive example for class cid.

        Parameters
        ----------
        tf : Counter
            Term frequency vector of the new document.
        cid : str
            Class identifier of the document.
        """
        # Update class prior
        self.class_prior_counts[cid] += 1
        self.total_docs += 1

        # Update word counts
        for word, freq in tf.items():
            self.class_word_counts[cid][word] += freq
        self.class_total_words[cid] += sum(tf.values())

        # Invalidate caches
        self._invalidate(cid)

    def decay(self, factor: float = None):
        """
        Decay all counts by a factor (default 0.5). Useful for sliding window or forgetting.

        Parameters
        ----------
        factor : float, optional
            Decay factor (0 < factor <= 1). If None, defaults to 0.5.
        """
        if factor is None:
            factor = 0.5
        if not (0 < factor <= 1):
            raise ValueError("Decay factor must be in (0, 1].")

        # Decay class priors
        for cid in list(self.class_prior_counts.keys()):
            self.class_prior_counts[cid] *= factor
            if self.class_prior_counts[cid] < 1e-6:
                del self.class_prior_counts[cid]
                del self.class_word_counts[cid]
                del self.class_total_words[cid]
                self._invalidate(cid)

        # Decay word counts
        for cid, counter in self.class_word_counts.items():
            for word in list(counter.keys()):
                counter[word] *= factor
                if counter[word] < 1e-6:
                    del counter[word]
            self.class_total_words[cid] *= factor

        # Decay total docs
        self.total_docs *= factor