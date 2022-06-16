
import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud  # import the files
import models
import schemas
from database import engine, SessionLocal  # import d functions

models.Base.metadata.create_all(bind=engine)

app = FastAPI()



#  Dependency


def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


###########################################################################


def resultset(cursor):
    """"
    function for get all result set with key-value pair from table
    """
    sets = []
    while True:
        names = [c[0] for c in cursor.description]
        set_ = []
        while True:
            row_raw = cursor.fetchone()
            if row_raw is None:
                break
            row = dict(zip(names, row_raw))
            set_.append(row)
        sets.append(list(set_))
        if cursor.nextset() is None or cursor.description is None:
            break
    return sets


# register API
@app.post("/register", response_model=schemas.UserInfo)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


# login API
@app.post("/login")
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_Login(db, email=user.email, password=user.password)
    if not db_user:
        raise HTTPException(status_code=400, detail="Wrong username/password")
    return {"message": "User found"}

@app.get("/add_address")
def add_address(username: str, address: schemas.UserAddress, db: Session = Depends(get_db)):
    return crud.add_address(db, username, address)


# get user by username API
@app.get("/get_user/{username}", response_model=schemas.UserInfo)
def get_user(email, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=email)
    return db_user


@app.post("/add_item")
def add_item(item: schemas.ItemInfo, db: Session = Depends(get_db)):
    return crud.add_table(db=db, item=item)


# get item by id API
@app.get("/get_item/{id}", )
def get_item(id, db: Session = Depends(get_db)):
    db_item = crud.get_item_by_id(db, id=id)
    return db_item


@app.get("/get_all_item")
def get_all_item(db: Session = Depends(get_db)):
    return crud.get_all_item(db)


# delete item by id API
@app.delete("/del_item/{id}", response_model=schemas.ItemAInfo)
def del_item(id, db: Session = Depends(get_db)):
    db_item = crud.delete_item_by_id(db, id=id)
    if db_item:
        raise HTTPException(status_code=200, detail="Item found to delete")
    else:
        raise HTTPException(status_code=400, detail="Item Not found to delete")
    return


# add to cart by username and the items to be added API
@app.post("/add_to_cart/{username}", response_model=schemas.CartOwnerInfo)
def add_item_cart(username, items: schemas.CartInfo, db: Session = Depends(get_db)):
    db_cart = crud.add_to_cart(db=db, username=username, items=items)
    if db_cart:
        raise HTTPException(status_code=200, detail="item registered to cart")
    return


# delete items in the cart by id API
@app.delete("/del_cart_item/{id}", response_model=schemas.CartItemAInfo)
def del_user(id, db: Session = Depends(get_db)):
    db_item = crud.delete_cart_item_by_id(db, id=id)
    if db_item:
        raise HTTPException(status_code=200, detail="Item found to delete")
    else:
        raise HTTPException(status_code=400, detail="Item Not found to delete")
    return


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

from fastapi.param_functions import Form
from typing import Optional


class KycInsertRequestForm:
    def __init__(
            self,
            userid: int = Form(0),
            country_id: int = Form(0),
            document_type_id: int = Form(0),
            name: Optional[str] = Form(''),
            mode: Optional[str] = Form('INSERT'),

    ):
        self.mode = mode
        self.userid = userid
        self.country_id = country_id
        self.document_type_id = document_type_id
        self.name = name


@app.post("/account/KYC_select")
async def KYC_select(
        form_data: KycInsertRequestForm = Depends()
):
    try:
        print("Form data =======>> ", form_data.userid)
        execstring = f"exec Sp_KYC '{form_data.mode}',{form_data.userid},{form_data.country_id}," \
                     f"{form_data.document_type_id}, {form_data.name}"
        print("string ----->>>", execstring)
        return "Suceed"

    except Exception as e:
        return {
            "code": 500,
            "status": "error",
            "message": " Exception {} occurred while KYC_select.".format(e)
        }


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
