
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep

from bot.DiscordInteraction import MyClient

def run():
    try:
        out_of_stock_button = driver.find_element_by_xpath(
            "//button[@class='c-button c-button-disabled c-button-lg c-button-block add-to-cart-button']")

        print(out_of_stock_button.text)
        sleep(1)
        driver.refresh()
        sleep(10)  # change to 5 min
        run()

    except:
        print("IN STOCK")
        client = MyClient()
        client.run('') # add discord bot token key
        client.close()

##################################################

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")
options.add_argument("--lang=en")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/91.0.4472.77 Safari/537.36")

# init browser driver
DRIVER_PATH = "C:\\Users\\Acme\\Desktop\\webDriver\\chromedriver.exe" # "C:\Users\Acme\Desktop\webDriver\chromedriver.exe"
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

driver.get("https://www.bestbuy.com/site/nvidia-geforce-rtx-3080-10gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6429440.p?skuId=6429440")

sleep(3)

print("checking if in stock")

run()
