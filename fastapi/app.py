from fastapi import FastAPI,HTTPException,Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,EmailStr
from datetime import date
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import and_

from model import Base,Products,Signup,new_products
from database import SessionLocal, engine


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from sqlalchemy.orm import Session
from datetime import date
from database import SessionLocal
from model import new_products,Products



app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class login_data(BaseModel):
    email: Annotated[EmailStr, Field(..., description="Email ID")]
    password: Annotated[str, Field(..., description="Password")]

class signup_data(BaseModel):
    name: Annotated[str, Field(..., description="name of person", examples=["Jay"])]
    email : EmailStr
    password : Annotated[str, Field(..., description="Password")]
    phone_number : Annotated[str, Field(..., description="Phone number")]


@app.post("/signup")
def signup(user: signup_data, db: Session = Depends(get_db)):
    if db.query(Signup).filter_by(email=user.email).first():
        raise HTTPException(status_code=400, detail="GMAIL ALREADY EXISTS")
    if db.query(Signup).filter_by(phone_number=user.phone_number).first():
        raise HTTPException(status_code=400, detail="PHONE NUMBER ALREADY EXISTS")

    db.add(Signup(
        name=user.name,
        email=user.email,
        password=user.password,
        phone_number = user.phone_number
    ))
    db.commit()

    return JSONResponse(status_code=201, content={"message": "SIGNUP SUCCESSFUL"})

@app.post("/login")
def login(user: login_data, db: Session = Depends(get_db)):
    user_login = db.query(Signup).filter_by(email=user.email).first()
    if not user_login:
        raise HTTPException(status_code=404, detail="USER NOT FOUND")
    if user_login.password != user.password:
        raise HTTPException(status_code=401, detail="INVALID PASSWORD")
    user_login = db.query(Signup).filter_by(email=user.email).first()
    return user_login


class products_data(BaseModel):
    email : Annotated[EmailStr, Field(...,description="email",examples=["jayjitendrajainn@gmail.com"])]


@app.post("/products")
def products_list(user_products: products_data,db: Session = Depends(get_db)):
    items =  db.query(Products).filter(and_(Products.email== user_products.email , Products.date==date.today())).all()
    if not items:
        return items
        raise HTTPException(status_code=400,detail="PRODUCT DOESNOT EXIST")
    return items


class product_data(BaseModel):
    email: Annotated[EmailStr, Field(...,description="email",examples=["jayjitendrajainn@gmail.com"])]
    product_name: Annotated[str, Field(..., description="NAME OF PRODUCT")]


@app.post("/product")
def product_list(user_product:product_data,db: Session = Depends(get_db)):
    lists = db.query(Products).filter(and_(Products.email==user_product.email,
                                           Products.product_name==user_product.product_name)).order_by(Products.date.asc()).all()
    if not lists:
        raise HTTPException(status_code=400,detail="PRODUCT DOESNOT EXIST")
    
    return lists

class add_product(BaseModel):
    url : Annotated[str,Field(...,description="url of new product")]
    email : Annotated[EmailStr,Field(...,description="email of new person")]
@app.post("/addproduct")
def addproduct(add_url: add_product, db: Session = Depends(get_db)):
    db.add(new_products(
        url = add_url.url,
        email = add_url.email
    ))
    db.commit()

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')

    driver = webdriver.Chrome(options)
    driver.get(add_url.url)
    wait = WebDriverWait(driver,10)

    try:
        wait.until(EC.element_to_be_clickable((By.ID,"productTitle")))
        wait.until(EC.element_to_be_clickable((By.ID,"landingImage")))
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME,"a-price-whole")))

        try:
            price = driver.find_element(By.CLASS_NAME, "a-price-whole").text
            price = int(price.replace(",", "").strip())
        except:
            price = 0
        name = driver.find_element(By.ID, "productTitle").text.strip()

        image = driver.find_element(By.ID, "landingImage").get_attribute("src")
        today = date.today()
        new_data = Products(
        product_name = name,
        product_link = add_url.url,
        product_image_link = image,
        price = price,
        email = add_url.email,
        date = today,
        )
        db.add(new_data)
    except TimeoutException:
        print(f"Element not found for index {i}, skipping...")
    db.commit()
    db.close()



    return JSONResponse(status_code=201, content={"message": "URL ADDED SUCCESSFUL"})

