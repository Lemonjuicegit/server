import asyncio
from fastapi import  APIRouter
from pydantic import BaseModel

router = APIRouter()

class Args(BaseModel):
    pass



@router.get("/run_onlineMediators")
def run_onlineMediators():
    pass