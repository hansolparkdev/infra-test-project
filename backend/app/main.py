from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="My API", version="0.1.0")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터를 만들고 prefix 적용
router = APIRouter(prefix="/api")

@router.get("/health")
def health():
    return {"status": "ok", "env": os.getenv("ENVIRONMENT", "dev")}

@router.get("/")
def root():
    return {"message": "Hello World"}
