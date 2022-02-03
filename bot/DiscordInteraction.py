
from discord.ext import tasks

import discord

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    async def on_ready(self):
        print("__________BuyBot: " + f'Logged in as {self.user}')

        channel = self.get_channel(796599418710523937)  # channel ID goes here
        await channel.send("@everyone The 3080 might by IN STOCK. Check by going to  https://www.bestbuy.com/site/nvidia-geforce-rtx-3080-10gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6429440.p?skuId=6429440")
