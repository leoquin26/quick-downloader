from app.database import db

async def add_or_update_rating(user_session: str, download_type: str, rating: float):
    if not (1 <= rating <= 5):
        raise ValueError("Rating must be between 1 and 5.")

    ratings_collection = db["ratings"]
    filter_query = {"user_session": user_session, "download_type": download_type}
    update_data = {"$set": {"rating": rating}}
    await ratings_collection.update_one(filter_query, update_data, upsert=True)
    return {"message": "Rating saved successfully."}


async def get_user_rating(user_session: str, download_type: str):
    ratings_collection = db["ratings"]
    rating = await ratings_collection.find_one({"user_session": user_session, "download_type": download_type})
    return {"rating": rating["rating"]} if rating else None


async def get_average_rating(download_type: str = None):
    """
    Calculate the average rating.
    If `download_type` is provided, calculate for that type; otherwise, calculate the overall average.
    """
    ratings_collection = db["ratings"]

    pipeline = []
    # Add a $match stage only if download_type is provided
    if download_type and download_type != "overall":
        pipeline.append({"$match": {"download_type": {"$regex": f"^{download_type}$", "$options": "i"}}})

    pipeline.append(
        {"$group": {"_id": None, "average_rating": {"$avg": "$rating"}, "total_ratings": {"$sum": 1}}}
    )

    result = await ratings_collection.aggregate(pipeline).to_list(length=1)
    print("Matching Documents:", result)

    if not result:
        return {"average_rating": 0, "total_ratings": 0}

    return {
        "average_rating": round(result[0]["average_rating"], 2),
        "total_ratings": result[0]["total_ratings"],
    }
