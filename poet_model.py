from sqlalchemy import Column, String, Boolean, TIMESTAMP
from sqlalchemy.orm import relationship
from database import Session
from datetime import datetime

class Poet(Session.session.get_base()):
    __tablename__ = 'poet'
    id = Column(String, primary_key=True)
    first_name = Column(String)
    middle_name = Column(String)
    last_name = Column(String)
    website = Column(String, nullable=True)
    address = Column(String, nullable=True)
    email = Column(String)
    phone_num = Column(String)
    city = Column(String)
    status = Column(Boolean)
    zip_code = Column(String)
    pic = Column(String, nullable=True)
    is_laureate = Column(Boolean)
    photo_credit = Column(String, nullable=True)
    state = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(TIMESTAMP, nullable=True)
    
    # Define One-to-Many relationship with PoetAndPoem entity
    poets = relationship("PoetAndPoem", back_populates="poet")

    def __init__(self, first_name=None, middle_name=None, last_name=None, 
                website=None, address=None, email=None, phone_num=None,
                city=None, status=None, zip_code=None, pic=None, is_laureate=None, photo_credit=None,
                state=None, created_at=None, updated_at=None, deleted_at=None):
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.website = website
        self.address = address
        self.email = email
        self.phone_num = phone_num
        self.city = city
        self.status = status
        self.zip_code = zip_code
        self.pic = pic
        self.is_laureate = is_laureate
        self.photo_credit = photo_credit
        self.state = state
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def __repr__(self):
        return f"<Poet(first_name='{self.first_name}', middle_name='{self.middle_name}' last_name='{self.last_name}', email='{self.email}')>"

    def to_json(self):
        return {
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "website": self.website,
            "address": self.address,
            "email": self.email,
            "phone_num": self.phone_num,
            "city": self.city,
            "status": self.status,
            "zip_code": self.zip_code,
            "pic": self.pic,
            "is_laureate": self.is_laureate,
            "photo_credit": self.photo_credit,
            "state": self.state,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at
        }
