from fastapi import APIRouter, HTTPException
from app.models import TweetRequest, TweetResponse
from app.services.tweet_generator import generate_viral_tweet

router = APIRouter(prefix="/api", tags=["tweets"])

@router.post("/generate-tweet", response_model=TweetResponse)
async def create_tweet(request: TweetRequest):
    """Generate a viral tweet based on the provided topic"""
    try:
        result = generate_viral_tweet(
            topic=request.topic,
            max_iteration=request.max_iteration
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Tweet Generator API"}
