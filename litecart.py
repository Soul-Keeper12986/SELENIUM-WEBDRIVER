from time import sleep

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


@pytest.fixture
def driver(request):
    driver = webdriver.Chrome()
    request.addfinalizer(driver.quit)
    return driver

def test_exaple1(driver):
    driver.get('http://localhost/litecart/admin')
    username = driver.find_element(By.NAME, "username").send_keys('test')
    password = driver.find_element(By.NAME, "password").send_keys('test')
    login = driver.find_element(By.NAME, "Login").click()
    sleep(5)
    driver.quit()

