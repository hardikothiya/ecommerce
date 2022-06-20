from sqlalchemy.orm import Session
import models, schemas
import bcrypt


# Get user by username function
def get_user_by_email(db: Session, email: str):
    a = db.query(models.UserInfo).filter(models.UserInfo.email == email).first()

    if a:
        return True


def get_user_by_userid(db: Session, user_id: int):
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

    if user is None:
        return {"msg": "invalid user id/email"}

    else:
        db_address = models.UserAddress(user_id=user.id, address_line1=address.address_line1,
                                        address_line2=address.address_line2, city=address.city,
                                        state=address.state, postal_code=address.postal_code,
                                        mobile_number=address.mobile_number)
        db.add(db_address)
        db.commit()
        db.refresh(db_address)
        return db_address


# Login Function
def get_Login(db: Session, user: schemas.UserLogin):
    db_user = db.query(models.UserInfo).filter(models.UserInfo.email == user.email).first()
    passw: bool = bcrypt.checkpw(user.password.encode('utf-8'), db_user.password.encode('utf-8'))
    if passw:
        return db_user


# Get item by id function
def get_item_by_id(db: Session, id: int):
    # a = db.query(models.ItemInfo).filter(models.ItemInfo.id == id).first()

    a = db.query(models.ItemInfo, models.ItemCategory, models.ItemDiscount).filter(models.ItemInfo.id == id). \
        join(models.ItemCategory, models.ItemInfo.category_id == models.ItemCategory.id). \
        join(models.ItemDiscount, models.ItemInfo.discount_id == models.ItemDiscount.id).first()

    b = {
        'itemid': a[0].id,
        'itemname': a[0].itemname,
        'itemprice': a[0].itemprice,
        'itemimage': a[0].itemimage,
        'description': a[0].description,
        'category_name': a[1].category_name,
        'discount_percentage': a[2].discount_percentage,

    }

    return b


def get_all_item(db: Session):
    a = db.query(models.ItemInfo, models.ItemCategory, models.ItemDiscount). \
        join(models.ItemCategory, models.ItemInfo.category_id == models.ItemCategory.id). \
        join(models.ItemDiscount, models.ItemInfo.discount_id == models.ItemDiscount.id).all()

    b = []
    for i in a:
        b.append({
            'itemid': i[0].id,
            'itemname': i[0].itemname,
            'itemprice': i[0].itemprice,
            'itemimage': i[0].itemimage,
            'description': i[0].description,
            'category_name': i[1].category_name,
            'discount_percentage': i[2].discount_percentage})

    return b


# Add items to DB function
def add_table(db: Session, item: schemas.ItemInfo):
    db_item = models.ItemInfo(itemname=item.itemname, itemprice=item.itemprice, itemimage=item.itemimage,
                              description=item.description, category_id=item.category_id,
                              discount_id=item.discount_id)
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
    try:
        db_inventory = models.ItemInventory(inventory_quantity=inventory.inventory_quantity,
                                            item_id=inventory.item_id)
        db.add(db_inventory)
        db.commit()
        db.refresh(db_inventory)
        return db_inventory
    except Exception as e:
        return "Error occurred"


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

    item_price = db.query(models.ItemInfo).filter(models.ItemInfo.id == cart.product_id).first()

    final_amount = item_price.itemprice * cart.quantity
    db_cart = models.CartInfo(user_id=user.id, product_id=cart.product_id,
                              quantity=cart.quantity, item_amount=final_amount)
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart


def get_cart(db: Session, user_id: int):
    user = db.query(models.UserInfo).filter(models.UserInfo.id == user_id).first()
    a = db.query(models.CartInfo).filter(models.CartInfo.user_id == user.id).all()
    list_cart = {}
    quantity = 0
    final_amount = 0

    if len(a) != 0:
        for x in range(len(a)):
            b = get_item_by_id(db, a[x].product_id)
            b['quantity'] = a[x].quantity
            b['item_amount'] = a[x].item_amount
            list_cart[a[x].id] = b
            quantity += a[x].quantity
            final_amount += a[x].item_amount

        return {
            "all_item ": list_cart,
            "quantity": quantity,
            "bill_amount": final_amount
        }

    else:
        return "cart is empty"


def get_order(db: Session, user_id: int):
    return db.query(models.OrderDetails).filter(models.OrderDetails.user_id == user_id).first()


def order_details(db: Session, user_id: int):
    a = get_cart(db=db, user_id=user_id)
    b = db.query(models.UserAddress).filter(models.UserAddress.user_id == user_id).first()
    d_order = db.query(models.OrderDetails).filter(models.OrderDetails.user_id == user_id).first()

    if d_order:
        d_order.bill_amount = a['bill_amount']
        d_order.quantity = a['quantity']
        db.commit()
        db.refresh(d_order)
        return {
            "order": a,
            "shipping_address": b
        }
    else:
        db_order = models.OrderDetails(bill_amount=a['bill_amount'], quantity=a['quantity'], user_id=user_id)

        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        return {
            "order": a,
            "shipping_address": b
        }


# Delete item in the cart by id
def delete_cart_item_by_id(db: Session, id: int):
    delitem = db.query(models.CartInfo).filter(models.CartInfo.id == id).first()
    if delitem is None:
        return
    db.delete(delitem)
    db.commit()
    return delitem

# Mpesa processing function(Not Complete Yet)
# def payment(db: Session, phone_number: int, total: int):
#     consumer_key = 'consumer_key'
#     consumer_secret = 'consumer_secret'
#     api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
#
#     r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
#     mpesa_access_token = json.loads(r.text)
#     validated_mpesa_access_token = mpesa_access_token['access_token']
#
#     lipa_time = datetime.now().strftime('%Y%m%d%H%M%S')
#     Business_short_code = 'short_code'  # replace with the business short code
#     passkey = "pass_key"
#     data_to_encode = Business_short_code + passkey + lipa_time
#     online_password = base64.b64encode(data_to_encode.encode())
#     decode_password = online_password.decode('utf-8')
#
#     access_token = validated_mpesa_access_token
#     api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
#     headers = {"Authorization": "Bearer %s" % access_token}
#     request = {
#         "BusinessShortCode": Business_short_code,
#         "Password": decode_password,
#         "Timestamp": lipa_time,
#         "TransactionType": "CustomerPayBillOnline",
#         "Amount": total,
#         "PartyA": phone_number,
#         "PartyB": Business_short_code,
#         "PhoneNumber": phone_number,
#         "CallBackURL": "https://127.0.0.1:8000/callback",  # Mpesa Callback
#         "AccountReference": "User Payment",
#         "TransactionDesc": "Testing stk push"
#     }
#     response = requests.post(api_url, json=request, headers=headers)
#     return response.text
