from fastapi import FastAPI
from pydantic import BaseModel
from chatbot import chatbot_response   
import qrcode
import io
from fastapi.responses import StreamingResponse
app = FastAPI()

# -----------------------------
# Data Models
# -----------------------------
class TouristID(BaseModel):
    name: str
    trip_id: str
    contact: str

class Location(BaseModel):
    tourist_id: str
    lat: float
    lon: float

class ChatMessage(BaseModel):
    tourist_id: str
    message: str

class TouristInfo(BaseModel):
    tourist_id: str
    name: str
    trip_id: str
    emergency_contact: str

# -----------------------------
# Mock DB
# -----------------------------
tourists = {}

# -----------------------------
# API Endpoints
# -----------------------------
@app.post("/generate_id")
def generate_id(tourist: TouristID):
    tourists[tourist.trip_id] = tourist.dict()
    return {
        "qr_id": f"QR-{tourist.trip_id}",
        "details": tourist.dict()
    }

@app.post("/check_location")
def check_location(loc: Location):
    if 26.0 <= loc.lat <= 26.3 and 92.8 <= loc.lon <= 93.0:
        return {
            "risk": "HIGH",
            "advice": "Avoid this area after dark. Stay on main roads."
        }
    return {
        "risk": "LOW",
        "advice": "Area seems safe. Stay alert and follow local guidelines."
    }

@app.post("/panic")
def panic_alert(loc: Location):
    return {
        "alert": "SOS Triggered 🚨",
        "location": {"lat": loc.lat, "lon": loc.lon},
        "action": "Police notified (mock)"
    }

@app.post("/chat")
def chat(msg: ChatMessage):
    reply = chatbot_response(msg.message)
    return {"reply": reply}


@app.post("/generate_qr")
def generate_qr(info: TouristInfo):
    # Convert the tourist info into QR code data
    data = info.dict()

    img = qrcode.make(str(data))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")


@app.get("/generate_qr/{tourist_id}")
def generate_qr(tourist_id: str):
    # For now, just encode TouristID, later we can put JSON
    data = {
        "tourist_id": tourist_id,
        "name": "Demo Tourist",
        "trip_id": "TRIP123",
        "emergency_contact": "+911234567890"
    }

    img = qrcode.make(str(data))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")
