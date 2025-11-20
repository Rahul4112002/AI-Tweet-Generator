from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import tweets
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Viral Tweet Generator API",
    description="Generate viral tweets using AI with iterative optimization",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tweets.router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to Tweet Generator API",
        "docs": "/docs",
        "health": "/api/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
