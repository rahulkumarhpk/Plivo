from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from db.session import engine, Base
from api.v1 import services, incidents, organizations
from websocket.server import get_websocket_status

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

# CORS settings - update origins as needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(services.router, prefix=f"{settings.API_V1_STR}/services", tags=["services"])
app.include_router(
    incidents.router,
    prefix="/api/v1/incidents",
    tags=["incidents"]
)
app.include_router(organizations.router, prefix=f"{settings.API_V1_STR}/organizations", tags=["organizations"])

@app.get("/ws/status")
async def websocket_status():
    """Get current WebSocket connection status"""
    return await get_websocket_status()

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}
