from contextlib import asynccontextmanager
from fastapi import FastAPI
from foundation.config import settings
from foundation.database import Database
from foundation.logging import configure_logging
from integrations.opik_client import configure_opik

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print(f"Starting {settings.app_name} in {settings.environment}...")
    configure_opik()
    
    # Initialize DB (Lazy checks)
    # await Database.init() # Explicit check if desired
    
    yield
    
    # Shutdown
    print("Shutting down...")
    await Database.close()

app = FastAPI(title=settings.app_name, lifespan=lifespan)

# Configure OpenTelemetry
configure_logging(app)

@app.get("/")
def read_root():
    return {
        "service": settings.app_name,
        "environment": settings.environment,
        "status": "active"
    }

@app.get("/health")
async def health_check():
    # Simple DB connection check could go here
    return {"status": "ok"}
