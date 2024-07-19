import time
import requests
from requests.exceptions import ProxyError, ConnectTimeout, HTTPError

def verify_proxy(proxy):
    test_url = "http://httpbin.org/ip"
    proxies = {
        "http": proxy,
        "https": proxy
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    start_time = time.time()
    try:
        response = requests.get(test_url, proxies=proxies, headers=headers, timeout=30)
        end_time = time.time()
        if response.status_code == 200:
            print(f"Proxy is working!")
            print(f"Response time: {end_time - start_time:.2f} seconds")
            print(f"Your IP address appears to be: {response.json()['origin']}")
            return True
        else:
            print(f"Proxy test failed. Status code: {response.status_code}")
            return False
    except ProxyError as e:
        print(f"Proxy test failed. ProxyError: {e}")
    except ConnectTimeout as e:
        print(f"Proxy test failed. ConnectTimeout: {e}")
    except HTTPError as e:
        print(f"Proxy test failed. HTTPError: {e}")
    except requests.RequestException as e:
        print(f"Proxy test failed. RequestException: {e}")
    return False

if __name__ == "__main__":
    proxy = "47.252.29.28:11222"  
    verify_proxy(proxy)
