from time import sleep

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestShoppingFlow:

    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost/litecart/en/")

    def teardown_method(self):
        self.driver.quit()

    def test_shopping_flow(self):
        cart_item_element = self.driver.find_element(By.CSS_SELECTOR, '#cart > a.content > span.quantity')
        while int(cart_item_element.text) < 3:
            self.add_product_to_cart()
            cart_item_element = self.driver.find_element(By.CSS_SELECTOR, '#cart > a.content > span.quantity')
        cart = self.driver.find_element(By.CSS_SELECTOR, '#cart > a.content')
        cart.click()

    def add_product_to_cart(self):
        first_product = self.driver.find_element(By.CSS_SELECTOR, '#box-most-popular > div > ul > li:nth-child(1)')
        first_product.click()

        original_cart_count = int(self.driver.find_element(By.CSS_SELECTOR, '#cart > a.content > span.quantity').text)
        if self.driver.find_element(By.CSS_SELECTOR, '#box-product > div:nth-child(1) > h1').text == 'Yellow Duck':
            size = self.driver.find_element(By.NAME, 'options[Size]')
            Select(size).select_by_visible_text("Small")
        add_to_cart = self.driver.find_element(By.NAME, 'add_cart_product')
        add_to_cart.click()

        WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#cart > a.content > span.quantity"),
                                             str(original_cart_count + 1)))
        self.driver.back()
        sleep(2)

    def remove_all_products_from_cart(self):
        while True:
            try:
                remove_button = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.NAME, 'remove_cart_item')))
                remove_button.click()
                WebDriverWait(self.driver, 10).until(EC.staleness_of(remove_button))
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'table.dataTable.rounded-corners')))
            except:
                break

            if len(self.driver.find_elements(By.CSS_SELECTOR, '#checkout-cart-wrapper > p:nth-child(1) > em')) > 0:
                break

    def test_product(self):
        self.test_shopping_flow()
        self.remove_all_products_from_cart()


if __name__ == "__main__":
    pytest.main(['-k', 'TestShoppingFlow.test_product'])

