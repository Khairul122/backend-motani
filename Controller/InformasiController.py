from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import shutil
import os
from datetime import datetime

from conn import SessionLocal
from Model.InformasiModel import Informasi
from Model.KalenderPanenModel import KalenderPanen
from Model.PrediksiPermintaanModel import PrediksiPermintaan
from Schema.InformasiSchema import InformasiSchema
from Schema.KalenderPanenSchema import KalenderPanenSchema, KalenderPanenCreateSchema
from Schema.PrediksiPermintaanSchema import PrediksiPermintaanSchema, PrediksiPermintaanCreateSchema
from sqlalchemy.orm import joinedload

router = APIRouter()

UPLOAD_DIR = "uploads/informasi"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/informasi/", response_model=List[InformasiSchema])
def get_all_informasi(db: Session = Depends(get_db)):
    return db.query(Informasi).all()

@router.get("/informasi/{id_informasi}", response_model=InformasiSchema)
def get_informasi_by_id(id_informasi: int, db: Session = Depends(get_db)):
    # Gunakan join atau options untuk memuat relasi
    informasi = db.query(Informasi).options(
        joinedload(Informasi.kalender_panen),
        joinedload(Informasi.prediksi_permintaan)
    ).filter(Informasi.id_informasi == id_informasi).first()
    
    if not informasi:
        raise HTTPException(status_code=404, detail="Informasi not found")
    
    return informasi

