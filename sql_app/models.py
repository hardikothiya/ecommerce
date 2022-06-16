from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from fastapi.param_functions import Form, Body
from database import Base


# User Database Model
class UserInfo(Base):
    __tablename__ = "user_info"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), unique=True)
    mobile = Column(String(50))
    username = Column(String(50))
    password = Column(String(256))
    fullname = Column(String(50))


# user address Model
class UserAddress(Base):
    __tablename__ = "user_address"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_info.id"))
    address_line1 = Column(String(100))
    address_line2 = Column(String(100))
    postal_code = Column(Integer)
    mobile_number = Column(Integer)
    city = Column(String(50))
    state = Column(String(50))


# Items Databse Model
class ItemInfo(Base):
    __tablename__ = "item_info"

    id = Column(Integer, primary_key=True, index=True)
    itemname = Column(String(50), unique=True)
    itemprice = Column(Integer)
    description = Column(String(100))
    itemimage = Column(String(256), unique=True)
    category_id = Column(Integer, ForeignKey("item_category.id"))
    inventory_id = Column(Integer, ForeignKey("item_inventory.id"))
    discount_id = Column(Integer, ForeignKey("item_discount.id"))

    class Config:
        orm_mode = True


# item category Model
class ItemCategory(Base):
    __tablename__ = "item_category"

    id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(50), unique=True)

    class Config:
        orm_mode = True


# item inventory Model
class ItemInventory(Base):
    __tablename__ = "item_inventory"

    id = Column(Integer, primary_key=True, index=True)
    inventory_id = Column(Integer)
    inventory_quantity = Column(Integer)

    class Config:
        orm_mode = True

    # User Cart Database Model


# item discount Model
class ItemDiscount(Base):
    __tablename__ = "item_discount"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(100))
    discount_percentage = Column(Integer)
    active = Column(Boolean)


# Cart/Order Database Model
class CartInfo(ItemInfo):
    __tablename__ = "cart_info"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_info.id"))
    product_id = Column(Integer, ForeignKey('item_info.id'))
    quantity = Column(Integer)


# Cart/Order Database Model
class OrderDetails(Base):
    __tablename__ = "order_details"

    id = Column(Integer, ForeignKey("cart_info.id"))
    user_id = Column(Integer, ForeignKey("user_info.id"))
    quantity = Column(Integer)
    order_id = Column(Integer, primary_key = True ,index=True)
    total = Column(Integer)
    payment_id = Column(Integer, index=True)


# Payment Database Model
class PaymentInfo(Base):
    __tablename__ = "payment_info"

    id = Column(Integer, primary_key=True, index=True)
    payment_id = Column(Integer, ForeignKey("order_details.payment_id"))
    order_id = Column(Integer, ForeignKey("order_details.order_id"))
    user_id = Column(Integer, ForeignKey("user_info.id"))
    status = Column(String(50))
    created_at = Column(String(50))
