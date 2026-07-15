from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from uuid import uuid4
import re

router = APIRouter()

class ScanRequest(BaseModel):
    url: str

class ScanResponse(BaseModel):
    scan_id: str
    url: str
    status: str

def is_valid_url(url: str) -> bool:
    regex = re.compile(
        r'^(?:http|https)://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

@router.post("/api/scan", response_model=ScanResponse)
async def request_scan(request: ScanRequest):
    if not is_valid_url(request.url):
        raise HTTPException(status_code=400, detail="Invalid URL format. Please ensure it starts with http:// or https://")

    scan_id = str(uuid4())
    clean_url = request.url.rstrip("/")
    
    return ScanResponse(
        scan_id=scan_id,
        url=clean_url,
        status="queued"
    )
