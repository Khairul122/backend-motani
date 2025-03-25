from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
from mysql.connector import Error
from Controller.LoginController import router as LoginController
from conn import db_config  # Impor kredensial dari conn.py

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

# Route untuk cek koneksi ke database
@app.get("/cek")
def cek_koneksi():
    try:
        # Menggunakan kredensial yang diimpor dari conn.py
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

# Menambahkan route LoginController
app.include_router(LoginController, prefix="/controller")
