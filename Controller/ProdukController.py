from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form, Request
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import shutil, os
from sqlalchemy.orm import joinedload
from conn import SessionLocal
from Model.ProdukModel import Produk, ProdukFoto
from Schema.ProdukSchema import ProdukSchema

router = APIRouter()

UPLOAD_DIR = "uploads/produk"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/produk/view_image/{filename}")
def view_image(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)

@router.get("/produk/", response_model=List[ProdukSchema])
def get_all_produk(db: Session = Depends(get_db)):
    return db.query(Produk).options(joinedload(Produk.produk_foto)).all()

@router.get("/produk/{id}", response_model=ProdukSchema)
def get_produk_by_id(id: int, db: Session = Depends(get_db)):
    produk = db.query(Produk).options(joinedload(Produk.produk_foto)).filter(Produk.id_produk == id).first()
    if not produk:
        raise HTTPException(status_code=404, detail="Produk not found")
    return produk

@router.post("/produk/", response_model=ProdukSchema)
async def create_produk(
    nama_produk: str = Form(...),
    keterangan: Optional[str] = Form(None),
    stok: int = Form(...),
    deskripsi: Optional[str] = Form(None),
    status_produk: Optional[str] = Form("aktif"),
    id_logistik: int = Form(...),
    harga: float = Form(...),
    diskon: float = Form(0.00),
    foto: UploadFile = File(...),
    additional_photos: Optional[List[UploadFile]] = File(None),
    db: Session = Depends(get_db)
):
    if not foto or not foto.filename:
        raise HTTPException(status_code=422, detail="Foto utama produk harus diupload")

    produk = Produk(
        nama_produk=nama_produk,
        keterangan=keterangan,
        stok=stok,
        deskripsi=deskripsi,
        status_produk=status_produk,
        id_logistik=id_logistik,
        harga=harga,
        diskon=diskon
    )
    db.add(produk)
    db.commit()
    db.refresh(produk)

    filename = f"{produk.id_produk}_{foto.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(foto.file, buffer)

    foto_entry = ProdukFoto(id_produk=produk.id_produk, url_foto=filename)
    db.add(foto_entry)

    if additional_photos:
        for idx, add_photo in enumerate(additional_photos):
            if add_photo and add_photo.filename:
                add_filename = f"{produk.id_produk}_additional_{idx}_{add_photo.filename}"
                add_file_path = os.path.join(UPLOAD_DIR, add_filename)
                with open(add_file_path, "wb") as buffer:
                    shutil.copyfileobj(add_photo.file, buffer)
                add_foto_entry = ProdukFoto(id_produk=produk.id_produk, url_foto=add_filename)
                db.add(add_foto_entry)

    db.commit()
    db.refresh(produk)
    return produk

@router.put("/produk/{id}", response_model=ProdukSchema)
async def update_produk(
    id: int,
    nama_produk: str = Form(...),
    keterangan: Optional[str] = Form(None),
    stok: int = Form(...),
    deskripsi: Optional[str] = Form(None),
    status_produk: Optional[str] = Form("aktif"),
    id_logistik: int = Form(...),
    harga: float = Form(...),
    diskon: float = Form(0.00),
    foto: Optional[UploadFile] = File(None),
    additional_photos: Optional[List[UploadFile]] = File(None),
    db: Session = Depends(get_db)
):
    produk = db.query(Produk).filter(Produk.id_produk == id).first()
    if not produk:
        raise HTTPException(status_code=404, detail="Produk not found")

    for attr, value in {
        "nama_produk": nama_produk,
        "keterangan": keterangan,
        "stok": stok,
        "deskripsi": deskripsi,
        "status_produk": status_produk,
        "id_logistik": id_logistik,
        "harga": harga,
        "diskon": diskon
    }.items():
        setattr(produk, attr, value)

    if foto and foto.filename:
        foto_utama = db.query(ProdukFoto).filter(ProdukFoto.id_produk == id).first()
        if foto_utama:
            old_path = os.path.join(UPLOAD_DIR, foto_utama.url_foto)
            if os.path.exists(old_path):
                os.remove(old_path)
            db.delete(foto_utama)

        filename = f"{id}_{foto.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(foto.file, buffer)

        foto_entry = ProdukFoto(id_produk=id, url_foto=filename)
        db.add(foto_entry)

    if additional_photos:
        for idx, add_photo in enumerate(additional_photos):
            if add_photo and add_photo.filename:
                add_filename = f"{id}_additional_{idx}_{add_photo.filename}"
                add_file_path = os.path.join(UPLOAD_DIR, add_filename)
                with open(add_file_path, "wb") as buffer:
                    shutil.copyfileobj(add_photo.file, buffer)
                add_foto_entry = ProdukFoto(id_produk=id, url_foto=add_filename)
                db.add(add_foto_entry)

    db.commit()
    db.refresh(produk)
    return produk

@router.delete("/produk/{id}")
def delete_produk(id: int, db: Session = Depends(get_db)):
    produk = db.query(Produk).filter(Produk.id_produk == id).first()
    if not produk:
        raise HTTPException(status_code=404, detail="Produk not found")

    fotos = db.query(ProdukFoto).filter(ProdukFoto.id_produk == id).all()
    for foto in fotos:
        file_path = os.path.join(UPLOAD_DIR, foto.url_foto)
        if os.path.exists(file_path):
            os.remove(file_path)
        db.delete(foto)

    db.delete(produk)
    db.commit()

    return {"detail": f"Produk dan semua fotonya dengan ID {id} berhasil dihapus"}

@router.delete("/produk/{id}/foto/{foto_id}")
def delete_produk_foto(id: int, foto_id: int, db: Session = Depends(get_db)):
    foto = db.query(ProdukFoto).filter(
        ProdukFoto.id_produk == id,
        ProdukFoto.id_foto == foto_id
    ).first()
    
    if not foto:
        raise HTTPException(status_code=404, detail="Foto produk tidak ditemukan")
    
    file_path = os.path.join(UPLOAD_DIR, foto.url_foto)
    if os.path.exists(file_path):
        os.remove(file_path)
    
    db.delete(foto)
    db.commit()
    
    return {"detail": f"Foto dengan ID {foto_id} untuk produk ID {id} berhasil dihapus"}
