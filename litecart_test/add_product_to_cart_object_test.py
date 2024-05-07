import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MainPage:
    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get("http://localhost/litecart/en/")

    def select_first_product(self):
        first_product = self.driver.find_element(By.CSS_SELECTOR, '#box-most-popular > div > ul > li:nth-child(1)')
        first_product.click()


class ProductPage:
    def __init__(self, driver):
        self.driver = driver

    def add_to_cart(self):
        if self.product_named('Yellow Duck'):
            self.select_size('Small')
        self.add_to_cart_button().click()

    def product_named(self, name):
        return self.driver.find_element(By.CSS_SELECTOR, '#box-product > div:nth-child(1) > h1').text == name

    def select_size(self, size_name):
        size = self.driver.find_element(By.NAME, 'options[Size]')
        Select(size).select_by_visible_text(size_name)

    def add_to_cart_button(self):
        return self.driver.find_element(By.NAME, 'add_cart_product')


class CartPage:
    def __init__(self, driver):
        self.driver = driver

    def open(self):
        cart = self.driver.find_element(By.CSS_SELECTOR, '#cart > a.content')
        cart.click()

    def remove_product(self):
        remove_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'remove_cart_item')))
        remove_button.click()
        return remove_button


class TestShoppingFlow:
    PRODUCT_COUNT = 3

    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.main_page = MainPage(self.driver)
        self.product_page = ProductPage(self.driver)
        self.cart_page = CartPage(self.driver)

    def teardown_method(self):
        if self.driver:
            self.driver.quit()

    def cart_items_count(self):
        cart_item_element = self.driver.find_element(By.CSS_SELECTOR, '#cart > a.content > span.quantity')
        return int(cart_item_element.text)

    def wait_for_cart_update(self):
        original_cart_count = self.cart_items_count()
        WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, "#cart > a.content > span.quantity"), str(original_cart_count + 1)))
        self.driver.back()

    def cart_empty_message_visible(self):
        return WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#checkout-cart-wrapper > p:nth-child(1) > em'),
                                             'There are no items in your cart.'))

    def table_cart_update(self):
        return WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'table.dataTable.rounded-corners')))

    def remove_all_products(self):
        ul_element = self.driver.find_element(By.CSS_SELECTOR, "#box-checkout-cart > ul")
        cart_items = ul_element.find_elements(By.TAG_NAME, "li")
        counter = len(cart_items)
        while counter != 0:
            remove_button = self.cart_page.remove_product()
            WebDriverWait(self.driver, 10).until(EC.staleness_of(remove_button))
            counter -= 1
            print(counter)
            if counter != 0:
                self.table_cart_update()
            elif self.cart_empty_message_visible():
                self.driver.quit()

    def test_shopping_flow(self):
        self.main_page.open()

        while self.cart_items_count() < self.PRODUCT_COUNT:
            self.main_page.select_first_product()
            self.product_page.add_to_cart()
            self.wait_for_cart_update()
        self.cart_page.open()
        self.remove_all_products()


if __name__ == "__main__":
    pytest.main(args=['-s', __file__])
