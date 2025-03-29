from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Api.Route import router as api_router
import mysql.connector
from mysql.connector import Error
from conn import DB_CONFIG
from fastapi import HTTPException


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
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"]
        )
        if connection.is_connected():
            return {"message": "Koneksi ke database berhasil!"}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    finally:
        if connection.is_connected():
            connection.close()

app.include_router(api_router)
