from configparser import ConfigParser, NoOptionError
from datetime import datetime

from selenium import webdriver


class OutOfStockError(Exception):
    def __init__(self, message):
        self.message = message


class NotOnPageError(Exception):
    def __init__(self, message):
        self.message = message


class CaptchaError(Exception):
    def __init__(self, message):
        self.message = message


def print_timestamped(msg=""):
    print("[" + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "] " + str(msg))


class CheckOutBot():
    def __init__(self, config_file_loc, base_url, query_base_url, cart_base_url):
        print_timestamped("Starting Bot...")

        # Main URL's
        self.url = base_url
        self.query_base_url = query_base_url
        self.cart_base_url = cart_base_url

        parsed_config = ConfigParser()
        parsed_config.read(config_file_loc)

        # Product details
        self.SKUs = parsed_config.get("ITEM_INFO", "SKUs").replace(' ', '').strip('\"').split(",")

        # Account details
        self.username = parsed_config.get('ACCOUNT', 'USERNAME').strip('\"')
        self.password = parsed_config.get('ACCOUNT', 'PASSWORD').strip('\"')

        # Card details
        self.card = parsed_config.get('CARD_INFO', 'CARD_NUM').strip('\"')
        self.card_security = parsed_config.get('CARD_INFO', 'SEC_CODE').strip('\"')
        self.exp_m = parsed_config.get('CARD_INFO', 'EXP_M').strip('\"')
        self.exp_y = parsed_config.get('CARD_INFO', 'EXP_Y').strip('\"')

        # Bot Options
        self.poll_rate = 1200  # TODO: pull these from config.
        self.poll_rate = parsed_config.getfloat('BOT_OPTIONS', 'POLL_PERIOD_S')
        self.max_fails = 100000

        try:
            self.ID = parsed_config.get('ACCOUNT', 'MEMBER_ID').strip('\"')
        except NoOptionError as e:
            self.ID = "none"
            print_timestamped("\tWarning, no MEMBER_ID was set in the config.ini. "
                              "This may not be required if you dont have one.")

        # Init Selenium
        self.driver = webdriver.Chrome()
        self.driver.get(self.url)
        print("\n")

    # Abstracts
    def login(self):
        raise NotImplementedError("The method not implemented")

    def check_in_stock(self, search_sku):
        raise NotImplementedError("The method not implemented")

    def add_to_cart(self, cart_btn):
        raise NotImplementedError("The method not implemented")

    def checkout(self):
        raise NotImplementedError("The method not implemented")

    # Non abstracts:
    def go_to_cart(self):
        self.enforce_on_domain(self.cart_base_url, self.cart_base_url)

    def search_sku(self, search_sku):
        self.driver.get(self.query_base_url + search_sku)

    def enforce_on_domain(self, domain, else_redirect):
        current_url = self.driver.current_url
        if (domain in current_url):
            return True
        else:
            self.driver.get(else_redirect)
            return False

    def enforce_on_url(self, domain, else_redirect):
        current_url = self.driver.current_url
        if (domain == current_url):
            return True
        else:
            self.driver.get(else_redirect)
            return False
