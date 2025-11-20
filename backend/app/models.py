from pydantic import BaseModel, Field
from typing import Literal, List

class TweetRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=200, description="Topic for tweet generation")
    max_iteration: int = Field(default=3, ge=1, le=5, description="Maximum optimization iterations")

class TweetIteration(BaseModel):
    iteration: int
    tweet: str
    feedback: str
    evaluation: str

class TweetResponse(BaseModel):
    final_tweet: str
    evaluation: Literal["approved", "needs_improvement"]
    total_iterations: int
    history: List[TweetIteration]
    topic: str
