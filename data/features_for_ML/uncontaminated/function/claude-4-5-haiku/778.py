from fastapi import FastAPI, Body
from pydantic import BaseModel
import json

app = FastAPI()

class FeedbackItem(BaseModel):
    user_id: str
    message: str
    rating: int = None
    timestamp: str = None

@app.post("/feedback")
def feedback(payload: dict = Body(...)):
    try:
        if not payload:
            return {"status": "error", "message": "Empty payload"}
        
        required_fields = ["user_id", "message"]
        for field in required_fields:
            if field not in payload:
                return {"status": "error", "message": f"Missing required field: {field}"}
        
        user_id = payload.get("user_id")
        message = payload.get("message")
        rating = payload.get("rating")
        timestamp = payload.get("timestamp")
        
        if not isinstance(user_id, str) or not user_id.strip():
            return {"status": "error", "message": "Invalid user_id"}
        
        if not isinstance(message, str) or not message.strip():
            return {"status": "error", "message": "Invalid message"}
        
        if rating is not None:
            if not isinstance(rating, int) or rating < 1 or rating > 5:
                return {"status": "error", "message": "Rating must be an integer between 1 and 5"}
        
        feedback_data = {
            "user_id": user_id,
            "message": message,
            "rating": rating,
            "timestamp": timestamp
        }
        
        return {
            "status": "success",
            "message": "Feedback received successfully",
            "data": feedback_data
        }
    
    except Exception as e:
        return {"status": "error", "message": str(e)}