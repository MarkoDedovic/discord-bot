import asyncio
import random

from datetime import datetime, timedelta

import discord


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

        self.cooldown = 30
        self.leaves_str = ':leaves:'
        self.leaves_sources = ['🍃', '🌳']
        self.leaves_destroyer = ':fire:'

        self.server_vars = {}

    async def execute(self, message):
        if not message.guild.id in self.server_vars:
            self.server_vars[message.guild.id] = {}
            self.server_vars[message.guild.id][ONGOING] = False
            self.server_vars[message.guild.id][MESSAGE_COUNT] = 0
            self.server_vars[message.guild.id][NUM_WAIT_MESSAGES] = 5
            self.server_vars[message.guild.id][LEAVES_SENT] = 0
            self.server_vars[message.guild.id][TIMES_REPEAT] = 5
            self.server_vars[message.guild.id][LAST_LEAVES] = datetime.min

        if self.server_vars[message.guild.id][ONGOING]:
            if '🍃' in message.content:
                self.server_vars[message.guild.id][MESSAGE_COUNT] = 0
            else:
                self.server_vars[message.guild.id][MESSAGE_COUNT] += 1

                if self.server_vars[message.guild.id][MESSAGE_COUNT] == self.server_vars[message.guild.id][NUM_WAIT_MESSAGES]:
                    if self.server_vars[message.guild.id][LEAVES_SENT] < self.server_vars[message.guild.id][TIMES_REPEAT]:
                        await message.channel.send(content=self.leaves_str)
                        self.server_vars[message.guild.id][LEAVES_SENT] += 1
                        self.server_vars[message.guild.id][NUM_WAIT_MESSAGES] = random.choice(range(3,6))
                    elif self.server_vars[message.guild.id][LEAVES_SENT] == self.server_vars[message.guild.id][TIMES_REPEAT]:
                        await message.channel.send(content=random.choices((self.leaves_destroyer, random.choice(self.config['GIFs'])), weights=[90, 10])[0])
                        self.server_vars[message.guild.id][ONGOING] = False
                    self.server_vars[message.guild.id][MESSAGE_COUNT] = 0

        if any(leaves_source in message.content for leaves_source in self.leaves_sources):
            print(f'{datetime.now().isoformat()} Leaves triggered!')
            print(message.author, '-', message.content, message.jump_url)

            if (datetime.now() - self.server_vars[message.guild.id][LAST_LEAVES]) < timedelta(minutes=self.cooldown):
                print(f'{datetime.now().isoformat()} Leaves is on cooldown for '
                    f'{self.cooldown - ((datetime.now() - self.server_vars[message.guild.id][LAST_LEAVES]).seconds // 60)} minutes')
            elif self.server_vars[message.guild.id][ONGOING]:
                print('Another leaves is currently still going!')
            else:
                print(f'{datetime.now().isoformat()} Throwing leaves!')
                self.server_vars[message.guild.id][TIMES_REPEAT] = random.choices((random.choice(range(1, 10)), 30), weights=[95, 5])[0]
                self.server_vars[message.guild.id][NUM_WAIT_MESSAGES] = random.choice(range(3,6))
                self.server_vars[message.guild.id][ONGOING] = True
                self.server_vars[message.guild.id][LAST_LEAVES] = datetime.now()
