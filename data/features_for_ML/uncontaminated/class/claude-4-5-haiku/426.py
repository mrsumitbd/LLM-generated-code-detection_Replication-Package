class OnlineNaiveBayes:

    def __init__(self, alpha: float = 0.5, beta: float = 0.5, gamma: float = 1.0, vocab_size: int = 200000):
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.vocab_size = vocab_size
        
        self.class_counts = {}
        self.feature_counts = {}
        self.logZ_cache = {}

    def _invalidate(self, cid: str):
        if cid in self.logZ_cache:
            del self.logZ_cache[cid]

    def _logZ_c(self, cid: str) -> float:
        if cid in self.logZ_cache:
            return self.logZ_cache[cid]
        
        if cid not in self.feature_counts:
            logZ = self.vocab_size * math.log(self.beta)
            self.logZ_cache[cid] = logZ
            return logZ
        
        feature_sum = sum(self.feature_counts[cid].values())
        logZ = 0.0
        
        for word in self.feature_counts[cid]:
            count = self.feature_counts[cid][word]
            logZ += math.lgamma(count + self.beta)
        
        logZ += (self.vocab_size - len(self.feature_counts[cid])) * math.lgamma(self.beta)
        logZ -= math.lgamma(feature_sum + self.vocab_size * self.beta)
        
        self.logZ_cache[cid] = logZ
        return logZ

    def score_batch(self, tf: Counter, cids: List[str]) -> Dict[str, float]:
        scores = {}
        
        for cid in cids:
            score = 0.0
            
            if cid in self.class_counts:
                score += math.log(self.class_counts[cid] + self.alpha)
            else:
                score += math.log(self.alpha)
            
            score += self._logZ_c(cid)
            
            if cid in self.feature_counts:
                for word, count in tf.items():
                    word_count = self.feature_counts[cid].get(word, 0)
                    for _ in range(count):
                        score += math.log(word_count + self.beta)
                        word_count += 1
            else:
                for word, count in tf.items():
                    for _ in range(count):
                        score += math.log(self.beta)
            
            scores[cid] = score
        
        return scores

    def update_positive(self, tf: Counter, cid: str):
        if cid not in self.class_counts:
            self.class_counts[cid] = 0
            self.feature_counts[cid] = Counter()
        
        self.class_counts[cid] += 1
        
        for word, count in tf.items():
            self.feature_counts[cid][word] += count
        
        self._invalidate(cid)

    def decay(self, factor: float = None):
        if factor is None:
            factor = self.gamma
        
        for cid in self.class_counts:
            self.class_counts[cid] *= factor
            for word in self.feature_counts[cid]:
                self.feature_counts[cid][word] *= factor
            self._invalidate(cid)