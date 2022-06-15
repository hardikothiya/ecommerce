from sqlalchemy import Column, Integer, String

from database import Base


# User Database Model
class UserInfo(Base):
    __tablename__ = "user_info"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), unique=True)
    username = Column(String(50))
    password = Column(String(256))
    fullname = Column(String(50))


# Items Databse Model
class ItemInfo(Base):
    __tablename__ = "item_info"

    id = Column(Integer, primary_key=True, index=True)
    itemname = Column(String(50), unique=True)
    itemprice = Column(Integer)
    itemimage = Column(String(256), unique=True)

    class Config:
        orm_mode = True


# User Cart Database Model
class CartInfo(Base):
    __tablename__ = "cart_info"

    id = Column(Integer, primary_key=True, index=True)
    ownername = Column(Integer, unique=True)
    itemname = Column(String(50), unique=True)
    itemprice = Column(Integer)
