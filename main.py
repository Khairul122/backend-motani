# app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Controller.LoginController import router as LoginController

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.get("/")
def root():
    return {"message": "SPK WSM"}

app.include_router(LoginController, prefix="/controller")
