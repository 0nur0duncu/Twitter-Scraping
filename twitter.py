import time
import json
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import logging
import random

class TwitterMonitor:
    def __init__(self, accounts):
        self.accounts = accounts
        self.last_tweets_file = 'last_tweets.json'
        self.tweets_log_file = 'tweets_log.txt'
        self.last_tweets = self.load_last_tweets()
        self.setup_driver()
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('twitter_monitor.log'),
                logging.StreamHandler()
            ]
        )

    def setup_driver(self):
        options = Options()
        ua = UserAgent()
        options.add_argument(f'user-agent={ua.random}')
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-infobars')
        
        self.driver = webdriver.Chrome(options=options)
        self.driver.set_page_load_timeout(30)

    def load_last_tweets(self):
        if os.path.exists(self.last_tweets_file):
            with open(self.last_tweets_file, 'r') as f:
                return json.load(f)
        return {account: None for account in self.accounts}

    def save_last_tweets(self):
        with open(self.last_tweets_file, 'w') as f:
            json.dump(self.last_tweets, f)

    def log_tweet(self, account, tweet_info):
        with open(self.tweets_log_file, 'a', encoding='utf-8') as f:
            f.write(f"\nAccount: {account}\n")
            f.write(f"Text: {tweet_info['text']}\n")
            f.write(f"Link: {tweet_info['link']}\n")
            f.write(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("-" * 50 + "\n")

    def extract_tweet_info(self, tweet_element, account):
        try:
            tweet_link = tweet_element.find_element(By.CSS_SELECTOR, 'a[href*="/status/"]').get_attribute('href')
            tweet_id = tweet_link.split('/status/')[1].split('?')[0]
            tweet_text = tweet_element.find_element(By.CSS_SELECTOR, '[data-testid="tweetText"]').text
            
            return {
                'id': tweet_id,
                'text': tweet_text,
                'link': tweet_link
            }

        except Exception as e:
            logging.error(f"Error extracting tweet info: {str(e)}")
            return None

    def check_account(self, account):
        try:
            self.driver.get(f'https://x.com/{account}')
            time.sleep(random.uniform(2, 4))

            tweet_elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'article[data-testid="tweet"]'))
            )

            if not tweet_elements:
                return

            latest_tweet = self.extract_tweet_info(tweet_elements[0], account)
            if not latest_tweet:
                return

            if self.last_tweets[account] != latest_tweet['id']:
                self.log_tweet(account, latest_tweet)
                logging.info(f"New tweet found from {account}")
                self.last_tweets[account] = latest_tweet['id']
                self.save_last_tweets()

        except Exception as e:
            logging.error(f"Error checking account {account}: {str(e)}")

    def monitor(self, interval=300):
        while True:
            try:
                for account in self.accounts:
                    self.check_account(account)
                    time.sleep(random.uniform(5, 10))
                
                logging.info("Completed checking all accounts")
                time.sleep(interval)

            except Exception as e:
                logging.error(f"Monitor error: {str(e)}")
                time.sleep(60)

    def __del__(self):
        try:
            self.driver.quit()
        except:
            pass

def main():
    accounts = [
        'cnbceofficial',
        'FintablesHaber',
        'fintables'
    ]
    
    monitor = TwitterMonitor(accounts)
    monitor.monitor()

if __name__ == "__main__":
    main()
