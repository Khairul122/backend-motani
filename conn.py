from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_config = {
    "host": "bpzpmitofd6n28nnuyf5-mysql.services.clever-cloud.com",
    "user": "udcsfrft0pwkg8sr",
    "password": "6T4almdEdFh9ngGclyCi",
    "database": "bpzpmitofd6n28nnuyf5",
    "port": 3306
}

DATABASE_URL = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"

engine = create_engine(DATABASE_URL, connect_args={"charset": "utf8mb4"})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
