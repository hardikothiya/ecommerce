from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import mysql.connector


SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:hardik991322@localhost:3306/ecom_backend"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=True, connect_args={'use_unicode': "utf-8"}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


cxnn = mysql.connector.connect(host='localhost', database='ecom_backend', user='root', password='hardik991322')
cursor = cxnn.cursor()


# SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://sql6499676:kQCr914jWd@sql6.freemysqlhosting.net:3306/sql6499676"
#
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, echo=True, connect_args={'use_unicode': "utf-8"}
# )
#
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
# Base = declarative_base()
