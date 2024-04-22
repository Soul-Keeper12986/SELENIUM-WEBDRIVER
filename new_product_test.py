from time import sleep
import os
from random import randint
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class TestAdminPanel:
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
        sleep(2)

    def navigate_to_catalog(self):
        catalog_link = self.driver.find_element(By.LINK_TEXT, "Catalog")
        catalog_link.click()
        sleep(2)

    def add_new_product(self):
        add_product_button = self.driver.find_element(By.CSS_SELECTOR, '#content > div:nth-child(2) > a:nth-child(2)')
        add_product_button.click()

        element = WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.TAG_NAME, "html")))
        name_input = element.find_element(By.NAME, 'name[en]')
        name_input.send_keys("Ytochka")

        code_input = self.driver.find_element(By.NAME, 'code')
        code_input.send_keys(str(randint(0, 999999999)).zfill(5))

        checkbox = self.driver.find_element(By.XPATH,
                                            '//*[@id="tab-general"]/table/tbody/tr[4]/td/div/table/tbody/tr[3]/td['
                                            '1]/input')
        checkbox.click()

        unisex_gender = self.driver.find_element(By.XPATH,
                                                 '//*[@id="tab-general"]/table/tbody/tr[7]/td/div/table/tbody/tr['
                                                 '4]/td[1]/input')
        unisex_gender.click()

        sleep(2)

        quantity_input = self.driver.find_element(By.NAME, 'quantity')
        quantity_input.clear()
        quantity_input.send_keys(randint(1, 5))

        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, "images\\1e6763690cba9156393df750092ee4d5.jpg")
        input_file = self.driver.find_element(By.XPATH,
                                              '//*[@id="tab-general"]/table/tbody/tr[9]/td/table/tbody/tr[1]/td/input')
        sleep(2)
        input_file.send_keys(file_path)

        date_valid_from_input = self.driver.find_element(By.NAME, 'date_valid_from')
        date_valid_from_input.send_keys('01010001')

        sleep(2)

        date_valid_to_input = self.driver.find_element(By.NAME, 'date_valid_to')
        date_valid_to_input.send_keys('09129999')
        sleep(2)

        infomation_page_link = self.driver.find_element(By.XPATH, '//*[@id="content"]/form/div/ul/li[2]/a')
        infomation_page_link.click()

        manufacturer_dropdown = self.driver.find_element(By.NAME, 'manufacturer_id')
        Select(manufacturer_dropdown).select_by_visible_text('ACME Corp.')

        keywords_input = self.driver.find_element(By.NAME, 'keywords')
        keywords_input.send_keys('Test string')

        short_description_input = self.driver.find_element(By.NAME, 'short_description[en]')
        short_description_input.send_keys('Short description')

        description_input = self.driver.find_element(By.XPATH,
                                                     '//*[@id="tab-information"]/table/tbody/tr[5]/td/span/div/div[2]')
        description_input.send_keys('description')

        head_title_input = self.driver.find_element(By.NAME, 'head_title[en]')
        head_title_input.send_keys('Head title')

        meta_description_input = self.driver.find_element(By.NAME, 'meta_description[en]')
        meta_description_input.send_keys('Meta description')

        prices_link = self.driver.find_element(By.XPATH, '//*[@id="content"]/form/div/ul/li[4]/a')
        prices_link.click()

        purchase_price_input = self.driver.find_element(By.NAME, 'purchase_price')
        purchase_price_input.send_keys(randint(15, 30))

        purchase_price_currency_dropdown = self.driver.find_element(By.NAME, 'purchase_price_currency_code')
        Select(purchase_price_currency_dropdown).select_by_visible_text('US Dollars')

        gross_prices_usd_input = self.driver.find_element(By.NAME, 'gross_prices[USD]')
        gross_prices_usd_input.send_keys('18')

        gross_prices_eur_input = self.driver.find_element(By.NAME, 'gross_prices[EUR]')
        gross_prices_eur_input.send_keys('19')

        save_button = self.driver.find_element(By.NAME, 'save')
        save_button.click()

    def test_new_product(self):
        self.login_as_admin()
        self.navigate_to_catalog()
        self.add_new_product()


if __name__ == "__main__":
    pytest.main(args=['-s', __file__])
