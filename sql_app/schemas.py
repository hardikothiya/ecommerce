from pydantic import BaseModel


# base schema for user data
class UserInfoBase(BaseModel):
    email: str
    username: str
    fullname: str
    mobile: int

    class Config:
        orm_mode = True


# schema for user creation(registration)
class UserCreate(UserInfoBase):
    password: str

    class Config:
        orm_mode = True


# inherits from user data schema
class UserInfo(UserInfoBase):
    id: int

    class Config:
        orm_mode = True


class UserAddress(BaseModel):
    user_id = int
    address_line1: str
    address_line2: str
    postal_code: int
    mobile_number: int
    city: str
    state: str

    class Config:
        orm_mode = True


# base schema for user login
class UserLogin(BaseModel):
    email: str
    password: str


# base schema for items
class ItemInfo(BaseModel):
    itemname: str
    description: str
    itemprice: int
    itemimage: str
    category_id: int
    discount_id: int


class ItemCategory(BaseModel):
    category_name: str

    class Config:
        orm_mode = True


class ItemInventory(BaseModel):
    item_id: int
    inventory_quantity: int

    class Config:
        orm_mode = True


class ItemDiscount(BaseModel):
    discount_percentage: int
    description: str
    active: bool


# inherits from item data schema used for getting item by id
class ItemAInfo(ItemInfo):
    id: int

    class Config:
        orm_mode = True


# base schema for relating a cart to it's user


class CartCreate(BaseModel):
    product_id: int
    quantity: int


class CartInfo(ItemInfo):
    user_id: int

    class Config:
        orm_mode = True


class OrderInfo(BaseModel):
    user_id: int
    product_id: int
    quantity: int
    order_date: str
    order_status: str
    order_total: int

    class Config:
        orm_mode = True


# base schema for the payment api
class UserPayment(BaseModel):
    mobile: int
    total: int
