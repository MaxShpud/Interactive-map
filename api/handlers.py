from fastapi import APIRouter, Depends, HTTPException

app_router = APIRouter()

@app_router.get("")
async def root():
    return {"message": "Interactive Map"}