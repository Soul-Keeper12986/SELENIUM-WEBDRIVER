from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import pytest


class TestLog:
    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost/litecart/admin/")

    def teardown_method(self):
        self.driver.quit()

    def login_as_admin(self):
        username_input = self.driver.find_element(By.NAME, "username")
        password_input = self.driver.find_element(By.NAME, "password")
        login_button = self.driver.find_element(By.NAME, "login")
        username_input.send_keys('admin')
        password_input.send_keys('admin')
        login_button.click()

    def navigate_to_catalog(self):
        catalog_link = self.driver.find_element(By.LINK_TEXT, "Catalog")
        catalog_link.click()

    def inspect_log(self):
        rubber_ducks = self.driver.find_element(By.LINK_TEXT, "Rubber Ducks")
        rubber_ducks.click()
        subcategory = self.driver.find_element(By.LINK_TEXT, 'Subcategory')
        subcategory.click()
        products = self.driver.find_elements(By.XPATH, "//table[@class='dataTable']//tr/td[3]/a")
        for i in range(len(products)):
            products = self.driver.find_elements(By.XPATH,"//table[@class='dataTable']//tr/td[3]/a")  # Находим элементы заново
            product = products[i]
            product.click()
            sleep(2)
            logs = self.driver.get_log('browser')
            if len(logs) > 0:
                print(f"Найдены сообщения в логе для товара: {self.driver.current_url}")
                for log in logs:
                    print(log)
            self.driver.back()

    def test_log(self):
        self.login_as_admin()
        self.navigate_to_catalog()
        self.inspect_log()


if __name__ == "__main__":
    pytest.main(args=['-s', __file__])
