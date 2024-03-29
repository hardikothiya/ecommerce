from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, BigInteger
from sql_app.database import Base


# User Database Model
class UserInfo(Base):
    __tablename__ = "user_info"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), unique=True)
    mobile = Column(BigInteger)
    username = Column(String(50))
    password = Column(String(256))
    fullname = Column(String(50))


# user address Model
class UserAddress(Base):
    __tablename__ = "user_address"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True)
    address_line1 = Column(String(100))
    address_line2 = Column(String(100))
    postal_code = Column(Integer)
    mobile_number = Column(BigInteger)
    city = Column(String(50))
    state = Column(String(50))


# Items Databse Model
class ItemInfo(Base):
    __tablename__ = "item_info"

    id = Column(Integer, primary_key=True, index=True)
    itemname = Column(String(50), nullable=False)
    itemprice = Column(Integer, nullable=False)
    description = Column(String(100), nullable=False)
    itemimage = Column(String(256), unique=True, nullable=False)
    category_id = Column(Integer, ForeignKey("item_category.id"), nullable=False)
    inventory_id = Column(Integer, index=True, default=id)
    discount_id = Column(Integer, ForeignKey("item_discount.id"))

    class Config:
        orm_mode = True


# item category Model
class ItemCategory(Base):
    __tablename__ = "item_category"

    id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(50), unique=True, nullable=False, default="general")

    class Config:
        orm_mode = True


# item inventory Model
class ItemInventory(Base):
    __tablename__ = "item_inventory"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("item_info.id"), nullable=False, )
    inventory_quantity = Column(Integer, nullable=False)

    class Config:
        orm_mode = True

    # User Cart Database Model


# item discount Model
class ItemDiscount(Base):
    __tablename__ = "item_discount"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(100))
    discount_percentage = Column(Integer, nullable=False)
    active = Column(Boolean, nullable=False)


# Cart/Order Database Model
class CartInfo(Base):
    __tablename__ = "cart_info"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_info.id"))
    product_id = Column(Integer, ForeignKey('item_info.id'))
    quantity = Column(Integer, nullable=False, default=1)
    item_amount = Column(Integer, nullable=False)


# Cart/Order Database Model
class OrderDetails(Base):
    __tablename__ = "order_details"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_info.id"))
    quantity = Column(Integer, nullable=False, default=1)
    order_id = Column(Integer, index=True)
    bill_amount = Column(Integer, nullable=False)
    payment_id = Column(Integer, index=True)


# Payment Database Model
class PaymentInfo(Base):
    __tablename__ = "payment_info"

    id = Column(Integer, primary_key=True, index=True)
    paymentId = Column(Integer, ForeignKey("order_details.id"))
    orderId = Column(Integer)
    user_id = Column(Integer, ForeignKey("user_info.id"))
    status = Column(String(50))
    created_at = Column(String(50))
