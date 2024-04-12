from telnetlib import EC
from time import sleep

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@pytest.fixture
def driver(request):
    driver = webdriver.Chrome()
    driver.get("http://localhost/litecart/admin")
    return driver


@pytest.fixture
def wait(driver):
    wait = WebDriverWait(driver, 10)
    return wait


def test_wrapper(driver, wait):
    username = driver.find_element(By.NAME, "username").send_keys('admin')
    password = driver.find_element(By.NAME, "password").send_keys('admin')
    login = driver.find_element(By.NAME, "login").click()
    menu_items = driver.find_elements(By.CSS_SELECTOR, "#box-apps-menu li#app-")
    print(menu_items)
    sleep(10)
    for i in range(len(menu_items)):
        menu_items = driver.find_elements(By.CSS_SELECTOR, "#box-apps-menu li#app-")
        menu_items[i].click()

        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1")))
            print(f"Заголовок h1 найден на странице: {driver.find_element(By.CSS_SELECTOR, 'h1').text}")
        except:
            print("Заголовок h1 не найден на странице")

        sub_menu_items = driver.find_elements(By.CSS_SELECTOR, "ul.docs li")
        if sub_menu_items:
            for j in range(len(sub_menu_items)):
                sub_menu_items = driver.find_elements(By.CSS_SELECTOR, "ul.docs li")
                sub_menu_items[j].click()

                try:
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1")))
                    print(f"Заголовок h1 найден на странице: {driver.find_element(By.CSS_SELECTOR, 'h1').text}")
                except:
                    print("Заголовок h1 не найден на странице")

    # Закрытие браузера
    driver.quit()
