import os
import time
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def login(loader, email, password):
    url = 'https://x.com/i/flow/login'
    loader.get(url)
    time.sleep(5)
    if loader:
        login_input_1 = loader.find_element(By.CLASS_NAME, 'r-30o5oe')
        login_input_1.send_keys(email)
        login_input_1.send_keys(Keys.RETURN)
        time.sleep(30)
        login_input_2 = loader.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')
        login_input_2.send_keys(password)
        login_input_2.send_keys(Keys.RETURN)
        time.sleep(5)

