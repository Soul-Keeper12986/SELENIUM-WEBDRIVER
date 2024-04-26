from time import sleep

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


@pytest.fixture
def driver(request):
    driver = webdriver.Chrome()
    print(driver.capabilities)
    request.addfinalizer(driver.quit)
    return driver

def test_exaple1(driver):
    driver.get('https://soreal.ru/uilyam-batler-jejts/')
    link_next = driver.find_element(By.CSS_SELECTOR,"a[rel='next']")
    link_next.click()
    sleep(5)
    driver.quit()

