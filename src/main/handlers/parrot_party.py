import asyncio

from datetime import datetime, timedelta

import discord


class ParrotParty:

    def __init__(self, client):
        self.client = client

        self.keywords = ['crumpets', 'horseradish', 'portugal', 'spam', 'login', 'crashed', 'avian',
                         'let\'s drop it', 'world', 'crux', 'noooo', 'dragon', 'died', 'parrot party']
        self.override = 'liek'
        self.cooldown = 30
        self.parrot_party_str = '<a:congaparrot:854214193289232424>' * 5

        self.last_party = datetime.min

    async def execute(self, message):
        if message.author == self.client.user:
            if ':congaparrot:' in message.content:
                await asyncio.sleep(2)
                await message.delete()
            return

        # only check public channels
        if message.channel.type != discord.ChannelType.text:
            return

        if any(keyword in message.content for keyword in self.keywords):
            print(f'{datetime.now().isoformat()} Parrot party triggered!')
            print(message.author, '-', message.content, message.jump_url)

            if (datetime.now() - self.last_party) > timedelta(minutes=self.cooldown) or self.override in message.content.lower():
                print(f'{datetime.now().isoformat()} Throwing parrot party!')

                await message.channel.send(content=self.parrot_party_str)
                self.last_party = datetime.now()
            else:
                print(f'{datetime.now().isoformat()} Parrot party is on cooldown for '
                      f'{self.cooldown - ((datetime.now() - self.last_party).seconds // 60)} minutes')
