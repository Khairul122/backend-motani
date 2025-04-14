from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from conn import SessionLocal
from Model.ProduksiModel import Produksi
from Model.ProdukModel import Produk
from Model.LogStokModel import LogStok
from Schema.ProduksiSchema import ProduksiSchema, ProduksiCreateSchema

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/produksi/", response_model=List[ProduksiSchema])
def get_all_produksi(db: Session = Depends(get_db)):
    return db.query(Produksi).all()

@router.get("/produksi/{id}", response_model=ProduksiSchema)
def get_produksi_by_id(id: int, db: Session = Depends(get_db)):
    produksi = db.query(Produksi).filter(Produksi.id_produksi == id).first()
    if not produksi:
        raise HTTPException(status_code=404, detail="Data produksi tidak ditemukan")
    return produksi

@router.post("/produksi/", response_model=ProduksiSchema)
def create_produksi(data: ProduksiCreateSchema, db: Session = Depends(get_db)):
    produksi = Produksi(**data.dict())
    db.add(produksi)

    produk = db.query(Produk).filter(Produk.id_produk == data.id_produk).first()
    if not produk:
        raise HTTPException(status_code=404, detail="Produk tidak ditemukan")

    produk.stok += data.jumlah

    log = LogStok(id_produk=data.id_produk, aksi="INSERT_PRODUKSI", perubahan=data.jumlah)
    db.add(log)

    db.commit()
    db.refresh(produksi)
    return produksi

@router.put("/produksi/{id}", response_model=ProduksiSchema)
def update_produksi(id: int, data: ProduksiCreateSchema, db: Session = Depends(get_db)):
    produksi = db.query(Produksi).filter(Produksi.id_produksi == id).first()
    if not produksi:
        raise HTTPException(status_code=404, detail="Data produksi tidak ditemukan")

    jumlah_lama = produksi.jumlah
    for field, value in data.dict().items():
        setattr(produksi, field, value)

    produk = db.query(Produk).filter(Produk.id_produk == produksi.id_produk).first()
    if produk:
        selisih = data.jumlah - jumlah_lama
        produk.stok += selisih
        db.add(LogStok(id_produk=produksi.id_produk, aksi="UPDATE_PRODUKSI", perubahan=selisih))

    db.commit()
    db.refresh(produksi)
    return produksi

@router.delete("/produksi/{id}")
def delete_produksi(id: int, db: Session = Depends(get_db)):
    produksi = db.query(Produksi).filter(Produksi.id_produksi == id).first()
    if not produksi:
        raise HTTPException(status_code=404, detail="Data produksi tidak ditemukan")

    produk = db.query(Produk).filter(Produk.id_produk == produksi.id_produk).first()
    if produk:
        produk.stok -= produksi.jumlah
        db.add(LogStok(id_produk=produksi.id_produk, aksi="DELETE_PRODUKSI", perubahan=-produksi.jumlah))

    db.delete(produksi)
    db.commit()
    return {"detail": "Data produksi berhasil dihapus"}
