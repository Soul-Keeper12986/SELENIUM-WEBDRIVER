from random import randint
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.get("http://localhost/litecart/en/")
    yield driver
    driver.quit()


def test_registration(driver):
    send_password = str(randint(0, 999999999)).zfill(10)
    email = f"test{randint(1325, 78671)}@mail.ru"
    register_button = driver.find_element(By.CSS_SELECTOR,
                                          "#box-account-login > div > form > table > tbody > tr:nth-child(5) > td > a")
    register_button.click()
    country_dropdown = driver.find_element(By.XPATH,
                                           "//*[@id='create-account']/div/form/table/tbody/tr[5]/td[1]/select")
    # Используем Select для работы с выпадающим списком
    select = Select(country_dropdown)
    # Выбираем страну "United States"
    select.select_by_visible_text("United States")
    phone = driver.find_element(By.NAME, 'phone')

    fields = {
        'tax_id': randint(10000, 99999),
        'company': "Company Name",
        'firstname': 'Egor',
        'lastname': 'Tester',
        'address1': 'Railroad',
        'postcode': '12345',
        'city': 'Montgomery',
        'email': email,
        'phone': str(phone.get_attribute('placeholder')) + str(randint(0, 999999999)).zfill(9),
        'password': send_password,
        'confirmed_password': send_password
    }

    for field_name, value in fields.items():
        field = driver.find_element(By.NAME, field_name)
        field.send_keys(value)

    create_account_button = driver.find_element(By.NAME, 'create_account')
    create_account_button.click()

    logout_link = driver.find_element(By.XPATH, '//*[@id="box-account"]/div/ul/li[4]/a')
    logout_link.click()

    login_email = driver.find_element(By.NAME, 'email')
    login_password = driver.find_element(By.NAME, 'password')
    login_email.send_keys(email)
    login_password.send_keys(send_password, Keys.ENTER)
    driver.find_element(By.XPATH, '//*[@id="box-account"]/div/ul/li[4]/a').click()

    driver.quit()