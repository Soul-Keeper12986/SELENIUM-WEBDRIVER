import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.get("http://localhost/litecart/")
    return driver

def test(driver):
    products = driver.find_elements(By.CSS_SELECTOR, ".product")
    for product in products:
        stickers = product.find_elements(By.CSS_SELECTOR, ".sticker")

        try:
            if len(stickers) == 1:
                print("У товара есть только 1 стикер")
        except:
            print("У товара нет стикера или их больше 1")

    driver.quit()

