import pathway as pw
from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
import uvicorn
import os

app = FastAPI()


client = MongoClient(os.getenv("MONGO_URI"))
db = client["test"]
ward_collection = db["wards"]

class ComplaintEvent(BaseModel):
    wardNumber: int
    status: str
    createdAt: str

@app.post("/event")
async def receive_event(event: ComplaintEvent):
    process_events(event.model_dump())
    return {"status": "received"}



def process_events(event):
    ward = event["wardNumber"]
    status = event["status"]

    score_change = 0

    if status == "completed":
        score_change = 10
    elif status == "resolved":
        score_change = 5
    elif status == "pending":
        score_change = -5
    elif status == "in-progress":
        score_change = -2

    # Update performanceScore
    result = ward_collection.update_one(
        {"wardNumber": ward},
        {"$inc": {"performanceScore": score_change}},
        upsert=False
    )


    # Recalculate ranks
    wards = list(
        ward_collection.find().sort("performanceScore", -1)
    )

    for index, ward_doc in enumerate(wards):
        ward_collection.update_one(
            {"_id": ward_doc["_id"]},
            {"$set": {"rank": index + 1}}
        )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
