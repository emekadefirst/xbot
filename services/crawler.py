import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from .recent import Tweet
from .response import generate_reply
from .__init__ import scroll_page

def parse_tweets(content, driver, signal_time):
    soup = BeautifulSoup(content, 'html.parser')
    for tweet in soup.find_all('article'):
        account = tweet.find('a', {'class': 'css-175oi2r r-1wbh5a2 r-dnmrzs r-1ny4l3l r-1loqt21'})
        user = account.get('href') if account else 'username not found'
        link = tweet.find('a', {'class': 'css-146c3p1 r-bcqeeo r-1ttztb7 r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-16dba41 r-xoduu5 r-1q142lx r-1w6e6rj r-9aw3ui r-3s2u2q r-1loqt21'})
        url = f'https://x.com{link.get("href")}' if link else 'URL not found'
        print(url)        
        content = tweet.find('div', {'data-testid': 'tweetText'}).text.strip() if tweet.find('div', {'data-testid': 'tweetText'}) else 'Content not found'
        print(content)
        
        time_s = tweet.find('time')
        if time_s:
            created_at = time_s.get('datetime')
            parsed_time = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M:%S")
            print(parsed_time)
        else:
            parsed_time = 'Time not found'

        tweet_obj = Tweet(user, parsed_time, content, url, signal_time)
        status = tweet_obj.is_recent()
        print(status)
        
        if status == True:
            post_comment(driver, tweet_obj)

def post_comment(driver, tweet_obj):
    driver.get(tweet_obj.url)
    scroll_page(driver, 1)
    comment = generate_reply(tweet_obj.content)
    comment = "Test 2 "
    time.sleep(5)
    
    # Locate the reply button using the combination of class name and data-testid
    reply_buttons = driver.find_elements(By.CLASS_NAME, 'css-175oi2r')
    reply_button = None
    for button in reply_buttons:
        if button.get_attribute('data-testid') == 'reply':
            reply_button = button
            break
    
    if reply_button:
        reply_button.click()  
        time.sleep(5)
        
        # Locate the reply text area and send the comment
        type_reply = driver.find_element(By.CLASS_NAME, 'public-DraftStyleDefault-block')
        time.sleep(5)
        type_reply.send_keys(comment)
        time.sleep(5)
        tweet_button = driver.find_element(By.CSS_SELECTOR, '[data-testid="tweetButton"]')
        tweet_button.click()
        print("Comment posted successfully!")
    else:
        print("Failed to find the reply button")

