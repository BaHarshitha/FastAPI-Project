from sqlalchemy import Boolean,Integer,String,ForeignKey,Column
from sqlalchemy.orm import relationship
# from database import Base
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True)
    email = Column(String, unique=True,index=True)
    hashed_password = Column(String,index=True)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer,ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")
