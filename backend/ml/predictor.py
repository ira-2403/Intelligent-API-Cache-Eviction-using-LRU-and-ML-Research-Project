import joblib
import numpy as np
from pathlib import Path
MODEL_PATH = Path("backend/ml/cache_reuse_model.pkl")
class CacheReusePredictor:
    def __init__(self):
        self.model=joblib.load(MODEL_PATH)
    def predict(self,features: dict)->int:
        X=np.array([[
            features.get("url_freq",0),
            features.get("time_diff",999999),
            features.get("cache_hit",0),
            features.get("response_time_ms",0),
            features.get("data_size",0)
        ]])
        return int(self.model.predict(X)[0])
    