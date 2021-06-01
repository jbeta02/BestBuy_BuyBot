from bot import Bot

def main():
    BuyBot = Bot.BuyBot()

    print("")
    print("Buy Bot Activated")

    BuyBot.set_up()
    BuyBot.login_in()
    BuyBot.add_to_cart()
    BuyBot.go_to_cart()
    BuyBot.go_to_checkout()
    BuyBot.fill_shipping()
    BuyBot.fill_payment()
    #BuyBot.place_order()


# RUN CODE
main()