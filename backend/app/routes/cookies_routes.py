from fastapi import APIRouter, Request, HTTPException
from app.database import db

cookies_router = APIRouter()

@cookies_router.post("/log-cookies")
async def log_user_cookies(request: Request):
    """
    Log user's cookie and terms acceptance status.
    """
    try:
        data = await request.json()
        cookies_collection = db["cookies"]

        # Save or update user's cookie information
        user_entry = {
            "session_id": data["session_id"],
            "terms_accepted": data.get("terms_accepted", False),
            "timestamp": data.get("timestamp"),
        }
        await cookies_collection.update_one({"session_id": data["session_id"]}, {"$set": user_entry}, upsert=True)
        return {"message": "User cookie and terms data logged successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error logging cookies: {str(e)}")
