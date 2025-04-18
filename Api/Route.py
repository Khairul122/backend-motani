from fastapi import APIRouter
from Controller.LoginController import router as login_router
from Controller.RegistrasiController import router as registrasi_router
from Controller.PembeliController import router as pembeli_router
from Controller.UserController import router as user_router
from Controller.InformasiController import router as informasi_router
from Controller.ProdukController import router as produk_router
from Controller.LogistikController import router as logistik_router
from Controller.ProduksiController import router as produksi_router

router = APIRouter()

router.include_router(login_router, prefix="/api")
router.include_router(registrasi_router, prefix="/api")
router.include_router(pembeli_router, prefix="/api")
router.include_router(user_router, prefix="/api")
router.include_router(informasi_router, prefix="/api")
router.include_router(produk_router, prefix="/api")
router.include_router(logistik_router, prefix="/api")
router.include_router(produksi_router, prefix="/api")