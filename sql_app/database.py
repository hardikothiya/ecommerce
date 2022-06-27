from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import mysql.connector

# SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:hardik991322@localhost:3306/ecom_backend"
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://THybKxI0bq:9XPsxcR7g5@remotemysql.com:3306/THybKxI0bq"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=True, connect_args={'use_unicode': "utf-8"}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# cxnn = mysql.connector.connect(host='localhost', database='ecom_backend', user='root', password='hardik991322')
cxnn = mysql.connector.connect(host='remotemysql.com', database='THybKxI0bq', user='THybKxI0bq', password='9XPsxcR7g5')

cursor = cxnn.cursor()

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, echo=True, connect_args={'use_unicode': "utf-8"}
# )
#
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
# Base = declarative_base()
