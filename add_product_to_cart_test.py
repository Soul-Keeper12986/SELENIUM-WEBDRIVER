import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestShoppingFlow:
    PRODUCT_COUNT = 3

    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost/litecart/en/")

    def teardown_method(self):
        if self.driver:
            self.driver.quit()

    def add_product_to_cart(self):
        cart_item_element = self.driver.find_element(By.CSS_SELECTOR, '#cart > a.content > span.quantity')
        while int(cart_item_element.text) < self.PRODUCT_COUNT:
            first_product = self.driver.find_element(By.CSS_SELECTOR,
                                                     '#box-most-popular > div > ul > li:nth-child(1)')
            first_product.click()

            original_cart_count = int(
                self.driver.find_element(By.CSS_SELECTOR, '#cart > a.content > span.quantity').text)
            if self.driver.find_element(By.CSS_SELECTOR,
                                        '#box-product > div:nth-child(1) > h1').text == 'Yellow Duck':
                size = self.driver.find_element(By.NAME, 'options[Size]')
                Select(size).select_by_visible_text("Small")
            add_to_cart = self.driver.find_element(By.NAME, 'add_cart_product')
            add_to_cart.click()

            WebDriverWait(self.driver, 10).until(
                EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#cart > a.content > span.quantity"),
                                                 str(original_cart_count + 1)))
            self.driver.back()
            cart_item_element = self.driver.find_element(By.CSS_SELECTOR, '#cart > a.content > span.quantity')

    def remove_products_from_cart(self):
        cart = self.driver.find_element(By.CSS_SELECTOR, '#cart > a.content')
        cart.click()
        ul_element = self.driver.find_element(By.CSS_SELECTOR, "#box-checkout-cart > ul")
        counter = int(len(ul_element.find_elements(By.TAG_NAME, "li")))
        while counter != 0:
            counter -= 1
            remove_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'remove_cart_item')))
            remove_button.click()
            if counter != 0:
                WebDriverWait(self.driver, 10).until(EC.staleness_of(remove_button))  # Ждем исчезновения кнопки
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'table.dataTable.rounded-corners')))
            elif WebDriverWait(self.driver, 10).until(
                    EC.text_to_be_present_in_element(
                        (By.CSS_SELECTOR, '#checkout-cart-wrapper > p:nth-child(1) > em'),
                        'There are no items in your cart.')):
                self.driver.quit()

    def test_shopping_flow(self):
        self.add_product_to_cart()
        self.remove_products_from_cart()


if __name__ == "__main__":
    pytest.main(args=['-s', __file__])
