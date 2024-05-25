mport os
from models.base_model import BaseModel, Base

storage_type = os.environ.get('HBNB_TYPE_STORAGE')

if storage_type == "db":
    from sqlalchemy.orm import relationship
    from sqlalchemy import Column, Integer, String, Float
    from sqlalchemy.orm import backref

    class Amenity(BaseModel, Base):
        """Amenity class handles all application amenities"""
        __tablename__ = 'amenities'
        name = Column(String(128), nullable=False)
        place_amenities = relationship("Place", secondary="place_amenity")
else:
    class Amenity(BaseModel):
        """Amenity class handles all application amenities"""
        name = ''
