from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Api.Route import router as api_router
from conn import db_config
import mysql.connector
from mysql.connector import Error
from fastapi.exceptions import HTTPException

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
    return {"message": "Backend Aplikasi Motani"}

@app.get("/cek")
def cek_koneksi():
    try:
        connection = mysql.connector.connect(
            host=db_config["host"],
            user=db_config["user"],
            password=db_config["password"],
            database=db_config["database"]
        )
        if connection.is_connected():
            return {"message": "Koneksi ke database berhasil!"}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    finally:
        if connection.is_connected():
            connection.close()

app.include_router(api_router, prefix="/api")
