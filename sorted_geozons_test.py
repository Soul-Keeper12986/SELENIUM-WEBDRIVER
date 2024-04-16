import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.get("http://localhost/litecart/admin/?app=geo_zones&doc=geo_zones")
    return driver


def test_sorted_geozon(driver):
    driver.find_element(By.NAME, "username").send_keys('admin')
    driver.find_element(By.NAME, "password").send_keys('admin')
    login = driver.find_element(By.NAME, "login")
    login.click()

    # Получаем список всех стран
    countries = driver.find_elements(By.CSS_SELECTOR, "table.dataTable tr.row")

    for i in range(len(countries)):
        countries = driver.find_elements(By.CSS_SELECTOR, "table.dataTable tr.row")  # Повторное получение списка стран
        country_link = countries[i].find_element(By.CSS_SELECTOR, "a")

        country_link.click()

        # Получаем список всех зон для текущей страны
        zones_list = driver.find_elements(By.CSS_SELECTOR,
                                          "table.dataTable select[name*='zone_code'] option[selected='selected']")
        zone_names = [zone.text for zone in zones_list]

        # Проверяем, что зоны расположены в алфавитном порядке
        if zone_names == sorted(zone_names):
            print("Зоны для стран расположены в алфавитном порядке")
        else:
            print("Зоны для страны НЕ расположены в алфавитном порядке")

        driver.back()

    driver.quit()
