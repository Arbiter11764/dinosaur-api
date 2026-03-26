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
