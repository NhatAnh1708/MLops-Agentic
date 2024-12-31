"""
Project: Safe-Agentic
Developed by: AnhTDN
Created on: 2025-01-01
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes.safety_agent import router as safety_agent_router
from .routes.health_check import router as health_check_router


app = FastAPI(
    title="Safe-Agentic",
    description="Safe-Agentic is a service that helps to detect and filter toxic messages.",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_check_router)
app.include_router(safety_agent_router)
