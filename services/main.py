from .login import *
from .crawler import *
from .cookie import save_cookies, load_cookies, cookie_path
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
import time
import logging
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def init_driver(proxy_address=None):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    # options.add_argument('--headless')  
    if proxy_address:
        try:
            from .proxy import verify_proxy
            if verify_proxy(proxy_address):
                options.add_argument(f'--proxy-server=http://{proxy_address}')
            else:
                logger.warning(f"Proxy {proxy_address} failed verification. Proceeding without proxy.")
        except ImportError:
            logger.warning("proxy.py not found. Skipping proxy verification.")
        except Exception as e:
            logger.error(f"Error verifying proxy: {str(e)}. Proceeding without proxy.")
    
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(60) 
    return driver

def main(url, proxy, email, password):
    loader = None
    try:
        loader = init_driver(proxy)
        
        logger.info(f"Attempting to access {url}")
        try:
            loader.get('https://x.com')
        except Exception as e:
            logger.error(f"Error accessing https://x.com: {str(e)}")
            return  # Exit the function if we can't access the initial URL

        try:
            load_cookies(loader, cookie_path)
            loader.refresh()
            time.sleep(5)
            if "login" in loader.current_url:  
                logger.info("Login required. Attempting to log in.")
                login(loader, email, password)
                save_cookies(loader, cookie_path)
            else:
                logger.info("Already logged in.")
        except Exception as e:
            logger.error(f"Error during login process: {str(e)}")
            try:
                login(loader, email, password)
                save_cookies(loader, cookie_path)
            except Exception as login_error:
                logger.error(f"Failed to login: {str(login_error)}")
                return  

        logger.info(f"Accessing target URL: {url}")
        while True:
            try:
                loader.get(url)
                time.sleep(4)
                scroll_page(loader, 4)
                response = loader.page_source
                tweets = parse_tweets(response, loader)
                print(tweets)
                logger.info(f"Successfully parsed {len(tweets)} tweets")
                time.sleep(5)
            except Exception as e:
                logger.error(f"Error during tweet parsing: {str(e)}")
                break  # Exit the loop if an error occurs

    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
    finally:
        if loader:
            loader.quit()
            logger.info("Browser session closed")

# if __name__ == "__main__":
#     email = "your_email@example.com"  # Replace with actual email
#     password = "your_password"  # Replace with actual password
#     main('https://x.com/Mrfizzy_10', '47.251.28.148:8081', email, password)
