import pyodbc
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

server = 'DESKTOP-ICDAN0L'
database = 'ecom_backend'
username = ''
password = ''

engine = create_engine(f'mssql+pyodbc://{server}/{database}?driver=SQL+Server+Native+Client+11.0')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
cxnn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cxnn.cursor()



#
# SQLALCHEMY_DATABASE_URL = "mssql+mysqlconnector://THybKxI0bq:9XPsxcR7g5@remotemysql.com:3306/THybKxI0bq"
# engine = create_engine(
#      SQLALCHEMY_DATABASE_URL, echo=True, connect_args={'use_unicode': "utf-8"}
#  )
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()
# cursor = cxnn.cursor()
# cxnn = mysql.connector.connect(host='remotemysql.com', database='THybKxI0bq', user='THybKxI0bq', password='9XPsxcR7g5')
# cursor = cxnn.cursor()



