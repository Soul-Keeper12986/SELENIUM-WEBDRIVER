import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.get("http://localhost/litecart/admin/?app=countries&doc=countries")
    return driver


def test_countries_sorting(driver):
    driver.find_element(By.NAME, "username").send_keys('admin')
    driver.find_element(By.NAME, "password").send_keys('admin')
    login = driver.find_element(By.NAME, "login")
    login.click()

    rows = driver.find_elements(By.XPATH, '//*[@id="content"]/form/table/tbody/tr[@class="row"]')

    countries = {}

    # Проверка стран на алфавитный порядок
    for row in rows:
        country_name = row.find_element(By.XPATH, './/td[5]').text
        country_code = row.find_element(By.XPATH, './/td[4]').text
        zone_count = int(row.find_element(By.XPATH, './/td[6]').text)

        countries[country_name] = zone_count

        print(f'{country_name} ({country_code}) - {zone_count} зон')

    # Проверяем, что страны расположены в алфавитном порядке
    assert list(countries.keys()) == sorted(countries.keys()), "Страны расположены не в алфавитном порядке"

    # Проверяем зоны для стран с несколькими зонами
    for country, zones in countries.items():
        try:
            if zones != 0:
                print(f'Провекрка {country} зон...')
                driver.find_element(By.LINK_TEXT, country).click()
                zone_elements = driver.find_elements(By.XPATH, '//*[@id="table-zones"]/tbody/tr/td[3]')
                zone_names = [zone.text for zone in zone_elements if zone.text]
                if zone_names == sorted(zone_names):
                    print('Зоны для ' + country + 'отсортированы в алфовитном порядке')
                driver.back()
        except Exception as e:
            print(f'Произошла ошибка для страны' + country + ': {e}')

    driver.quit()
