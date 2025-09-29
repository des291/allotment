from fastapi import FastAPI, HTTPException, status
from dotenv import load_dotenv
from supabase import create_client, Client
import os
from pydantic import BaseModel
from datetime import datetime, date
from uuid import UUID
from typing import List

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
    id: int | None = None
    created_at: datetime | None = None
    profile_id: UUID
    name: str
    location: str
    notes: str


class Bed(BaseModel):
    id: int | None = None
    created_at: datetime | None = None
    name: str
    size: float
    description: str
    profile_id: UUID


class Crop(BaseModel):
    id: int | None = None
    created_at: datetime | None = None
    name: str
    description: str
    planting_season: str
    profile_id: UUID


class Planting(BaseModel):
    id: int | None = None
    created_at: datetime | None = None
    bed_id: int
    crop_id: int
    sow_date: date
    plant_date: date
    harvest_start: date
    harvest_end: date
    quantity: int
    profile_id: UUID


class Profile(BaseModel):
    id: UUID | None = None
    created_at: datetime | None = None
    name: str


class RecurringTask(BaseModel):
    id: int | None = None
    created_at: datetime | None = None
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
    id: int | None = None
    created_at: datetime | None = None
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


# --- Helper: Error Handling ---
async def execute_supabase_query(query):
    try:
        response = await query.execute()
        if response.data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No data found"
            )
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Supabase error: {str(e)}",
        )


@app.post("/profiles/", response_model=Profile, status_code=status.HTTP_201_CREATED)
async def create_profile(profile: Profile):
    data = await execute_supabase_query(
        supabase.table("profiles").insert(profile.model_dump()).execute()
    )
    return data.data[0]


@app.get("/profiles/", response_model=List[Profile])
async def get_profiles():
    data = await execute_supabase_query(supabase.table("profiles").select("*"))
    return data.data


@app.post("/plots/", response_model=Plot, status_code=status.HTTP_201_CREATED)
async def create_plot(plot: Plot):
    data = await execute_supabase_query(
        supabase.table("plots").insert(plot.model_dump()).execute()
    )
    return data.data[0]


@app.get("/plots/", response_model=List[Plot])
async def list_plots():
    data = await execute_supabase_query(supabase.table("plots").select("*"))
    return data.data
