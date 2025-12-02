"""
WebSocket server for OverWatch.
Provides real-time system metrics via WebSocket.
"""

from fastapi import WebSocket, WebSocketDisconnect
from typing import Set
import asyncio
import json

from overwatch.core import cpu, memory, disk, network, processes, sensors


class ConnectionManager:
    """Manages WebSocket connections."""
    
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
    
    async def connect(self, websocket: WebSocket):
        """
        Accept and register a new WebSocket connection.
        
        Args:
            websocket: WebSocket connection
        """
        await websocket.accept()
        self.active_connections.add(websocket)
    
    def disconnect(self, websocket: WebSocket):
        """
        Remove a WebSocket connection.
        
        Args:
            websocket: WebSocket connection to remove
        """
        self.active_connections.discard(websocket)
    
    async def broadcast(self, message: str):
        """
        Broadcast a message to all connected clients.
        
        Args:
            message: Message to broadcast
        """
        disconnected = set()
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                disconnected.add(connection)
        
        # Remove disconnected clients
        for connection in disconnected:
            self.disconnect(connection)


# Create connection manager
manager = ConnectionManager()


async def get_system_metrics() -> dict:
    """
    Get all system metrics.
    
    Returns:
        Dict with all metrics
    """
    return {
        "cpu": cpu.get(),
        "memory": memory.get(),
        "disk": disk.get(),
        "network": network.get(),
        "processes": processes.get(limit=10),
        "sensors": sensors.get(),
    }


async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time metrics.
    
    Args:
        websocket: WebSocket connection
    """
    await manager.connect(websocket)
    
    try:
        while True:
            # Get system metrics
            metrics = await get_system_metrics()
            
            # Send to client
            await websocket.send_text(json.dumps(metrics))
            
            # Wait 1 second before next update
            await asyncio.sleep(1)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)


def setup_websocket_routes(app):
    """
    Add WebSocket routes to FastAPI app.
    
    Args:
        app: FastAPI application instance
    """
    @app.websocket("/ws")
    async def websocket_route(websocket: WebSocket):
        await websocket_endpoint(websocket)
