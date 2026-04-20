from fastapi import FastAPI, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time
import random

app = FastAPI()

# Метрики
http_requests = Counter('http_requests_total', 'Total HTTP', ['method', 'endpoint'])
http_duration = Histogram('http_duration_seconds', 'Duration', ['endpoint'])
messages = Counter('support_messages_total', 'Support messages', ['status'])

@app.middleware("http")
async def metrics_middleware(request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    
    http_requests.labels(method=request.method, endpoint=request.url.path).inc()
    http_duration.labels(endpoint=request.url.path).observe(duration)
    return response

@app.get("/metrics")
async def get_metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/api/stats")
async def stats():
    return {"requests": 42, "messages": 10}

@app.post("/api/support")
async def support():
    messages.labels(status="sent").inc()
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)