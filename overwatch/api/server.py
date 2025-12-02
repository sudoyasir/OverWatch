"""
FastAPI server for OverWatch.
Provides REST API endpoints for system metrics.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any
import uvicorn

from overwatch.core import cpu, memory, disk, network, processes, sensors


# Create FastAPI app
app = FastAPI(
    title="OverWatch API",
    description="Advanced System Monitoring API",
    version="0.1.0",
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "OverWatch API",
        "version": "0.1.0",
        "status": "running",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/metrics")
async def get_all_metrics() -> Dict[str, Any]:
    """
    Get all system metrics.
    
    Returns:
        Dict containing CPU, memory, disk, network, and process metrics
    """
    try:
        return {
            "cpu": cpu.get(),
            "memory": memory.get(),
            "disk": disk.get(),
            "network": network.get(),
            "processes": processes.get(limit=20),
            "sensors": sensors.get(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/metrics/cpu")
async def get_cpu_metrics() -> Dict[str, Any]:
    """
    Get CPU metrics.
    
    Returns:
        CPU usage statistics
    """
    try:
        return cpu.get()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/metrics/memory")
async def get_memory_metrics() -> Dict[str, Any]:
    """
    Get memory metrics.
    
    Returns:
        Memory usage statistics
    """
    try:
        return memory.get()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/metrics/disk")
async def get_disk_metrics() -> Dict[str, Any]:
    """
    Get disk metrics.
    
    Returns:
        Disk usage and I/O statistics
    """
    try:
        return disk.get()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/metrics/network")
async def get_network_metrics() -> Dict[str, Any]:
    """
    Get network metrics.
    
    Returns:
        Network I/O and connection statistics
    """
    try:
        return network.get()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/metrics/processes")
async def get_process_metrics(limit: int = 10, sort_by: str = "cpu") -> Dict[str, Any]:
    """
    Get process metrics.
    
    Args:
        limit: Maximum number of processes to return
        sort_by: Sort criteria (cpu, memory, name)
        
    Returns:
        Process information
    """
    try:
        return processes.get(limit=limit, sort_by=sort_by)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/metrics/sensors")
async def get_sensor_metrics() -> Dict[str, Any]:
    """
    Get sensor metrics (temperature, fans, battery).
    
    Returns:
        Sensor data
    """
    try:
        return sensors.get()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/process/{pid}")
async def get_process_details(pid: int) -> Dict[str, Any]:
    """
    Get detailed information about a specific process.
    
    Args:
        pid: Process ID
        
    Returns:
        Detailed process information
    """
    try:
        result = processes.get_process_by_pid(pid)
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def start_server(host: str = "0.0.0.0", port: int = 8000):
    """
    Start the FastAPI server.
    
    Args:
        host: Host address to bind to
        port: Port number to listen on
    """
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    start_server()
