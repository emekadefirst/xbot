import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def init_driver():
    return webdriver.Chrome()


def headless_driver():
    webdriver.Chrome()
    options = webdriver.ChromeOptions()
    options.add_argument("--headless") 
    loader = webdriver.Chrome(options=options)
    driver = loader.maximize_window()
    return driver

def scroll_page(driver, count):
    driver.maximize_window()
    window = driver.find_element(By.TAG_NAME, 'html')
    for _ in range(count):
        window.send_keys(Keys.PAGE_DOWN)
        time.sleep(2)
