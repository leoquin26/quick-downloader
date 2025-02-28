from sqlalchemy import Column, Integer, String, Float, UniqueConstraint
from app.database import Base

class RatingModel(Base):
    __tablename__ = "ratings"
    id = Column(Integer, primary_key=True, index=True)
    user_session = Column(String, index=True)  # Identificador único para usuarios
    download_type = Column(String, index=True)  # youtube, tiktok, soundcloud, etc.
    rating = Column(Float, nullable=False)  # Calificación (1-5 estrellas)
    
    __table_args__ = (UniqueConstraint("user_session", "download_type", name="_user_download_uc"),)
