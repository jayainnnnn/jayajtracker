from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from sqlalchemy.orm import Session
from datetime import date
from database import SessionLocal
from model import new_products,Products



db: Session = SessionLocal()

# options = webdriver.ChromeOptions()
# options.add_argument('--headless')

# driver = webdriver.Chrome(options)

driver = webdriver.Chrome()
driver.maximize_window()


data = db.query(new_products.url, new_products.email).all()

url_list = [row[0] for row in data]
email_list = [row[1] for row in data]


data = []

length = len(url_list)
for i in range(length):
    driver.get(url_list[i])
    wait = WebDriverWait(driver,10)

    try:
        

        wait.until(EC.element_to_be_clickable((By.ID,"productTitle")))

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
        product_link = url_list[i],
        product_image_link = image,
        price = price,
        email = email_list[i],
        date = today,
        )
        data.append(new_data)
    except (TimeoutException, NoSuchElementException) as e:
        print(f"[{i}] Failed to scrape: {url_list[i]} | Reason: {str(e)}")
    except Exception as e:
        print(f"[{i}] Unexpected error for URL: {url_list[i]} | {str(e)}")
try:
    db.add_all(data)
    db.commit()
    print(f"✅ Successfully added {len(data)} products.")
except Exception as e:
    db.rollback()
    print(f"❌ Database error: {e}")
finally:
    db.close()
    driver.quit()








