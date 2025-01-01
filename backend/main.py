from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from api.routes import document, chat
from db.session import Base
from db.session import engine
from datetime import datetime, timezone
import time

from dotenv import load_dotenv
load_dotenv() ## Mini Guys Loads .env File

start_time = time.time()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["health"])
async def health_check():
    return {
        "status": "healthy",
        "uptime": round(time.time() - start_time),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


# Include routers
app.include_router(document.router, prefix=f"{settings.API_V1_STR}/documents", tags=["documents"])
app.include_router(chat.router, prefix=f"{settings.API_V1_STR}/chat", tags=["chat"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)