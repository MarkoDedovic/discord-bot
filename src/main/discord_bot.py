import json
import asyncio
from datetime import datetime
import os

from util import secrets_loader
from handlers.parrot_party import ParrotParty
from handlers.status_check import StatusCheck

import discord


class DiscordBot(discord.Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # TODO figure out a way to do this programatically so it can be stored in a config
        self.parrot_party = ParrotParty(self)
        self.status_check = StatusCheck(self)

        self.first = True

    async def on_ready(self):
        # TODO log in UTC time - also implement a proper logger
        print(f'{datetime.now().isoformat()} {self.user} is ready')

        if self.first:
            self.first = False
            # start the background tasks after we connect the first time
            self.loop.create_task(self.background_tasks())

    async def on_message(self, message):
        await asyncio.gather(
            self.parrot_party.execute(message)
        )

    async def background_tasks(self):
        await asyncio.gather(
            self.status_check.execute()
        )

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

if __name__ == '__main__':
    config_file = open(os.path.join(__location__, 'config.json'))
    config = json.load(config_file)
    client = DiscordBot()
    if config['use.aws.secrets.manager']:
        config = json.loads(secrets_loader.get_secret('discord-bot'))
    client.run(config['discord.bot.token.dev' if config['use.dev.bot'] else 'discord.bot.token.prod'])
