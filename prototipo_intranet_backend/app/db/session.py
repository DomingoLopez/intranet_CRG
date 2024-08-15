from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Carga las variables de entorno desde el archivo .env
load_dotenv()

DB_HOST=os.getenv("DB_HOST")
DB_PORT=os.getenv("DB_PORT")
DB_USER=os.getenv("DB_USER")
DB_PASSWD=os.getenv("DB_PASSWD")

SQLALCHEMY_DATABASE_URL = f'ibm_db_sa://{DB_USER}:{DB_PASSWD}@{DB_HOST}:{DB_PORT}/INSTANCIA'


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Dependencia de sesion de la BBDD, estoy hay que ponerlo fuera, aqui no pinta
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