@router.post("/informasi/", response_model=InformasiSchema)
def create_informasi(
    judul: str = Form(...),
    ket: Optional[str] = Form(None),
    tgl_post: str = Form(...),
    foto: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    foto_path = os.path.join(UPLOAD_DIR, foto.filename)
    with open(foto_path, "wb") as f:
        shutil.copyfileobj(foto.file, f)

    informasi = Informasi(
        judul=judul,
        ket=ket,
        tgl_post=tgl_post,
        foto=foto.filename
    )
    db.add(informasi)
    db.commit()
    db.refresh(informasi)
    return informasi

@router.put("/informasi/{id_informasi}", response_model=InformasiSchema)
def update_informasi(
    id_informasi: int,
    judul: str = Form(...),
    ket: Optional[str] = Form(None),
    tgl_post: str = Form(...),
    foto: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    informasi = db.query(Informasi).filter(Informasi.id_informasi == id_informasi).first()
    if not informasi:
        raise HTTPException(status_code=404, detail="Informasi not found")

    informasi.judul = judul
    informasi.ket = ket
    informasi.tgl_post = tgl_post

    if foto:
        if informasi.foto:
            old_path = os.path.join(UPLOAD_DIR, informasi.foto)
            if os.path.exists(old_path):
                os.remove(old_path)
        new_path = os.path.join(UPLOAD_DIR, foto.filename)
        with open(new_path, "wb") as f:
            shutil.copyfileobj(foto.file, f)
        informasi.foto = foto.filename

    db.commit()
    db.refresh(informasi)
    return informasi

@router.delete("/informasi/{id_informasi}")
def delete_informasi(id_informasi: int, db: Session = Depends(get_db)):
    informasi = db.query(Informasi).filter(Informasi.id_informasi == id_informasi).first()
    if not informasi:
        raise HTTPException(status_code=404, detail="Informasi not found")

    if informasi.foto:
        foto_path = os.path.join(UPLOAD_DIR, informasi.foto)
        if os.path.exists(foto_path):
            os.remove(foto_path)

    db.query(KalenderPanen).filter(KalenderPanen.id_informasi == id_informasi).delete()
    db.query(PrediksiPermintaan).filter(PrediksiPermintaan.id_informasi == id_informasi).delete()
    db.delete(informasi)
    db.commit()
    return {"detail": f"Informasi dengan ID {id_informasi} dan relasinya berhasil dihapus"}

from fastapi.responses import FileResponse

@router.get("/informasi/foto/{filename}")
def get_foto(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path=file_path)

@router.get("/kalender-panen/", response_model=List[KalenderPanenSchema])
def get_all_kalender_panen(db: Session = Depends(get_db)):
    return db.query(KalenderPanen).all()

@router.get("/kalender-panen/{id_kalender}", response_model=KalenderPanenSchema)
def get_kalender_panen_by_id(id_kalender: int, db: Session = Depends(get_db)):
    kalender = db.query(KalenderPanen).filter(KalenderPanen.id_kalender == id_kalender).first()
    if not kalender:
        raise HTTPException(status_code=404, detail="Kalender panen not found")
    return kalender

@router.post("/kalender-panen/", response_model=KalenderPanenSchema)
def create_kalender_panen(
    id_informasi: int = Form(...),
    wilayah: str = Form(...),
    awal_panen: str = Form(...),
    akhir_panen: str = Form(...),
    catatan: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    informasi = db.query(Informasi).filter(Informasi.id_informasi == id_informasi).first()
    if not informasi:
        raise HTTPException(status_code=404, detail="Informasi not found")
    
    kalender = KalenderPanen(
        id_informasi=id_informasi,
        wilayah=wilayah,
        awal_panen=awal_panen,
        akhir_panen=akhir_panen,
        catatan=catatan
    )
    db.add(kalender)
    db.commit()
    db.refresh(kalender)
    return kalender

@router.put("/kalender-panen/{id_kalender}", response_model=KalenderPanenSchema)
def update_kalender_panen(
    id_kalender: int,
    id_informasi: int = Form(...),
    wilayah: str = Form(...),
    awal_panen: str = Form(...),
    akhir_panen: str = Form(...),
    catatan: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    kalender = db.query(KalenderPanen).filter(KalenderPanen.id_kalender == id_kalender).first()
    if not kalender:
        raise HTTPException(status_code=404, detail="Kalender panen not found")
    
    informasi = db.query(Informasi).filter(Informasi.id_informasi == id_informasi).first()
    if not informasi:
        raise HTTPException(status_code=404, detail="Informasi not found")
    
    kalender.id_informasi = id_informasi
    kalender.wilayah = wilayah
    kalender.awal_panen = awal_panen
    kalender.akhir_panen = akhir_panen
    kalender.catatan = catatan
    
    db.commit()
    db.refresh(kalender)
    return kalender

@router.delete("/kalender-panen/{id_kalender}")
def delete_kalender_panen(id_kalender: int, db: Session = Depends(get_db)):
    kalender = db.query(KalenderPanen).filter(KalenderPanen.id_kalender == id_kalender).first()
    if not kalender:
        raise HTTPException(status_code=404, detail="Kalender panen not found")
    
    db.delete(kalender)
    db.commit()
    return {"detail": f"Kalender panen dengan ID {id_kalender} berhasil dihapus"}

@router.get("/prediksi-permintaan/", response_model=List[PrediksiPermintaanSchema])
def get_all_prediksi_permintaan(db: Session = Depends(get_db)):
    return db.query(PrediksiPermintaan).all()

@router.get("/prediksi-permintaan/{id_prediksi}", response_model=PrediksiPermintaanSchema)
def get_prediksi_permintaan_by_id(id_prediksi: int, db: Session = Depends(get_db)):
    prediksi = db.query(PrediksiPermintaan).filter(PrediksiPermintaan.id_prediksi == id_prediksi).first()
    if not prediksi:
        raise HTTPException(status_code=404, detail="Prediksi permintaan not found")
    return prediksi

@router.post("/prediksi-permintaan/", response_model=PrediksiPermintaanSchema)
def create_prediksi_permintaan(
    id_informasi: int = Form(...),
    wilayah: str = Form(...),
    periode: str = Form(...),
    deskripsi: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    # Verifikasi informasi ada
    informasi = db.query(Informasi).filter(Informasi.id_informasi == id_informasi).first()
    if not informasi:
        raise HTTPException(status_code=404, detail="Informasi not found")
    
    prediksi = PrediksiPermintaan(
        id_informasi=id_informasi,
        wilayah=wilayah,
        periode=periode,
        deskripsi=deskripsi
    )
    db.add(prediksi)
    db.commit()
    db.refresh(prediksi)
    return prediksi

@router.put("/prediksi-permintaan/{id_prediksi}", response_model=PrediksiPermintaanSchema)
def update_prediksi_permintaan(
    id_prediksi: int,
    id_informasi: int = Form(...),
    wilayah: str = Form(...),
    periode: str = Form(...),
    deskripsi: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    prediksi = db.query(PrediksiPermintaan).filter(PrediksiPermintaan.id_prediksi == id_prediksi).first()
    if not prediksi:
        raise HTTPException(status_code=404, detail="Prediksi permintaan not found")
    
    # Verifikasi informasi ada
    informasi = db.query(Informasi).filter(Informasi.id_informasi == id_informasi).first()
    if not informasi:
        raise HTTPException(status_code=404, detail="Informasi not found")
    
    prediksi.id_informasi = id_informasi
    prediksi.wilayah = wilayah
    prediksi.periode = periode
    prediksi.deskripsi = deskripsi
    
    db.commit()
    db.refresh(prediksi)
    return prediksi

@router.delete("/prediksi-permintaan/{id_prediksi}")
def delete_prediksi_permintaan(id_prediksi: int, db: Session = Depends(get_db)):
    prediksi = db.query(PrediksiPermintaan).filter(PrediksiPermintaan.id_prediksi == id_prediksi).first()
    if not prediksi:
        raise HTTPException(status_code=404, detail="Prediksi permintaan not found")
    
    db.delete(prediksi)
    db.commit()
    return {"detail": f"Prediksi permintaan dengan ID {id_prediksi} berhasil dihapus"}