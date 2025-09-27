from fastapi import FastAPI
from dotenv import load_dotenv
from supabase import create_client, Client
import os
from pydantic import BaseModel
from datetime import datetime, date
from uuid import UUID

load_dotenv()
required_vars = ["ENVIRONMENT", "SUPABASE_URL", "SUPABASE_KEY"]
missing_vars = [var for var in required_vars if var not in os.environ]
if missing_vars:
    raise RuntimeError(f"Missing environment variables: {', '.join(missing_vars)}")


# Supabase Setup
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# FastAPI Setup
app = FastAPI(
    title="Allotment",
    description="API for allotment task management app",
    version="0.1.0",
    debug=os.getenv("ENVIRONMENT") == "dev",
)


@app.get("/")
def read_root():
    return {"Hello": "Allotment App"}


class Plot(BaseModel):
    id: int
    created_at: datetime
    profile_id: UUID
    name: str
    location: str
    notes: str


class Bed(BaseModel):
    id: int
    created_at: datetime
    name: str
    size: float
    description: str
    profile_id: UUID


class Crop(BaseModel):
    id: int
    created_at: datetime
    name: str
    description: str
    planting_season: str
    profile_id: UUID


class Planting(BaseModel):
    id: int
    created_at: datetime
    bed_id: int
    crop_id: int
    sow_date: date
    plant_date: date
    harvest_start: date
    harvest_end: date
    quantity: int
    profile_id: UUID


class Profile(BaseModel):
    id: UUID
    created_at: datetime
    name: str


class RecurringTask(BaseModel):
    id: int
    created_at: datetime
    crop_id: int
    bed_id: int
    description: str
    repeat_interval: int
    repeat_unit: str
    repeat_number: int
    plot_id: int
    planting_id: int
    profile_id: int


class ScheduledTask(BaseModel):
    id: int
    created_at: datetime
    crop_id: int
    bed_id: int
    description: str
    due_date: date
    completed: bool
    is_repeating: bool
    repeat_interval: int
    repeat_unit: str
    end_date: date
    plot_id: int
    planting_id: int
    profile_id: int
    recurring_task_id: int
