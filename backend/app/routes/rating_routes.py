from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.services.rating_service import add_or_update_rating, get_user_rating, get_average_rating

rating_router = APIRouter()

# Define a Pydantic model for the request body
class RatingRequest(BaseModel):
    user_session: str = Field(..., description="Unique session identifier for the user")
    download_type: str = Field(..., description="Type of download (e.g., 'tiktok', 'soundcloud')")
    rating: float = Field(..., ge=1, le=5, description="Rating value between 1 and 5")

@rating_router.post("/ratings")
async def rate_download(request: RatingRequest):
    """
    Endpoint to add or update a rating for a download.
    """
    try:
        return await add_or_update_rating(request.user_session, request.download_type, request.rating)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@rating_router.get("/ratings/user")
async def get_user_rating_endpoint(user_session: str, download_type: str):
    """
    Endpoint to get a user's rating for a specific download type.
    """
    rating = await get_user_rating(user_session, download_type)
    if not rating:
        raise HTTPException(status_code=404, detail="No rating found for this user and download type.")
    return rating


@rating_router.get("/ratings/average")
async def get_average_rating_endpoint(download_type: str):
    """
    Endpoint to get the average rating for a specific download type.
    """
    return await get_average_rating(download_type)
