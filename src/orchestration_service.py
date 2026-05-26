from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from prometheus_client import Counter, Gauge, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import time
from datetime import datetime
import asyncio
import random

app = FastAPI(title="Axiom DataOps Platform")

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Prometheus Metrics
request_count = Counter(
    'axiom_requests_total',
    'Total requests to Axiom platform',
    ['method', 'endpoint', 'status']
)

request_duration = Histogram(
    'axiom_request_duration_seconds',
    'Request duration in seconds',
    ['method', 'endpoint']
)

active_connections = Gauge(
    'axiom_active_connections',
    'Number of active connections'
)

cpu_usage = Gauge(
    'axiom_cpu_usage_percent',
    'CPU usage percentage'
)

memory_usage = Gauge(
    'axiom_memory_usage_percent',
    'Memory usage percentage'
)

disk_usage = Gauge(
    'axiom_disk_usage_percent',
    'Disk usage percentage'
)

etl_jobs_total = Counter(
    'axiom_etl_jobs_total',
    'Total ETL jobs executed',
    ['status']
)

data_processed_bytes = Counter(
    'axiom_data_processed_bytes_total',
    'Total data processed in bytes'
)

service_uptime = Gauge(
    'axiom_service_uptime_seconds',
    'Service uptime in seconds',
    ['service_name']
)

# Global state for demo
app_start_time = datetime.now()
request_counter = 0

@app.middleware("http")
async def track_requests(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    request_count.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()
    
    request_duration.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(process_time)
    
    return response

@app.get("/")
async def root():
    return FileResponse("static/index.html")

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    # Update gauges with current values
    active_connections.set(random.randint(120, 200))
    cpu_usage.set(round(random.uniform(15, 45), 1))
    memory_usage.set(round(random.uniform(35, 65), 1))
    disk_usage.set(round(random.uniform(50, 80), 1))
    
    # Update service uptimes
    uptime_seconds = (datetime.now() - app_start_time).total_seconds()
    service_uptime.labels(service_name="etl_pipeline").set(uptime_seconds)
    service_uptime.labels(service_name="data_quality").set(uptime_seconds)
    service_uptime.labels(service_name="orchestration").set(uptime_seconds)
    
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/api/status")
async def get_status():
    global request_counter
    request_counter += 1
    uptime_seconds = (datetime.now() - app_start_time).total_seconds()
    
    etl_jobs_total.labels(status='completed').inc(random.randint(0, 2))
    data_processed_bytes.inc(random.randint(1000000, 5000000))
    
    return {
        "status": "running",
        "platform": "Axiom DataOps",
        "version": "1.0.0",
        "uptime_seconds": uptime_seconds,
        "total_requests": request_counter,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/health")
async def health():
    return {
        "status": "healthy",
        "service": "Orchestration Service",
        "active": True
    }

@app.get("/api/services")
async def get_services():
    return {
        "services": [
            {"name": "ETL Pipeline", "status": "active", "uptime": "42h 30m"},
            {"name": "Data Quality Framework", "status": "active", "uptime": "42h 30m"},
            {"name": "Monitoring & Logging", "status": "active", "uptime": "42h 30m"},
            {"name": "Security Measures", "status": "active", "uptime": "42h 30m"}
        ]
    }

@app.get("/api/metrics")
async def get_metrics():
    return {
        "cpu_usage": round(random.uniform(15, 45), 1),
        "memory_usage": round(random.uniform(35, 65), 1),
        "disk_usage": round(random.uniform(50, 80), 1),
        "network_in_mbps": round(random.uniform(5, 20), 1),
        "network_out_mbps": round(random.uniform(3, 15), 1),
        "active_connections": random.randint(120, 200),
        "requests_per_second": round(random.uniform(30, 60), 1)
    }

@app.get("/api/logs")
async def get_logs():
    return {
        "logs": [
            {"timestamp": "2026-05-26 14:40:15", "level": "INFO", "message": "ETL Pipeline started successfully"},
            {"timestamp": "2026-05-26 14:40:10", "level": "INFO", "message": "Data validation completed: 10,000 records processed"},
            {"timestamp": "2026-05-26 14:40:05", "level": "INFO", "message": "Orchestration service initialized"},
            {"timestamp": "2026-05-26 14:40:00", "level": "INFO", "message": "Database connection established"},
        ]
    }

if __name__ == "__main__":
    import uvicorn
    print("Starting Axiom Orchestration Service...")
    print("Dashboard available at http://localhost/")
    print("Prometheus metrics available at http://localhost/metrics")
    uvicorn.run(app, host="0.0.0.0", port=8080)
