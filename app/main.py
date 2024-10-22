from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
from app.routes import allocation
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Vehicle Allocation System",
    description="API for managing vehicle allocations for company employees",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(settings.MONGODB_URL)
    app.mongodb = app.mongodb_client[settings.DATABASE_NAME]
    
    # Create indexes for optimization
    await app.mongodb["allocations"].create_index([("allocation_date", 1), ("vehicle_id", 1)], unique=True)
    await app.mongodb["allocations"].create_index([("employee_id", 1)])
    await app.mongodb["allocations"].create_index([("status", 1)])

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(allocation.router, prefix="/api/v1", tags=["Allocations"])
