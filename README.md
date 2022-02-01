# BestBuy_BuyBot
A bot that can buy any item on BestBuy.com

## What Can It Do
* Log in to your account
* Check when an item is in stock
* Add item to cart as soon as it is in stock
* Change quanity of items in cart (in case your want more than one)
* Go to checkout
* Fill shipping and payment information
* Place order

## How To Setup and Usage
### Setup
1. Make a BestBuy account
2. Go to account settings and add a shipping address then set it as default (bot won't work without this step)
3. Download Chrome (if you don't have it) and chrome driver at https://sites.google.com/chromium.org/driver/downloads, make sure the one you download correstponds to your Chrome version (you can check your version in Chome settings > about Chrome > for me its 91.------)
4. Keep track of where you download the chrome driver, you will need the PATH of the chromedriver.exe for later
5. Clone this repository

### How to Use

1. Within the project files, go to BuyBot > dist > Main.exe. Run Main.exe by double clicking it. 
2. The program will open up a terminal window and will ask you to enter the path of the chrome driver exe file. (PATH should look similar to "C:\Users\JBeta\downloads\chromedriver.exe)
3. Next the program will ask about your item's url and BestBuy account email, password, ect.
4. It will also ask about payment information such as card number, expiration date, ect.
5. After you input the data, the bot will begin checking if the item is in stock and buy it when it is


## How to Modify
This program is setup to run as an exe file so user does not have to worry about getting a python interpreter. However, if you want to make edits to the code and continue to run the program as an exe file there are a few sets you can take.
1. Get all the items to run and write python code such as the python interpreter and an IDE if you don't want to use the defualt one.
2. Open the project and make your edits to the code
3. Now delete the dist folder in the BuyBot project files (you will replace that folder with next steps)
4. Next open a terminal window
5. Using the terminal, Navigate to the BuyBot project directory (use cd [next direcotry] if using command prompt)
6. In terminal, enter: python setup.py py2exe
7. The above command will make a new dist folder with an updated Main.exe with the code you wrote
8. Follow the "How to Use" section to learn to how run the program


## Running On Raspberry Pi W!ith Raspbian
1. Run: sudo apt install chromium-chromedriver
2. Remove: self.driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH). Replace with: self.driver = webdriver.Chrome(options=options)
