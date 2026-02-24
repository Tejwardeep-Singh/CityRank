import pathway as pw
from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
import uvicorn

app = FastAPI()

client = MongoClient("mongodb+srv://atessquad4_db_user:1LTErlWI8229Zpc4@routerakshak.v7masfp.mongodb.net/?appName=RouteRakshak")
db = client["RouteRakshak"]
ward_collection = db["wards"]

# In-memory storage
events = []

class ComplaintEvent(BaseModel):
    wardNumber: int
    status: str
    createdAt: str

@app.post("/event")
async def receive_event(event: ComplaintEvent):
    events.append(event.dict())
    process_events()
    return {"status": "received"}

def process_events():
    ward_scores = {}

    for e in events:
        ward = e["wardNumber"]
        status = e["status"]

        if ward not in ward_scores:
            ward_scores[ward] = 0

        if status == "completed":
            ward_scores[ward] += 10
        elif status == "resolved":
            ward_scores[ward] += 5
        elif status == "pending":
            ward_scores[ward] -= 5

    # Update Mongo
    for ward, score in ward_scores.items():
        ward_collection.update_one(
            {"wardNumber": ward},
            {"$set": {"performanceScore": score}}
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)