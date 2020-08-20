import os.path
from database import DataBase


DATABASE = DataBase()
DATABASE.setup_db()

os.makedirs("files", exist_ok=True)
