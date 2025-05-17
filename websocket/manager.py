import asyncio
import json
from websockets.server import serve, WebSocketServerProtocol
from typing import Set, Dict
from datetime import datetime

class WebSocketManager:
    def __init__(self):
        self.connections: Set[WebSocketServerProtocol] = set()
        self.last_ping: Dict[WebSocketServerProtocol, datetime] = {}

    async def register(self, websocket: WebSocketServerProtocol):
        self.connections.add(websocket)
        self.last_ping[websocket] = datetime.now()

    async def unregister(self, websocket: WebSocketServerProtocol):
        self.connections.remove(websocket)
        self.last_ping.pop(websocket, None)

    async def broadcast(self, message: Dict):
        if self.connections:
            await asyncio.gather(
                *[connection.send(json.dumps(message)) for connection in self.connections]
            )

    async def check_connection(self, websocket: WebSocketServerProtocol) -> bool:
        try:
            await websocket.ping()
            return True
        except Exception:
            await self.unregister(websocket)
            return False

    async def get_status(self) -> Dict:
        active_connections = len(self.connections)
        connection_details = []
        
        for ws in self.connections:
            is_alive = await self.check_connection(ws)
            last_ping = self.last_ping.get(ws, None)
            connection_details.append({
                "client_id": id(ws),
                "connected_since": last_ping.isoformat() if last_ping else None,
                "is_alive": is_alive
            })
        
        return {
            "active_connections": active_connections,
            "connections": connection_details
        }

    async def monitor_connections(self):
        while True:
            for ws in list(self.connections):
                await self.check_connection(ws)
            await asyncio.sleep(30)  # Check every 30 seconds

    @staticmethod
    async def handler(websocket: WebSocketServerProtocol):
        manager = websocket_manager
        await manager.register(websocket)
        try:
            async for message in websocket:
                pass  # We only handle outgoing messages
        finally:
            await manager.unregister(websocket)

websocket_manager = WebSocketManager()
