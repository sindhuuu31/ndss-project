import os
import pickle
import collections
import random
import asyncio
from datetime import datetime
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'frontend'))
MODEL_PATH = os.path.join(BASE_DIR, "ndss_model.pkl")

try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

traffic_queue = collections.deque()
analyzed_results = []

def analyze_traffic(packet):
    if not model:
        return {"error": "Model not loaded"}

    features = [[packet['packet_count'], packet['packet_size'], packet['entropy']]]
    pred = model.predict(features)[0]
    
    if pred == 1:
        status = "MALICIOUS"
        reason = "DDoS Signature Detected"
    else:
        status = "NORMAL"
        reason = "Safe Request"

    return {
        "id": packet["id"],
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "packet_count": packet["packet_count"],
        "packet_size": packet["packet_size"],
        "entropy": packet["entropy"],
        "status": status,
        "reason": reason
    }

async def process_traffic_queue():
    while True:
        if traffic_queue:
            packet = traffic_queue.popleft() 
            result = analyze_traffic(packet)
            analyzed_results.append(result)
            
            if len(analyzed_results) > 100:
                analyzed_results.pop(0) 
        await asyncio.sleep(0.5)

async def ingest_traffic_simulator():
    packet_id = 0
    while True:
        packet_id += 1
        is_attack = random.random() < 0.25 
        
        if is_attack:
            packet = {
                "id": f"PKT-{packet_id}",
                "packet_count": random.randint(8000, 20000),
                "packet_size": random.choice([64, 128, 512]),
                "entropy": round(random.uniform(0.1, 2.5), 2)
            }
        else:
            packet = {
                "id": f"PKT-{packet_id}",
                "packet_count": random.randint(100, 1500),
                "packet_size": random.randint(64, 1500),
                "entropy": round(random.uniform(3.0, 7.8), 2)
            }
        
        traffic_queue.append(packet) 
        await asyncio.sleep(2) 

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(process_traffic_queue())
    asyncio.create_task(ingest_traffic_simulator())

@app.get("/api/results")
def get_results():
    return {"data": list(reversed(analyzed_results))[:20]}

class ManualData(BaseModel):
    packet_count: int
    packet_size: int
    entropy: float

@app.post("/api/manual")
def manual_analysis(data: ManualData):
    if not model:
        return {"error": "Model not loaded"}
    
    features = [[data.packet_count, data.packet_size, data.entropy]]
    pred = model.predict(features)[0]
    
    if pred == 1:
        status = "MALICIOUS THREAT DETECTED"
        what = "A Volumetric DDoS Attack pattern has been identified."
        
        why_parts = []
        if data.packet_count > 5000:
            why_parts.append(f"The packet count ({data.packet_count}/s) violently exceeds the baseline limits.")
        else:
            why_parts.append(f"Although count ({data.packet_count}/s) is normal, other parameters triggered defensive protocols.")
            
        if data.packet_size in [64, 128, 512]:
             why_parts.append(f"The packet size is rigidly fixed at {data.packet_size} Bytes, indicating an automated flood tool rather than a human browser.")
        else:
             why_parts.append(f"The size ({data.packet_size} Bytes) exhibits irregular variance.")
             
        if data.entropy < 3.0:
            why_parts.append(f"The exceptionally low entropy ({data.entropy}) proves the payload is highly repetitive and contains no real encrypted data—the signature of a DDoS attack.")
        else:
            why_parts.append(f"The entropy ({data.entropy}) combined with other anomalies resembles an encrypted traffic flood.")
            
        why = " ".join(why_parts)
        
        how = "The NDSS Machine Learning (Random Forest) engine analyzed the input dimensions against pre-trained mathematical boundaries and confidently flagged this specific flow as an imminent threat."
        
        final_reason = f"<div class='exp-block exp-what'><b>WHAT:</b> {what}</div><div class='exp-block exp-why'><b>WHY:</b> {why}</div><div class='exp-block exp-how'><b>HOW:</b> {how}</div>"
        
    else:
        status = "SAFE (NORMAL TRAFFIC)"
        what = "Legitimate Network Traffic flow has been identified."
        
        why_parts = []
        why_parts.append(f"The packet count ({data.packet_count}/s) is within standard operational volume.")
        why_parts.append(f"The {data.packet_size} Byte size indicates natural, variable data transfer typical of web browsing or standard communication.")
        why_parts.append(f"The entropy value ({data.entropy}) reflects the complex randomness expected in healthy, encrypted applications.")
        
        why = " ".join(why_parts)
        how = "The internal AI decision-tree structure validated all network parameters strictly within the bounds of natural and safe data flow models."
        
        final_reason = f"<div class='exp-block exp-what'><b>WHAT:</b> {what}</div><div class='exp-block exp-why'><b>WHY:</b> {why}</div><div class='exp-block exp-how'><b>HOW:</b> {how}</div>"
        
    return {
        "status": status,
        "detailed_explanation": final_reason
    }

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/")
def read_index():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))
