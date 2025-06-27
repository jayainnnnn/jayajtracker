from sqlalchemy import Column,String,Integer,Date,LargeBinary
from database import Base

class Signup(Base):
    __tablename__ = "signup"
    name = Column(String, nullable=False)
    email = Column(String, primary_key=True)
    password = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)

class Products(Base):
    __tablename__ = "products"
    product_name = Column(String, primary_key=True)
    product_link = Column(String, nullable=False)
    product_image_link = Column(String,nullable=False)
    price = Column(Integer,nullable=False)
    email = Column(String,nullable=False)
    date = Column(Date, primary_key=True)

class new_products(Base):
    __tablename__ = "all_products"
    url = Column(String,primary_key=True)
    email = Column(String,nullable=False)



