import pytest as pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def driver(request):
    wd = webdriver.chrome()
    request.addfinaliser(wd.quit)
    return wd

@pytest.fixture
def test_example(driver):
    driver.get("https://www.google.com/")
    driver.find_element_by_name("q").send_keys("webdriver")
    driver.find_element_by_name("btnG").click()
    WebDriverWait(driver, 10).until(EC.title_is("webdriver - Поиск в Google"))
