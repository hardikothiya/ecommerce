import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Body
from common import send_mail

from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import engine, SessionLocal


models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Ecom")

#  Dependency

def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


###########################################################################

# register API
@app.post("/register", tags=["User"], response_model=schemas.UserInfo)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    send_mail(user.email)

    a = crud.get_user_by_email(db, user.email)

    if a:
        raise HTTPException(status_code=400, detail="Email already registered")
    else:

        return crud.create_user(db=db, user=user)


# login API
@app.post("/login", tags=["User"], response_model=schemas.UserInfo)
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_Login(db, user)
    if not db_user:
        raise HTTPException(status_code=400, detail="Wrong username/password")
    return db_user


@app.post("/add_address", tags=["User"])
def add_address(user_id: int, address: schemas.UserAddress, db: Session = Depends(get_db)):
    try:
        a = crud.add_address(user_id=user_id, address=address, db=db)
        return a
    except Exception as e:
        return "invalid value"


# get user by username API
@app.get("/get_user/{user_id}", tags=["User"])
def get_user(user_id, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_userid(db, user_id=user_id)
    return db_user


@app.post("/add_item", tags=["Admin"])
def add_item(item: schemas.ItemInfo, db: Session = Depends(get_db)):
    return crud.add_table(db=db, item=item)


# get item by id API
@app.get("/get_item/{id}", tags=["User"])
def get_item(id, db: Session = Depends(get_db)):
    db_item = crud.get_item_by_id(db, id=id)
    return db_item


@app.post("/add_category", tags=["Admin"])
def add_category(category: schemas.ItemCategory, db: Session = Depends(get_db)):
    return crud.add_category(db=db, category=category)


@app.post("/add_discount", tags=["Admin"])
def add_discount(discount: schemas.ItemDiscount, db: Session = Depends(get_db)):
    return crud.add_discount(db=db, discount=discount)


@app.post("/add_inventory", tags=["Admin"])
def add_inventory(inventory: schemas.ItemInventory, db: Session = Depends(get_db)):
    return crud.add_inventory(db=db, inventory=inventory)


@app.post("/get_all_item", tags=["User"])
def get_all_item(db: Session = Depends(get_db)):
    return crud.get_all_item(db)


# delete item by id API
@app.delete("/del_item/{id}", tags=["Admin"], response_model=schemas.ItemAInfo)
def del_item(id, db: Session = Depends(get_db)):
    db_item = crud.delete_item_by_id(db, id=id)
    if db_item:
        raise HTTPException(status_code=200, detail="Item found to delete")
    else:
        raise HTTPException(status_code=400, detail="Item Not found to delete")


# add to cart by username and the items to be added API
@app.post("/add_to_cart/{user_id}", tags=["User"])
def add_item_cart(user_id, cart: schemas.CartCreate, db: Session = Depends(get_db)):
    print(cart)
    db_cart = crud.add_to_cart(db=db, cart=cart, user_id=user_id)
    if db_cart:
        raise HTTPException(status_code=200, detail="item registered to cart")
    return


@app.post("/get_cart/{user_id}", tags=["User"])
def get_cart(user_id, db: Session = Depends(get_db)):
    db_cart = crud.get_cart(db=db, user_id=user_id)
    return db_cart


@app.post("/order_details", tags=["User"])
def get_order(user_id, db: Session = Depends(get_db)):
    db_order = crud.order_details(user_id=user_id, db=db)
    return db_order


# delete items in the cart by id API
@app.delete("/del_cart_item/{id}", tags=["User"])
def del_user(id, db: Session = Depends(get_db)):
    db_item = crud.delete_cart_item_by_id(db, id=id)
    if db_item:
        raise HTTPException(status_code=200, detail="Item found to delete")
    else:
        raise HTTPException(status_code=400, detail="Item Not found to delete")


# mpesa payment API
# @app.post("/payment")
# def add_payment(userphone: schemas.UserPayment, db: Session = Depends(get_db)):
#     user_payment = crud.payment(db=db, phone_number=userphone.phonenumber, total=userphone.total)
#     if user_payment:
#         raise HTTPException(status_code=200, detail="payment Started")
#     return


# mpesa Callback API
@app.post("/callback")
def mpesa_callback(db: Session = Depends(get_db)):
    return {'success': "Payment was made successfully"}


######################################

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
