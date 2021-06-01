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
        # self.__PRODUCT = "https://www.bestbuy.com/site/razer-viper-mini-wired-optical-gaming-mouse-with-chroma-rgb-lighting-black/6402115.p?skuId=6402115"

        self.__EMAIL = "jbeta02@gmail.com" #TODO enter email
        self.__PASSWORD = "JBeta20041337" #TODO enter password

        self.__PAYMENt_INFO = "1111222233334444" #TODO enter credit or debit card num

        self.is_in_stock = False

        self.__checking_counter = 0
        self.__counter_mark = 1 # 3600 is equal to 1 hour in sec but bc I have a 2 sec delay this will be equal to 2 hours

        self.__item_count = "2" #TODO enter item count if not 2

        options = Options()
        options.headless = True
        options.add_argument("--window-size=1920,1200")
        options.add_argument("--lang=en")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/91.0.4472.77 Safari/537.36")

        # init browser driver
        DRIVER_PATH = "C:\\Users\\Acme\\Desktop\\webDriver\\chromedriver.exe" #TODO enter driver path
        self.driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)


    def login_in(self):
        self.driver.get("https://www.bestbuy.com/identity/global/signin")
        WebDriverWait(self.driver, 10).until(lambda x: "Sign In to Best Buy" in self.driver.title)

        # find element by class name
        email_input = self.driver.find_element_by_xpath('//*[@id="fld-e"]')
        password_input = self.driver.find_element_by_xpath('//*[@id="fld-p1"]')
        submit_button = self.driver.find_element_by_xpath("//button[contains(@class,'cia-form__controls__submit')]")

        email_input.send_keys(self.__EMAIL)
        password_input.send_keys(self.__PASSWORD)

        submit_button.click()

        try:
            WebDriverWait(self.driver, 90).until( # wait for you to actually get logged in
                lambda x: "Official Online Store" in self.driver.title
            )
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
            sleep(random.randrange(1, 5)) # add random delay to avoid spam detection
            self.__checking_counter += 1
            return False

    def add_to_cart(self):
        print("checking if in stock")

        while self.is_in_stock == False: # crummy code, but it works
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

        # comment out the following if only getting 1 item
        try:
            WebDriverWait(self.driver, 30).until(
                lambda x: self.driver.find_element_by_id(self.__get_item_name() + "-quantity").is_displayed()
            )
        except TimeoutException:
            # try again
            print("going to cart failed, trying again")
            self.go_to_cart()


        item_count_selector = self.driver.find_element_by_id(self.__get_item_name() + "-quantity")

        Select(item_count_selector).select_by_value(self.__item_count) # number of items

        sleep(5)


    def go_to_checkout(self):
        self.driver.get("https://www.bestbuy.com/checkout/r/fast-track")

        try:
            WebDriverWait(self.driver, 30).until(
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
        payment_input.send_keys(self.__PAYMENt_INFO)

        print("filled payment info")

        sleep(1)


    def place_order(self):

        place_order = self.driver.find_element_by_xpath("//button[@class='btn btn-lg btn-block btn-primary'][1]")
        place_order.click()

        print("order placed")

        raise SystemExit()


    def __get_item_name(self):
        list = self.__PRODUCT.split("/")

        return list[4]