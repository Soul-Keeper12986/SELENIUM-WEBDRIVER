from time import sleep

from selenium.webdriver.support import expected_conditions as EC
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.get("http://localhost/litecart/admin/?app=countries&doc=countries")
    return driver


def test_new_window_opend(driver):
    driver.find_element(By.NAME, "username").send_keys('admin')
    driver.find_element(By.NAME, "password").send_keys('admin')
    login = driver.find_element(By.NAME, "login")
    login.click()

    add_new_country = driver.find_element(By.CSS_SELECTOR, '#content > div > a')
    add_new_country.click()
    links = driver.find_element(By.CSS_SELECTOR, '#content > form > table:nth-child(2)')
    need_links = links.find_elements(By.CSS_SELECTOR, "[target='_blank']")
    for link in need_links:
        link.click()
        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
        handles = driver.window_handles
        driver.switch_to.window(handles[-1])
        sleep(2)
        driver.close()
        driver.switch_to.window(handles[0])
    driver.quit()
