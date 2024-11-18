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
import urllib.request
from pathlib import Path

class TwitterMonitor:
    def __init__(self, accounts):
        self.accounts = accounts
        self.last_tweets_file = 'last_tweets.json'
        self.tweets_log_file = 'tweets_log.txt'
        self.images_folder = 'images'
        self.last_tweets = self.load_last_tweets()
        self.setup_driver()
        self.setup_logging()
        self.setup_folders()

    def setup_folders(self):
        # Resimler için klasör oluşturma
        Path(self.images_folder).mkdir(parents=True, exist_ok=True)

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

    def download_image(self, image_url, tweet_id, account):
        """Resmi indirip kaydetme fonksiyonu"""
        if not image_url:
            return None
        
        try:
            # Resim dosyası için isim oluşturma
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            image_extension = image_url.split('.')[-1].split('?')[0]
            if image_extension not in ['jpg', 'jpeg', 'png', 'gif']:
                image_extension = 'jpg'
            
            image_filename = f"{account}_{tweet_id}_{timestamp}.{image_extension}"
            image_path = os.path.join(self.images_folder, image_filename)
            
            # Resmi indirme
            headers = {'User-Agent': UserAgent().random}
            req = urllib.request.Request(image_url, headers=headers)
            with urllib.request.urlopen(req) as response, open(image_path, 'wb') as out_file:
                out_file.write(response.read())
            
            logging.info(f"Image downloaded successfully: {image_filename}")
            return image_path
            
        except Exception as e:
            logging.error(f"Error downloading image: {str(e)}")
            return None

    def log_tweet(self, account, tweet_info):
        # Resmi indirme
        image_path = self.download_image(
            tweet_info['image'], 
            tweet_info['link'].split('/status/')[1].split('?')[0],
            account
        )
        
        with open(self.tweets_log_file, 'a', encoding='utf-8') as f:
            f.write(f"\nAccount: {account}\n")
            f.write(f"Text: {tweet_info['text']}\n")
            f.write(f"Link: {tweet_info['link']}\n")
            f.write(f"Image: {image_path if image_path else 'No image'}\n")
            f.write(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("-" * 50 + "\n")

    def extract_tweet_info(self, tweet_element, account):
        try:
            tweet_link = tweet_element.find_element(By.CSS_SELECTOR, 'a[href*="/status/"]').get_attribute('href')
            tweet_text = tweet_element.find_element(By.CSS_SELECTOR, '[data-testid="tweetText"]').text
            
            # Resim URL'sini çekme işlemi
            image_elements = tweet_element.find_elements(By.CSS_SELECTOR, 'img[src*="media"]')
            image_url = None
            if image_elements:
                image_url = image_elements[0].get_attribute('src')
            
            return {
                'text': tweet_text,
                'link': tweet_link,
                'image': image_url
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

            tweet_id = latest_tweet['link'].split('/status/')[1].split('?')[0]
            if self.last_tweets[account] != tweet_id:
                self.log_tweet(account, latest_tweet)
                logging.info(f"New tweet found from {account}")
                self.last_tweets[account] = tweet_id
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
        'fintables',
        'binance',
        'Fenerbahce',
        '10ardaguler'
    ]
    
    monitor = TwitterMonitor(accounts)
    monitor.monitor()

if __name__ == "__main__":
    main()