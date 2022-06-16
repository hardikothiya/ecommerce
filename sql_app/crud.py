from sqlalchemy.orm import Session
import models, schemas
import bcrypt
import requests
from requests.auth import HTTPBasicAuth
import json
from datetime import datetime
import base64


# Get user by username function
def get_user_by_email(db: Session, user_id: int):
    a = db.query(models.UserInfo).filter(models.UserInfo.id == user_id).first()
    b = db.query(models.UserAddress).filter(models.UserAddress.user_id == user_id).first()

    return {
        'user': a,
        'address': b
    }


# User registration function
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())

    db_user = models.UserInfo(username=user.username, password=hashed_password, fullname=user.fullname,
                              email=user.email, mobile=user.mobile)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# user address function
def add_address(db: Session, user_id: int, address: schemas.UserAddress):
    user = db.query(models.UserInfo).filter(models.UserInfo.id == user_id).first()
    print(user.id)
    db_address = models.UserAddress(user_id=user.id, address_line1=address.address_line1,
                                    address_line2=address.address_line2, city=address.city,
                                    state=address.state, postal_code=address.postal_code,
                                    mobile_number=address.mobile_number)
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address


# Login Function
def get_Login(db: Session, email: str, password: str):
    db_user = db.query(models.UserInfo).filter(models.UserInfo.email == email).first()
    print(email, password)
    passw: bool = bcrypt.checkpw(password.encode('utf-8'), db_user.password.encode('utf-8'))
    return passw


# Get item by id function
def get_item_by_id(db: Session, id: int):
    # a = db.query(models.ItemInfo).filter(models.ItemInfo.id == id).first()

    a = db.query(models.ItemInfo, models.ItemCategory, models.ItemDiscount).filter(models.ItemInfo.id == id). \
        join(models.ItemCategory, models.ItemInfo.category_id == models.ItemCategory.id). \
        join(models.ItemDiscount, models.ItemInfo.discount_id == models.ItemDiscount.id).first()

    return a


def get_all_item(db: Session):
    return db.query(models.ItemInfo).all()


# Add items to DB function
def add_table(db: Session, item: schemas.ItemInfo):
    db_item = models.ItemInfo(itemname=item.itemname, itemprice=item.itemprice, itemimage=item.itemimage,
                              description=item.description, category_id=item.category_id,
                              inventory_id=item.inventory_id, discount_id=item.discount_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def add_discount(db: Session, discount: schemas.ItemDiscount):
    db_discount = models.ItemDiscount(description=discount.description,
                                      discount_percentage=discount.discount_percentage,
                                      active=discount.active)
    db.add(db_discount)
    db.commit()
    db.refresh(db_discount)
    return db_discount


def add_category(db: Session, category: schemas.ItemCategory):
    db_category = models.ItemCategory(category_name=category.category_name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def add_inventory(db: Session, inventory: schemas.ItemInventory):
    db_inventory = models.ItemInventory(inventory_quantity=inventory.inventory_quantity,
                                        inventory_id=inventory.inventory_id)
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory


# Delete item from DB by id function
def delete_item_by_id(db: Session, id: int):
    delitem = db.query(models.ItemInfo).filter(models.ItemInfo.id == id).first()
    if delitem is None:
        return
    db.delete(delitem)
    db.commit()
    return delitem


# Add to cart function
def add_to_cart(db: Session, user_id: id, cart: schemas.CartCreate):
    user = db.query(models.UserInfo).filter(models.UserInfo.id == user_id).first()
    print("cart==============>>>", cart.product_id)
    db_cart = models.CartInfo(user_id=user.id, product_id=cart.product_id, quantity=cart.quantity)
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart


def get_cart(db: Session, user_id: int):
    user = db.query(models.UserInfo).filter(models.UserInfo.id == user_id).first()
    return db.query(models.CartInfo).filter(models.CartInfo.user_id == user.id).all


# Delete item in the cart by id
def delete_cart_item_by_id(db: Session, id: int):
    delitem = db.query(models.CartInfo).filter(models.CartInfo.id == id).first()
    if delitem is None:
        return
    db.delete(delitem)
    db.commit()
    return delitem


# Mpesa processing function(Not Complete Yet)
def payment(db: Session, phone_number: int, total: int):
    consumer_key = 'consumer_key'
    consumer_secret = 'consumer_secret'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']

    lipa_time = datetime.now().strftime('%Y%m%d%H%M%S')
    Business_short_code = 'short_code'  # replace with the business short code
    passkey = "pass_key"
    data_to_encode = Business_short_code + passkey + lipa_time
    online_password = base64.b64encode(data_to_encode.encode())
    decode_password = online_password.decode('utf-8')

    access_token = validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "BusinessShortCode": Business_short_code,
        "Password": decode_password,
        "Timestamp": lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": total,
        "PartyA": phone_number,
        "PartyB": Business_short_code,
        "PhoneNumber": phone_number,
        "CallBackURL": "https://127.0.0.1:8000/callback",  # Mpesa Callback
        "AccountReference": "User Payment",
        "TransactionDesc": "Testing stk push"
    }
    response = requests.post(api_url, json=request, headers=headers)
    return response.text
