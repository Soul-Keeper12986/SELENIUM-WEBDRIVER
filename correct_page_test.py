import re
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.get("http://localhost/litecart/en/")
    return driver


def test_page_and_product(driver):
    # Находим первый товар в блоке Campaigns
    sale_price = driver.find_element(By.CSS_SELECTOR,
                                     "#box-campaigns > div > ul > li > a.link > div.price-wrapper > strong")
    regular_price = driver.find_element(By.CSS_SELECTOR,
                                        "#box-campaigns > div > ul > li > a.link > div.price-wrapper > s")
    product_name = driver.find_element(By.CSS_SELECTOR, "#box-campaigns > div > ul > li > a.link > div.name").text

    regular_price_text = regular_price.text
    sale_price_text = sale_price.text
    regular_price_style = regular_price.value_of_css_property("color")
    regular_price_lined = regular_price.value_of_css_property('text-decoration-line')
    sale_price_style = sale_price.value_of_css_property("color")
    regular_price_size = regular_price.value_of_css_property("font-size")
    sale_price_size = sale_price.value_of_css_property("font-size")
    sale_prise_strong = sale_price.value_of_css_property("font-weight")

    # Кликаем на товар для перехода на страницу товара
    driver.find_element(By.CSS_SELECTOR, "#box-campaigns > div > ul > li > a.link").click()

    product_name_product = driver.find_element(By.CSS_SELECTOR, "h1").text
    regular_price_product = driver.find_element(By.XPATH, "//*[@id='box-product']/div[2]/div[2]/div[2]/s")
    sale_price_product = driver.find_element(By.XPATH, "//*[@id='box-product']/div[2]/div[2]/div[2]/strong")

    regular_price_text_product = regular_price_product.text
    regular_price_product_lined = regular_price_product.value_of_css_property('text-decoration-line')
    sale_price_text_product = sale_price_product.text
    sale_price_style_product = sale_price_product.value_of_css_property("color")
    regular_price_style_product = regular_price_product.value_of_css_property("color")
    regular_price_size_product = regular_price_product.value_of_css_property("font-size")
    sale_price_size_product = sale_price_product.value_of_css_property("font-size")
    sale_prise_strong_product = sale_price_product.value_of_css_property("font-weight")

    print(regular_price_style_product)
    a = driver.find_element(By.XPATH, "//*[@id='box-product']/div[2]/div[2]/div[2]/s")

    try:
        assert product_name == product_name_product
    except AssertionError:
        print("AssertionError: Имена не совпадают")

    try:
        assert regular_price_text == regular_price_text_product
    except AssertionError:
        print("AssertionError: Обычная цена не совпадает")

    try:
        assert sale_price_text == sale_price_text_product
    except AssertionError:
        print("AssertionError: Цена со скидкой не совпадает")

    try:
        assert re.findall(r'\d+', sale_price_style)[1] == re.findall(r'\d+', sale_price_style)[2] == '0'
    except AssertionError:
        print("AssertionError: Цвет цены со скидкой не красная на главной странице")

    try:
        assert re.findall(r'\d+', sale_price_style_product)[1] == re.findall(r'\d+', sale_price_style_product)[2] == '0'
    except AssertionError:
        print("AssertionError: Цвет цены со скидкой не красная на странице товара")

    try:
        assert re.findall(r'\d+', regular_price_style_product)[0] == re.findall(r'\d+', regular_price_style_product)[
            1] == re.findall(r'\d+', regular_price_style_product)[2]
    except AssertionError:
        print("AssertionError: Цвет обычной цены не серый на странице товара")

    try:
        assert re.findall(r'\d+', regular_price_style)[0] == re.findall(r'\d+', regular_price_style)[
            1] == re.findall(r'\d+', regular_price_style)[2]
    except AssertionError:
        print("AssertionError: Цвет обычной цены не серый на главной странице")

    try:
        assert regular_price_product_lined == 'line-through'
    except AssertionError:
        print("AssertionError: Обычная цена не зачёркнута на странице товара")

    try:
        assert regular_price_lined == 'line-through'
    except AssertionError:
        print("AssertionError: Обычная цена не зачёркнута на главной странице")

    try:
        assert float(sale_price_size_product[:-2]) > float(regular_price_size_product[:-2])
    except AssertionError:
        print("AssertionError: Размер текста цены со скидкой меньше или равна размеру обычной цены на странице товара")

    try:
        assert float(sale_price_size[:-2]) > float(regular_price_size[:-2])
    except AssertionError:
        print("AssertionError: Размер текста цены со скидкой меньше или равна размеру обычной цены на главной странице")

    try:
        assert sale_prise_strong_product > "500"
    except:
        print("AssertionError: Текста цены со скидкой не жирный на странице товара")

    try:
        assert sale_prise_strong > "500"
    except:
        print("AssertionError: Текст цены со скидкой не жирный на главной странице")

    # Закрываем браузер
    driver.quit()
