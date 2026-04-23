# API Endpoints
from fastapi import APIRouter, HTTPException
from app.services.analyzer_service import analyze_user 

router = APIRouter() 

@router.get("/analyze/{username}")
def analyze(username: str): 
    result = analyze_user(username) 

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result