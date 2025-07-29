from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers import users, reports, downloads
from app.database import engine
from app.models import Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI Clean Architecture",
    description="A FastAPI application following clean architecture principles",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(reports.router, prefix="/api/v1/reports", tags=["reports"])
app.include_router(downloads.router, prefix="/api/v1/downloads", tags=["downloads"])

@app.get("/")
async def root():
    return {"message": "FastAPI Clean Architecture Application"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
