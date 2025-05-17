import asyncio
import os
from websockets.server import serve
from .manager import websocket_manager

async def start_websocket_server():
    host = os.getenv('WEBSOCKET_HOST', 'localhost')
    port = int(os.getenv('WEBSOCKET_PORT', 5001))
    
    # Start connection monitoring
    monitor_task = asyncio.create_task(websocket_manager.monitor_connections())
    
    async with serve(websocket_manager.handler, host, port):
        await asyncio.Future()  # run forever

    monitor_task.cancel()  # Clean up monitor task when server stops

def init_websocket_server():
    asyncio.run(start_websocket_server())

async def get_websocket_status():
    return await websocket_manager.get_status()
