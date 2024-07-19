import os
import pickle

cookie_directory = "cookie"
os.makedirs(cookie_directory, exist_ok=True)

cookie_path = os.path.join(cookie_directory, 'cookies.pkl')

def save_cookies(driver, path):
    driver.get('https://x.com')
    with open(path, 'wb') as file:
        pickle.dump(driver.get_cookies(), file)

def load_cookies(driver, path):
    driver.get('https://x.com/login')
    with open(path, 'rb') as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            if 'domain' in cookie:
                driver.add_cookie(cookie)
            else:
                print(f"Skipping cookie without domain: {cookie}")
