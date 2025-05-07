import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/library_db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False