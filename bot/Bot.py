from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep
import random

class BuyBot:

    def __init__(self):

        # below are private variables
        self.__PRODUCT = "https://www.bestbuy.com/site/nvidia-geforce-rtx-3080-10gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6429440.p?acampID=0&cmp=RMX&loc=Hatch&ref=198&skuId=6429440"
        # self.__PRODUCT = "https://www.bestbuy.com/site/sandisk-cruzer-16gb-usb-2-0-flash-drive-black/9226875.p?skuId=9226875"
        self.__PRODUCT_NAME = ""

        self.__EMAIL = ""
        self.__PASSWORD = ""

        self.__PAYMENT_CARD_NUMBER = ""
        self.__PAYMENT_EXDATE_MONTH = ""
        self.__PAYMENT_EXDATE_YEAR = ""
        self.__PAYMENT_CODE = ""

        self.is_in_stock = False

        self.__checking_counter = 0
        self.__counter_mark = 1 # 3600 is equal to 1 hour in sec but bc I have a 2 sec delay this will be equal to 2 hours

        self.__item_count = "2" #TODO enter item count if not 2

        self.__pass = False

        options = Options()
        options.headless = True
        options.add_argument("--window-size=1920,1200")
        options.add_argument("--lang=en")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/91.0.4472.77 Safari/537.36")

        # init browser driver
        DRIVER_PATH = input("Enter chromedriver.exe Path: ") # "C:\Users\Acme\Desktop\webDriver\chromedriver.exe"
        self.driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)


    def set_up(self):
        self.__EMAIL = input("Enter Email: ")
        self.__PASSWORD = input("Enter Password: ")
        self.__PAYMENT_CARD_NUMBER = input("Enter Credit or Debit Card Number: ")
        self.__PAYMENT_EXDATE_MONTH = input("Enter Card Expiration Date MONTH (2 digits): ")
        self.__PAYMENT_EXDATE_YEAR = input("Enter Card Expiration Date YEAR (2 digits): ")
        self.__PAYMENT_CODE = input("Enter 3 Digit Security Code: ")

    def login_in(self):
        self.driver.get("https://www.bestbuy.com/identity/global/signin")
        try:
            WebDriverWait(self.driver, 30).until(lambda x: "Sign In to Best Buy" in self.driver.title)
        except:
            print("getting to website to too long, trying again")
            self.login_in()

        # find element by class name
        email_input = self.driver.find_element_by_xpath('//*[@id="fld-e"]')
        password_input = self.driver.find_element_by_xpath('//*[@id="fld-p1"]')
        submit_button = self.driver.find_element_by_xpath("//button[contains(@class,'cia-form__controls__submit')]")

        email_input.send_keys(self.__EMAIL)
        password_input.send_keys(self.__PASSWORD)

        submit_button.click()

        try:
            WebDriverWait(self.driver, 90).until(  # wait for you to actually get logged in
                lambda x: "Official Online Store" in self.driver.title or "https://www.bestbuy.com/" == self.driver.current_url
            )
            sleep(3)
        except TimeoutException:
            # login failed try again
            print("login failed, trying again")
            self.login_in()
        print("successfully logged in")


    def in_stock(self):

        self.driver.get(self.__PRODUCT)

        try:
            add_to_cart_button = self.driver.find_element_by_xpath("//button[@class='btn btn-primary btn-lg btn-block btn-leading-ficon add-to-cart-button'][1]")

        except:
            add_to_cart_button = None

        if self.__checking_counter >= self.__counter_mark:
            print(".") # dot will represent about 2 hours but will always be more then bc of random delay
            self.__checking_counter = 0

        if add_to_cart_button != None and add_to_cart_button.is_enabled():
            # if add_to_cart_button exists and it is enabled then it is in stock
            print("is IN stock")
            self.is_in_stock = True
            return True
        else:
            self.driver.refresh()
            sleep(2) # allow for refresh
            sleep(random.randrange(1, 5)) # add random delay to avoid spam
            self.__checking_counter += 1
            return False

    def add_to_cart(self):
        print("checking if in stock")

        while self.is_in_stock == False:
            self.in_stock()

        if self.is_in_stock == True:
            print("adding to cart")

            self.driver.get(self.__PRODUCT)

            add_to_cart_button = self.driver.find_element_by_xpath("//button[@class='btn btn-primary btn-lg btn-block btn-leading-ficon add-to-cart-button'][1]")

            add_to_cart_button.click()

            try:
                WebDriverWait(self.driver, 90).until(
                    lambda x: self.driver.find_element_by_class_name("dot").is_displayed()
                )
                print("successfully added to cart")
            except TimeoutException:
                # failed try again
                print("adding to cart failed, trying again")
                self.add_to_cart()


    def go_to_cart(self):
        self.driver.get("https://www.bestbuy.com/cart")

        try:
            WebDriverWait(self.driver, 60).until(
                lambda x: self.driver.find_element_by_xpath("//select[@class='c-dropdown v-medium fluid-item__quantity']").is_displayed()
            )
            print("successfully put 2 items into cart")
            self.__pass = True

        except TimeoutException:
            # try again
            print("failed to add 2 items to cart, will just get 1") # if fail don't try again and just buy one
            self.__pass = False

        if self.__pass == True:

            item_count_selector = self.driver.find_element_by_xpath("//select[@class='c-dropdown v-medium fluid-item__quantity']")#self.driver.find_element_by_id(self.__PRODUCT_NAME + "-quantity")

            Select(item_count_selector).select_by_value(self.__item_count) # number of items

        sleep(5)


    def go_to_checkout(self):
        self.driver.get("https://www.bestbuy.com/checkout/r/fast-track")

        try:
            WebDriverWait(self.driver, 60).until(
                lambda x: self.driver.find_element_by_xpath(
                    "//button[@class='btn btn-lg btn-block btn-secondary'][1]").is_displayed()
            )
        except TimeoutException:
            # failed try again
            print("going to checkout failed, trying again")
            self.go_to_checkout()


    def fill_shipping(self):
        #TODO tell user to add house address as default shipping address

        self.driver.find_element_by_xpath("//button[@class='btn btn-lg btn-block btn-secondary'][1]").click()

        print("filled shipping info")

        try:
            WebDriverWait(self.driver, 90).until(
                lambda x: self.driver.find_element_by_xpath(
                    "//button[@class='btn btn-lg btn-block btn-primary'][1]").is_displayed()
            )
        except TimeoutException:
            # failed try again
            print("filled shipping failed, trying again")
            self.fill_shipping()


    def fill_payment(self):

        # fill payment info
        payment_input = self.driver.find_element_by_id("optimized-cc-card-number")
        payment_input.send_keys(self.__PAYMENT_CARD_NUMBER)

        sleep(2)

        month_selector = self.driver.find_element_by_name("expiration-month")
        Select(month_selector).select_by_value(self.__PAYMENT_EXDATE_MONTH)

        year_selector = self.driver.find_element_by_name("expiration-year")
        Select(year_selector).select_by_value("20"+self.__PAYMENT_EXDATE_YEAR)

        code_selector = self.driver.find_element_by_id("credit-card-cvv")
        code_selector.send_keys(self.__PAYMENT_CODE)

        print("filled payment info")

        sleep(1)


    def place_order(self):

        place_order = self.driver.find_element_by_xpath("//button[@class='btn btn-lg btn-block btn-primary'][1]")
        place_order.click()

        print("order placed")

        sleep(120)

        self.driver.quit()

        raise SystemExit()


    def __parse_item_name(self, name):
        name = name.replace("- ","")

        name = name.replace(" ", "-")

        print(name.lower())

        return name