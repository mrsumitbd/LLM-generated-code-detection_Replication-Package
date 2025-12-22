from fastapi import FastAPI, Request, Body, HTTPException
from .layers import memory as mem

def feedback(payload: dict = Body(...)):
    chat_id = payload.get("chat_id")
    rating = int(payload.get("rating", 0))
    comment = payload.get("comment")
    msg_id = payload.get("message_id")
    if not chat_id:
        raise HTTPException(status_code=400, detail="chat_id required")
    mem.add_feedback(chat_id, msg_id, rating, comment)
    return {"ok": True}