from backend.cache.lru_cache import LRUCache
from backend.ml.predictor import CacheReusePredictor
import time
class IntelligentLRUCache(LRUCache):
    def __init__(self,capacity:int):
        super().__init__(capacity)
        self.predictor=CacheReusePredictor()
    def put(self,key,value,metadata:None):
        if metadata is None:
            metadata={}
        if self.size<self.capacity:
            super().put(key,value)
            return
        lru_node=self.tail.prev
        lru_key=lru_node.key
        prediction=0
        try:
            prediction=self.predictor.predict(metadata)
        except Exception:
            pass
        if prediction==0:
            self._remove_node(lru_node)
            del self.cache[lru_key]
            self.size-=1
        super().put(key,value)
