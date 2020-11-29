import time
from configparser import ConfigParser
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Constants
BBY_URL = 'https://www.walmart.com/'

RE_SIGN_IN_URL = 'https://www.walmart.com/account/login'
SIGN_IN_URL = 'https://www.walmart.com/account/login?tid=0&returnUrl=%2F'

SRC_SKU_URL = 'https://affil.walmart.com/cart/addToCart?items='
IN_STK_TXT = 'to Cart'
BTN_CLASS = 'add-to-cart-button'
SKU_ATTR = 'data-sku-id'
CART_URL = 'https://www.bestbuy.com/cart'

class OutOfStockError(Exception):
    def __init__(self, message):
        self.message = message


class NotOnPageError(Exception):
    def __init__(self, message):
        self.message = message


class BBYbot():
    def __init__(self, config):

        self.driver = webdriver.Chrome()
        self.url = BBY_URL

        # Product details
        self.SKUs = config.get('ITEM_INFO', 'SKUs').replace(' ', '').strip('\"').split(",")

        # Account details
        self.username = config.get('WM_ACCOUNT', 'USERNAME').strip('\"')
        self.password = config.get('WM_ACCOUNT', 'PASSWORD').strip('\"')
        self.ID = config.get('WM_ACCOUNT', 'ID').strip('\"')

        # Card details
        self.card = config.get('CARD_INFO', 'CARD#').strip('\"')
        self.card_security = config.get('CARD_INFO', 'CARDSECURITY').strip('\"')
        self.exp_m = config.get('CARD_INFO', 'EXPM').strip('\"')
        self.exp_y = config.get('CARD_INFO', 'EXPY').strip('\"')

        self.driver.get(self.url)

    def login(self):
        self.enforce_on_domain(RE_SIGN_IN_URL, SIGN_IN_URL)
        timeout = 5

        username_input = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.ID, 'email')))
        username_input.send_keys(self.username)
        time.sleep(0.25)
        password_input = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.ID, 'password')))
        password_input.send_keys(self.password)
        password_input.submit()

    def enforce_on_domain(self, domain, else_redirect):
        current_url = self.driver.current_url
        if (domain in current_url):
            return True
        else:
            self.driver.get(else_redirect)
            return False

    def search_sku(self, search_sku):
        self.enforce_on_domain(BBY_URL, BBY_URL)
        searchbar = self.driver.find_element_by_class_name('search-input')
        searchbar.send_keys(search_sku)
        searchbar.submit()

    def go_to_sku(self, search_sku):
        new_url = SRC_SKU_URL + search_sku
        self.driver.get(new_url)

    def in_stock(self, search_sku):
        if (search_sku not in self.driver.current_url):
            raise NotOnPageError("Error! Not on correct webpage for [" + search_sku + "].")
        else:
            timeout = 5
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, BTN_CLASS)))

        all_checkouts = self.driver.find_elements_by_class_name(BTN_CLASS)
        matching_checkouts = list(filter(lambda btn: btn.get_attribute(SKU_ATTR) == search_sku, all_checkouts))
        in_stock_checkouts = list(filter(lambda btn: IN_STK_TXT in btn.text, matching_checkouts))

        if (len(all_checkouts) == 0 or len(matching_checkouts) == 0):
            raise NotOnPageError("ERROR! Could not find element corresponding to [" + search_sku + "] on this page.")
        elif (len(in_stock_checkouts) == 0):
            raise OutOfStockError("Item [" + search_sku + "] is out of stock")
        else:
            print("Item [" + search_sku + "] is in stock!!")
            return in_stock_checkouts[0]

    def add_to_cart(self, cart_btn):
        cart_btn.click()
        # TODO check for success by change in number next to cart icon

    def checkout(self):
        timeout = 500
        self.enforce_on_domain(CART_URL, CART_URL)

        time.sleep(5)
        btn = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, "button--primary")))
        btn.click()

        time.sleep(3)
        btn2 = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, "button--primary")))
        btn2.click()
        print_timestamped("Checkout complete!")
        time.sleep(300)

    def close_email_prompt(self):
        self.driver.find_element_by_class_name("c-modal-close-icon").click()

    def is_in_stock(self, text):
        return 'Item out of stock' not in text

    def close(self):
        self.driver.close()


def print_timestamped(msg=""):
    print("[" + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "] " + str(msg))

print_timestamped("Starting Bot...")
config_file = ConfigParser()
config_file.read("configs/wm.config.ini")
bot = BBYbot(config_file)
print_timestamped("Logging-in:")
logged_in = False
login_fail_count = 0
log_in_backoff = (60) # seconds
while (not logged_in and login_fail_count < 5):
    start_time = time.time()
    try:
        bot.login()
    except:
        print_timestamped("\tLog-in failed!")
        login_fail_count += 1
        if (login_fail_count < 5):
            print_timestamped('\t' + "Waiting " + str(log_in_backoff) + "s to try again.")
            time.sleep(log_in_backoff)
    else:
        logged_in = True
        print_timestamped("\tLog-in succeeded!\n")

print_timestamped("Checking for in-stock SKUs:")
time.sleep(3)

in_stock = False
stock_fail_count = 1
check_stock_period = (15)  # seconds

while (in_stock is False):
    start_time = time.time()
    print_timestamped("\t[" + str(stock_fail_count) + "] Checking For Restock")
    for sku in bot.SKUs:
        try:
            bot.driver.get(SRC_SKU_URL + sku)
            time.sleep(2)
            in_stock = bot.is_in_stock(bot.driver.find_element_by_xpath("//body").get_attribute('outerHTML'))
        except OutOfStockError as e:
            #print('\t' + str(e))
            pass
        except NotOnPageError as e:
            print_timestamped('\t' + str(e))
        except Exception as e:
            print_timestamped('\t' + str(e))
        else:
            pass

    wait_time = max(check_stock_period - (time.time() - start_time), 0)
    stock_fail_count += 1
    if (not in_stock and wait_time > 1.0):
        # print('\t' + "[" + str(stock_fail_count) + "]Waiting " + str(round(wait_time)) + "s.")
        time.sleep(wait_time)

print_timestamped("Adding in-stock item(s) to cart:")
bot.checkout()

# print_timestamped("Starting Checkout!")
# bot.checkout()
# print_timestamped("\tCompleted Checkout!")
# bot.close()
