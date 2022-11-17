from config import SQLALCHEMY_DATABASE_URI
from app import db
import os.path


try:
    db.create_all()
except Exception:
    print("Already Created")