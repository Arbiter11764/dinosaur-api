from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Dinosaur Facts API",
    description="""
## Dinosaur Facts API

A full CRUD API for managing dinosaur facts backed by **Supabase (PostgreSQL)**.

### Authentication
All write operations require a Bearer token:
```
Authorization: Bearer your-super-secret-key
```

### Endpoints
| Method | Path | Description |
|--------|------|-------------|
| GET | /health | Health check |
| GET | /dinosaurs | List all dinosaurs |
| GET | /dinosaurs/{id} | Get a single dinosaur |
| POST | /dinosaurs | Add a new dinosaur |
| PUT | /dinosaurs/{id} | Update a dinosaur |
| DELETE | /dinosaurs/{id} | Delete a dinosaur |
""",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SECRET_KEY   = os.getenv("SECRET_KEY", "your-super-secret-key")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

bearer_scheme = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    if credentials.credentials != SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing bearer token",
        )
    return credentials.credentials

class DinoBase(BaseModel):
    name: str                      = Field(..., example="Tyrannosaurus rex")
    period: str                    = Field(..., example="Late Cretaceous")
    diet: str                      = Field(..., example="Carnivore")
    length_m: Optional[float]      = Field(None, example=12.3)
    weight_kg: Optional[int]       = Field(None, example=8000)
    discovered_year: Optional[int] = Field(None, example=1902)
    found_in: Optional[str]        = Field(None, example="Montana, USA")
    fun_fact: Optional[str]        = Field(None, example="Had the most powerful bite of any land animal")

class DinoCreate(DinoBase):
    pass

class DinoUpdate(BaseModel):
    name: Optional[str]            = Field(None, example="Tyrannosaurus rex")
    period: Optional[str]          = Field(None, example="Late Cretaceous")
    diet: Optional[str]            = Field(None, example="Carnivore")
    length_m: Optional[float]      = Field(None, example=12.3)
    weight_kg: Optional[int]       = Field(None, example=8000)
    discovered_year: Optional[int] = Field(None, example=1902)
    found_in: Optional[str]        = Field(None, example="Montana, USA")
    fun_fact: Optional[str]        = Field(None, example="Had the most powerful bite of any land animal")

class Dinosaur(DinoBase):
    id: int
    created_at: Optional[str] = None

    class Config:
        from_attributes = True


@app.get("/health", tags=["Health"], summary="Health check")
def health():
    return {"status": "ok", "version": "1.0.0", "database": "supabase"}


@app.get("/dinosaurs", response_model=List[Dinosaur], tags=["Dinosaurs"], summary="List all dinosaurs")
def list_dinosaurs(
    diet: Optional[str] = None,
    period: Optional[str] = None,
):
    query = supabase.table("dinosaurs").select("*")
    if diet:
        query = query.ilike("diet", f"%{diet}%")
    if period:
        query = query.ilike("period", f"%{period}%")
    result = query.order("id").execute()
    return result.data


@app.get("/dinosaurs/{dino_id}", response_model=Dinosaur, tags=["Dinosaurs"], summary="Get a dinosaur by ID")
def get_dinosaur(dino_id: int):
    result = supabase.table("dinosaurs").select("*").eq("id", dino_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail=f"Dinosaur with id={dino_id} not found")
    return result.data[0]


@app.post("/dinosaurs", response_model=Dinosaur, status_code=201, tags=["Dinosaurs"], summary="Add a dinosaur")
def create_dinosaur(dino: DinoCreate, token: str = Depends(verify_token)):
    result = supabase.table("dinosaurs").insert(dino.model_dump()).execute()
    if not result.data:
        raise HTTPException(status_code=500, detail="Failed to create dinosaur")
    return result.data[0]


@app.put("/dinosaurs/{dino_id}", response_model=Dinosaur, tags=["Dinosaurs"], summary="Update a dinosaur")
def update_dinosaur(dino_id: int, updates: DinoUpdate, token: str = Depends(verify_token)):
    existing = supabase.table("dinosaurs").select("id").eq("id", dino_id).execute()
    if not existing.data:
        raise HTTPException(status_code=404, detail=f"Dinosaur with id={dino_id} not found")
    payload = {k: v for k, v in updates.model_dump().items() if v is not None}
    if not payload:
        raise HTTPException(status_code=400, detail="No fields provided for update")
    result = supabase.table("dinosaurs").update(payload).eq("id", dino_id).execute()
    return result.data[0]


@app.delete("/dinosaurs/{dino_id}", tags=["Dinosaurs"], summary="Delete a dinosaur")
def delete_dinosaur(dino_id: int, token: str = Depends(verify_token)):
    existing = supabase.table("dinosaurs").select("id").eq("id", dino_id).execute()
    if not existing.data:
        raise HTTPException(status_code=404, detail=f"Dinosaur with id={dino_id} not found")
    supabase.table("dinosaurs").delete().eq("id", dino_id).execute()
    return {"message": f"Dinosaur id={dino_id} deleted successfully"}
