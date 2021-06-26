import asyncio
import random

from datetime import datetime, timedelta

import discord


class ParrotParty:

    def __init__(self, client, config):
        self.client = client
        self.config = config

        self.cooldown = 30

        self.last_party = datetime.min

    async def execute(self, message):
        # only check public channels
        if message.channel.type != discord.ChannelType.text:
            return

        if any(keyword in message.content.lower() for keyword in self.config['keywords']):
            print(f'{datetime.now().isoformat()} Parrot party triggered!')
            print(message.author, '-', message.content, message.jump_url)

            if timedelta(minutes=self.cooldown) < (datetime.now() - self.last_party) or any(override in message.content.lower() for override in self.config['overrides']):
                print(f'{datetime.now().isoformat()} Throwing parrot party!')

                await message.channel.send(content=(random.choice(self.config['emojis']) * 5), delete_after=2)
                self.last_party = datetime.now()
            else:
                print(f'{datetime.now().isoformat()} Parrot party is on cooldown for '
                      f'{self.cooldown - ((datetime.now() - self.last_party).seconds // 60)} minutes')
