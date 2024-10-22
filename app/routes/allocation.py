from fastapi import APIRouter, HTTPException, Query, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.schemas import *
from datetime import datetime, time
from typing import List
from bson import ObjectId
import pytz

router = APIRouter()

def get_database() -> AsyncIOMotorDatabase:
    return app.mongodb

# Create allocation
@router.post("/allocations/", response_model=AllocationResponse, 
             summary="Create a new vehicle allocation",
             response_description="The created allocation")
async def create_allocation(
    allocation: AllocationCreate,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Create a new vehicle allocation with the following constraints:
    - Allocation can only be made for future dates
    - Vehicle should not be already allocated for the requested date
    - Employee and vehicle IDs must be valid (1-1000)
    """
    # Validate allocation date
    current_date = datetime.now(pytz.UTC)
    if allocation.allocation_date.date() <= current_date.date():
        raise HTTPException(status_code=400, detail="Allocation can only be made for future dates")

    # Check if vehicle is already allocated
    existing_allocation = await db.allocations.find_one({
        "vehicle_id": allocation.vehicle_id,
        "allocation_date": {
            "$gte": datetime.combine(allocation.allocation_date.date(), time.min),
            "$lte": datetime.combine(allocation.allocation_date.date(), time.max)
        },
        "status": {"$nin": ["cancelled"]}
    })

    if existing_allocation:
        raise HTTPException(status_code=400, detail="Vehicle already allocated for this date")

    # Create allocation document
    allocation_dict = allocation.model_dump()
    allocation_dict.update({
        "status": AllocationStatus.PENDING,
        "created_at": current_date,
        "updated_at": current_date
    })

    result = await db.allocations.insert_one(allocation_dict)
    
    created_allocation = await db.allocations.find_one({"_id": result.inserted_id})
    created_allocation["id"] = str(created_allocation.pop("_id"))
    
    return AllocationResponse(**created_allocation)

# Update allocation
@router.patch("/allocations/{allocation_id}", response_model=AllocationResponse)
async def update_allocation(
    allocation_id: str,
    allocation_update: AllocationUpdate,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Update an existing allocation. Can only update allocations for future dates.
    """
    try:
        allocation = await db.allocations.find_one({"_id": ObjectId(allocation_id)})
    except:
        raise HTTPException(status_code=404, detail="Allocation not found")

    if not allocation:
        raise HTTPException(status_code=404, detail="Allocation not found")

    current_date = datetime.now(pytz.UTC)
    if allocation["allocation_date"].date() <= current_date.date():
        raise HTTPException(status_code=400, detail="Cannot update past or current allocations")

    update_data = {k: v for k, v in allocation_update.model_dump(exclude_unset=True).items() if v is not None}
    update_data["updated_at"] = current_date

    await db.allocations.update_one(
        {"_id": ObjectId(allocation_id)},
        {"$set": update_data}
    )

    updated_allocation = await db.allocations.find_one({"_id": ObjectId(allocation_id)})
    updated_allocation["id"] = str(updated_allocation.pop("_id"))
    
    return AllocationResponse(**updated_allocation)

# Delete allocation
@router.delete("/allocations/{allocation_id}", status_code=204)
async def delete_allocation(
    allocation_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Delete an allocation. Can only delete allocations for future dates.
    """
    try:
        allocation = await db.allocations.find_one({"_id": ObjectId(allocation_id)})
    except:
        raise HTTPException(status_code=404, detail="Allocation not found")

    if not allocation:
        raise HTTPException(status_code=404, detail="Allocation not found")

    current_date = datetime.now(pytz.UTC)
    if allocation["allocation_date"].date() <= current_date.date():
        raise HTTPException(status_code=400, detail="Cannot delete past or current allocations")

    await db.allocations.delete_one({"_id": ObjectId(allocation_id)})

# Get allocation history with filters
@router.get("/allocations/", response_model=List[AllocationResponse])
async def get_allocations(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    employee_id: Optional[int] = None,
    vehicle_id: Optional[int] = None,
    status: Optional[AllocationStatus] = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Get allocation history with optional filters:
    - Date range
    - Employee ID
    - Vehicle ID
    - Allocation status
    Includes pagination support
    """
    query = {}
    
    if start_date and end_date:
        query["allocation_date"] = {
            "$gte": start_date,
            "$lte": end_date
        }
    elif start_date:
        query["allocation_date"] = {"$gte": start_date}
    elif end_date:
        query["allocation_date"] = {"$lte": end_date}

    if employee_id:
        query["employee_id"] = employee_id
    if vehicle_id:
        query["vehicle_id"] = vehicle_id
    if status:
        query["status"] = status

    cursor = db.allocations.find(query).skip(skip).limit(limit).sort("allocation_date", -1)
    allocations = []
    
    async for allocation in cursor:
        allocation["id"] = str(allocation.pop("_id"))
        allocations.append(AllocationResponse(**allocation))
    
    return allocations