from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests,time,json

from backend.cache.lru_cache import LRUCache
from backend.cache.intelligent_lru import IntelligentLRUCache

app = FastAPI()

normal_cache = LRUCache(capacity=5)
intelligent_cache = IntelligentLRUCache(capacity=5)

url_frequency = {}
last_request_time = {}

class RequestModel(BaseModel):
    url:str

@app.post("/request")
def handle_request(request:RequestModel):

    start_time = time.time()
    url = request.url

    url_frequency[url] = url_frequency.get(url,0)+1

    normal_cached = normal_cache.get(url)
    intelligent_cached = intelligent_cache.get(url)

    current_time = time.time()
    time_diff = current_time - last_request_time.get(url,current_time)
    last_request_time[url] = current_time

    if intelligent_cached:

        return {
            "data": intelligent_cached,
            "cache_status":"HIT"
        }

    try:
        api_response = requests.get(url)
        api_response.raise_for_status()
        data = api_response.json()
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))

    response_time = int((time.time()-start_time)*1000)

    metadata = {
        "url_freq": url_frequency[url],
        "cache_hit":0,
        "response_time_ms":response_time,
        "time_diff":time_diff,
        "data_size":len(str(data))
    }

    normal_cache.put(url,data)
    intelligent_cache.put(url,data,metadata)

    return {
        "data":data,
        "cache_status":"MISS"
    }


@app.get("/comparison")
def comparison():

    return {

        "normal_lru": normal_cache.stats(),
        "intelligent_lru": intelligent_cache.stats(),

        "normal_evictions": normal_cache.evictions,
        "intelligent_evictions": intelligent_cache.evictions
    }
