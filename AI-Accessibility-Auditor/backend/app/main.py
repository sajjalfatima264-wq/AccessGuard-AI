from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import health
from app.config import settings

app = FastAPI(
    title="AI Accessibility Auditor API",
    description="Backend API for scanning and fixing web accessibility issues.",
    version="0.1.0"
)

# 4. Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)