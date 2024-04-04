from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get('https://soreal.ru/uilyam-batler-jejts/')

text_area = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Введите слова для поиска"]')
link_next = driver.find_element(By.CSS_SELECTOR,"a[rel='next']")
link_next.click()
sleep(5)
driver.quit()

