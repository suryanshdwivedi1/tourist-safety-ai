from fastapi import FastAPI
from typing import List
from geopy.distance import geodesic
import time

app = FastAPI()

# -------------------------
# Mock Data (can connect to DB later)
# -------------------------

# Predefined risky zones (lat, lon, radius in km)
risky_zones = [
    (26.1445, 91.7362, 2),   # Example: Guwahati city center
    (27.1767, 78.0081, 1.5)  # Example: Agra near Taj Mahal
]

# Store last known tourist location + timestamp
last_location = {}
planned_routes = {
    "tourist1": [(26.1445, 91.7362), (26.2000, 91.7500)]  # Example route
}


# -------------------------
# Utility Functions
# -------------------------
def is_in_risky_zone(lat: float, lon: float):
    for z in risky_zones:
        dist = geodesic((lat, lon), (z[0], z[1])).km
        if dist <= z[2]:
            return True, dist
    return False, None


# -------------------------
# 1. Tourist Safety Risk Alert
# -------------------------
@app.get("/get_risk_score")
def get_risk_score(lat: float, lon: float):
    risky, dist = is_in_risky_zone(lat, lon)
    if risky:
        return {
            "risk_score": 75,
            "message": "⚠️ High-risk zone detected. Avoid this area after dark."
        }
    return {
        "risk_score": 20,
        "message": "✅ You are in a safe zone."
    }


# -------------------------
# 2. Anomaly Detection
# -------------------------
@app.get("/detect_anomaly")
def detect_anomaly(tourist_id: str, lat: float, lon: float):
    current_time = time.time()

    # If first location, store it
    if tourist_id not in last_location:
        last_location[tourist_id] = (lat, lon, current_time)
        return {"status": "tracking started"}

    prev_lat, prev_lon, prev_time = last_location[tourist_id]
    last_location[tourist_id] = (lat, lon, current_time)

    # Rule 1: Inactivity > 5 minutes
    if current_time - prev_time > 300:
        return {"alert": "🚨 Possible distress: No movement for over 5 minutes."}

    # Rule 2: Off-route detection (very simple version)
    planned = planned_routes.get(tourist_id, [])
    if planned:
        start, end = planned[0], planned[-1]
        dist_from_end = geodesic((lat, lon), end).km
        if dist_from_end > 5:  # more than 5 km away from destination
            return {"alert": "🚨 Tourist deviated from planned route!"}

    return {"status": "✅ Normal movement"}


# -------------------------
# 3. Panic Button Chat
# -------------------------
@app.get("/panic_chat")
def panic_chat(query: str):
    query_lower = query.lower()

    if "lost" in query_lower:
        return {"response": "Nearest police station is 1.2 km away. Stay calm, sharing location..."}
    elif "unsafe" in query_lower or "help" in query_lower:
        return {"response": "Do you want me to alert police and share your live location?"}
    elif "injured" in query_lower:
        return {"response": "Nearest hospital is 2 km away. Ambulance request initiated."}
    else:
        return {"response": "I'm here to help. Please describe your situation."}
