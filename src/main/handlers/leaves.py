import asyncio
import random

from datetime import datetime, timedelta

import discord


CONFIG_COOLDOWN = 'cooldown'
CONFIG_GIFS = 'GIFs'

ONGOING = 'ongoing'
MESSAGE_COUNT = 'message_count'
NUM_WAIT_MESSAGES = 'number_of_messages_to_wait_for'
LEAVES_SENT = 'leaves_sent'
TIMES_REPEAT = 'times_to_repeat'
LAST_LEAVES = 'last_leaves'

class Leaves:

    def __init__(self, client, config):
        self.client = client
        self.config = config

        self.leaves_emoji = '🍃'
        self.leaves_alias = ':leaves:'
        self.leaves_destroyer = ':fire:'
        self.leaves_sources = ['🍃', '🌳']

        self.channel_vars = {}

    async def execute(self, message):
        if not message.channel.id in self.channel_vars:
            self.channel_vars[message.channel.id] = {}
            self.channel_vars[message.channel.id][ONGOING] = False
            self.channel_vars[message.channel.id][MESSAGE_COUNT] = 0
            self.channel_vars[message.channel.id][NUM_WAIT_MESSAGES] = 5
            self.channel_vars[message.channel.id][LEAVES_SENT] = 0
            self.channel_vars[message.channel.id][TIMES_REPEAT] = 5
            self.channel_vars[message.channel.id][LAST_LEAVES] = datetime.min

        if self.channel_vars[message.channel.id][ONGOING]:
            if self.leaves_emoji in message.content:
                self.channel_vars[message.channel.id][MESSAGE_COUNT] = 0
            else:
                self.channel_vars[message.channel.id][MESSAGE_COUNT] += 1

                if self.channel_vars[message.channel.id][MESSAGE_COUNT] == self.channel_vars[message.channel.id][NUM_WAIT_MESSAGES]:
                    if self.channel_vars[message.channel.id][LEAVES_SENT] < self.channel_vars[message.channel.id][TIMES_REPEAT]:
                        await message.channel.send(content=self.leaves_alias)
                        self.channel_vars[message.channel.id][LEAVES_SENT] += 1
                        self.channel_vars[message.channel.id][NUM_WAIT_MESSAGES] = random.choice(range(3,6))
                    elif self.channel_vars[message.channel.id][LEAVES_SENT] == self.channel_vars[message.channel.id][TIMES_REPEAT]:
                        await message.channel.send(content=random.choices((self.leaves_destroyer, random.choice(self.config[CONFIG_GIFS])), weights=[90, 10])[0])
                        self.channel_vars[message.channel.id][ONGOING] = False
                        self.channel_vars[message.channel.id][LEAVES_SENT] = 0
                    self.channel_vars[message.channel.id][MESSAGE_COUNT] = 0

        if any(leaves_source in message.content for leaves_source in self.leaves_sources):
            print(f'{datetime.now().isoformat()} Leaves triggered!')
            print(message.author, '-', message.content, message.jump_url)

            if (datetime.now() - self.channel_vars[message.channel.id][LAST_LEAVES]) < timedelta(minutes=self.config[CONFIG_COOLDOWN]):
                print(f'{datetime.now().isoformat()} Leaves is on cooldown for '
                    f'{self.config[CONFIG_COOLDOWN] - ((datetime.now() - self.channel_vars[message.channel.id][LAST_LEAVES]).seconds // 60)} minutes')
            elif self.channel_vars[message.channel.id][ONGOING]:
                print('Another leaves is currently still going!')
            elif not message.channel.permissions_for(message.guild.get_member(self.client.user.id)).send_messages:
                print('No permission to send messages in this channel!')
            else:
                print(f'{datetime.now().isoformat()} Throwing leaves!')
                self.channel_vars[message.channel.id][TIMES_REPEAT] = random.choices((random.choice(range(1, 10)), 30), weights=[95, 5])[0]
                self.channel_vars[message.channel.id][NUM_WAIT_MESSAGES] = random.choice(range(3,6))
                self.channel_vars[message.channel.id][ONGOING] = True
                self.channel_vars[message.channel.id][LAST_LEAVES] = datetime.now()
