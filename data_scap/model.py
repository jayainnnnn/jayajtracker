from sqlalchemy import Column,String,Integer,Date
from database import Base

class new_products(Base):
    __tablename__ = "all_products"
    url = Column(String,primary_key=True)
    email = Column(String,nullable=True)

class Products(Base):
    __tablename__ = "products"
    product_name = Column(String, primary_key=True)
    product_link = Column(String, nullable=False)
    product_image_link = Column(String,nullable=False)
    price = Column(Integer,nullable=False)
    email = Column(String,nullable=False)
    date = Column(Date, primary_key=True)

