import fastapi
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from .models import Server, Metric
from .database import get_db

router = APIRouter()

@router.get("/health")
async def health_check():
    """
    Health check endpoint to verify if the API is running.
    """
    return JSONResponse(content={"status": "healthy"}, status_code=200)

@router.post("/data")
async def post_data(payload: list[dict], db: Session = Depends(get_db)):
    """
    Endpoint to handle data submission for multiple data points.
    """
    for data_point in payload:
        server_name = data_point.get("server_name")
        metric_name = data_point.get("metric_name")
        value = data_point.get("value")
        timestamp = data_point.get("timestamp")

        # Check if server exists, if not create it
        server = db.query(Server).filter(Server.name == server_name).first()
        if not server:
            server = Server(name=server_name, description="Auto-created server")
            db.add(server)
            db.commit()
            db.refresh(server)

        # Add metric to the server
        metric = Metric(server_id=server.id, metric_name=metric_name, value=value, timestamp=timestamp)
        db.add(metric)
        db.commit()
        db.refresh(metric)

    return JSONResponse(content={"message": "Data saved successfully"}, status_code=201)

@router.get("/data/{item_id}")
async def get_data(item_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to fetch data by item ID.
    """
    metric = db.query(Metric).filter(Metric.id == item_id).first()
    if not metric:
        return JSONResponse(content={"error": "Item not found"}, status_code=404)

    server = db.query(Server).filter(Server.id == metric.server_id).first()
    return JSONResponse(content={
        "item_id": item_id,
        "server_name": server.name,
        "metric_name": metric.metric_name,
        "value": metric.value,
        "timestamp": metric.timestamp
    }, status_code=200)

@router.get("/data")
async def get_all_data(db: Session = Depends(get_db)):
    """
    Endpoint to fetch all data.
    """
    servers = db.query(Server).all()
    data = []
    for server in servers:
        server_data = {
            "server_name": server.name,
            "description": server.description,
            "metrics": [
                {
                    "metric_name": metric.metric_name,
                    "value": metric.value,
                    "timestamp": metric.timestamp
                } for metric in server.metrics
            ]
        }
        data.append(server_data)

    return JSONResponse(content={"data": data}, status_code=200)