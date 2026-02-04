from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests,time,json
from backend.cache.intelligent_lru import IntelligentLRUCache
from backend.utils.logger import log_request
app=FastAPI()
cache=IntelligentLRUCache(capacity=5)
class RequestModel(BaseModel):
    url:str
@app.post("/request")
def handle_request(request:RequestModel):
    start_time=time.time()
    url=request.url
    cached_response=cache.get(url)
    if cached_response:
        response_time=int((time.time()-start_time)*1000)
        data_size=len(json.dumps(cached_response))
        log_request(
            url=url,
            cache_status="HIT",
            response_time_ms=response_time,
            data_size=data_size
            )
        return {
            "data":cached_response,
            "cache_status":"HIT",
            "response_time_ms":response_time,
            "data_size":data_size
            }
    try:
        api_response=requests.get(url)
        api_response.raise_for_status()
        data=api_response.json()
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))
    response_time=int((time.time()-start_time)*1000)
    cache.put(url, 
              data,
              metadata={
                  "url_freq":1,
                  "time_diff":response_time,
                  "cache_hit":0,
                  "response_time_ms":response_time,
                  "data_size":len(str(data))
              })
    data_size=len(json.dumps(data))
    log_request(url,"MISS",response_time,data_size)
    return {
        "data":data,
        "cache_status":"MISS",
        "response_time_ms":response_time,
        "data_size":data_size
    }
