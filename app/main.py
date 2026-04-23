# Entry point (FastAPI)
from fastapi import FastAPI
from app.routes.analyzer import router as analyzer_router

app = FastAPI()
app.include_router(analyzer_router)