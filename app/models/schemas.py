from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum

class AllocationStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class EmployeeBase(BaseModel):
    employee_id: int = Field(..., gt=0, le=1000)
    name: str
    department: str

class VehicleBase(BaseModel):
    vehicle_id: int = Field(..., gt=0, le=1000)
    model: str
    registration_number: str
    driver_id: int = Field(..., gt=0, le=1000)

class AllocationCreate(BaseModel):
    employee_id: int = Field(..., gt=0, le=1000)
    vehicle_id: int = Field(..., gt=0, le=1000)
    allocation_date: datetime
    purpose: str

class AllocationUpdate(BaseModel):
    purpose: Optional[str] = None
    status: Optional[AllocationStatus] = None

class AllocationResponse(BaseModel):
    id: str
    employee_id: int
    vehicle_id: int
    allocation_date: datetime
    purpose: str
    status: AllocationStatus
    created_at: datetime
    updated_at: datetime

class AllocationFilter(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    employee_id: Optional[int] = None
    vehicle_id: Optional[int] = None
    status: Optional[AllocationStatus] = None