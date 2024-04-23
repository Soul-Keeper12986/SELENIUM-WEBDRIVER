from time import sleep
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.get("http://localhost/litecart/en/")
    yield driver
    driver.quit()


def test_shopping_flow(driver):
    cart_item_element = driver.find_element(By.CSS_SELECTOR, '#cart > a.content > span.quantity')
    while int(cart_item_element.text) < 3:
        first_product = driver.find_element(By.CSS_SELECTOR, '#box-most-popular > div > ul > li:nth-child(1)')
        first_product.click()

        original_cart_count = int(driver.find_element(By.CSS_SELECTOR, '#cart > a.content > span.quantity').text)
        if driver.find_element(By.CSS_SELECTOR, '#box-product > div:nth-child(1) > h1').text == 'Yellow Duck':
            size = driver.find_element(By.NAME, 'options[Size]')
            Select(size).select_by_visible_text("Small")
        add_to_cart = driver.find_element(By.NAME, 'add_cart_product')
        add_to_cart.click()

        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#cart > a.content > span.quantity"),
                                             str(original_cart_count + 1)))
        driver.back()
        cart_item_element = driver.find_element(By.CSS_SELECTOR, '#cart > a.content > span.quantity')
        sleep(2)

    cart = driver.find_element(By.CSS_SELECTOR, '#cart > a.content')
    cart.click()
    sleep(2)
    while True:
        try:
            # Находим и нажимаем на кнопку "Remove"
            remove_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'remove_cart_item')))
            remove_button.click()
            WebDriverWait(driver, 10).until(EC.staleness_of(remove_button))  # Ждем исчезновения кнопки
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'table.dataTable.rounded-corners')))
        except:
            break

        if len(driver.find_elements(By.CSS_SELECTOR, '#checkout-cart-wrapper > p:nth-child(1) > em')) > 0:
            break

    driver.quit()
