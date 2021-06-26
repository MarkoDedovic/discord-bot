import asyncio
from datetime import datetime

from util import secrets_loader
from handlers.parrot_party import ParrotParty
from handlers.status_check import StatusCheck

import discord


class DiscordBot(discord.Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # TODO figure out a way to do this programatically so it can be stored in a config
        self.parrot_party = ParrotParty(self, kwargs['parrot_party_config'])
        self.status_check = StatusCheck(self, kwargs['status_check_config'])

        self.loop.create_task(self.background_tasks())

    async def on_ready(self):
        # TODO log in UTC time - also implement a proper logger
        print(f'{datetime.now().isoformat()} {self.user} is ready')

    async def on_message(self, message):
        await asyncio.gather(
            self.parrot_party.execute(message)
        )

    async def background_tasks(self):
        await self.wait_until_ready()
        await asyncio.gather(
            self.status_check.execute()
        )


if __name__ == '__main__':
    config = secrets_loader.get_secret('discord-bot')['prod']

    client = DiscordBot(parrot_party_config=config['parrotParty'], status_check_config=config['statusCheck'])
    client.run(config['botToken'])
