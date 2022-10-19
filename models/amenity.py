#!/usr/bin/python3
""" State Module for HBNB project """
import models
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String
from os import getenv
from sqlalchemy.orm import relationship

class Amenity(BaseModel, Base):
    """ DBStorage - Amenity"""
    
    __tablename__ = 'amenities'
    name = Column(String(128), nullable=False)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        place_amenities = relationship('Place',
                                       secondary='place_amenity',
                                       back_populates='amenities')
