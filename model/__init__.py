from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
 
import os

from .base_model import Base
from model.bookmark_model import Bookmark

from config import DATABASE_PATH, SQLALCHEMY_DATABASE_URL

# Certifique-se que o diretório existe
os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)



engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(engine)

