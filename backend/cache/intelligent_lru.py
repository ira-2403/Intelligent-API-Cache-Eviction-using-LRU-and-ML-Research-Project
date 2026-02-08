from backend.cache.lru_cache import LRUCache
from backend.ml.predictor import CacheReusePredictor
import time

class IntelligentLRUCache(LRUCache):

    def __init__(self,capacity:int):
        super().__init__(capacity)

        self.predictor = CacheReusePredictor()

        self.metadata_store = {}
        self.access_time = {}

        self.evictions = []

    # ---------- HYBRID SCORE -------------

    def calculate_final_score(self,key):

        metadata = self.metadata_store.get(key,{})

        freq = metadata.get("url_freq",0)
        hits = metadata.get("cache_hit",0)

        frequency_score = freq*3 + hits*5

        try:
            ml_score = self.predictor.predict(metadata)
        except:
            ml_score = 0

        # recency decay
        recency = time.time() - self.access_time.get(key,time.time())
        recency_penalty = recency * 0.05

        final_score = (
            frequency_score * 0.6 +
            ml_score * 2 -
            recency_penalty
        )

        return final_score

    # -------------------------------------

    def get_eviction_candidate(self):

        lowest_key = None
        lowest_score = float("inf")

        for key in self.cache.keys():

            score = self.calculate_final_score(key)

            if score < lowest_score:
                lowest_score = score
                lowest_key = key

        return lowest_key, lowest_score

    # -------------------------------------

    def put(self,key,value,metadata=None):

        if metadata is None:
            metadata = {}

        self.metadata_store[key] = metadata
        self.access_time[key] = time.time()

        if self.size >= self.capacity:

            evict_key,score = self.get_eviction_candidate()

            if evict_key:

                self.evictions.append({
                    "key": evict_key,
                    "score": score,
                    "reason": "Hybrid Intelligent Eviction",
                    "time": time.time()
                })

                node = self.cache.get(evict_key)

                if node:
                    self._remove_node(node)
                    del self.cache[evict_key]
                    self.metadata_store.pop(evict_key,None)
                    self.access_time.pop(evict_key,None)
                    self.size -= 1

        super().put(key,value)

    def get(self,key):

        value = super().get(key)

        if value is not None:

            metadata = self.metadata_store.get(key,{})

            metadata["cache_hit"] = metadata.get("cache_hit",0)+1
            metadata["url_freq"] = metadata.get("url_freq",0)+1

            self.metadata_store[key] = metadata
            self.access_time[key] = time.time()

        return value
