from fastapi import APIRouter
from Controller.LoginController import router as login_router
from Controller.RegistrasiController import router as registrasi_router

router = APIRouter()
router.include_router(login_router, prefix="/api")
router.include_router(registrasi_router, prefix="/api")
