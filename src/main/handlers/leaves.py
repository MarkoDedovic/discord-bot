import asyncio
import random

from datetime import datetime, timedelta

import discord


ONGOING = 'ongoing'
MESSAGE_COUNT = 'message_count'
NUM_WAIT_MESSAGES = 'number_of_messages_to_wait_for'
LEAVES_SENT = 'leaves_sent'
TIMES_REPEAT = 'times_to_repeat'
CHANNEL = 'channel'
LAST_LEAVES = 'last_leaves'

class Leaves:

    def __init__(self, client, config):
        self.client = client
        self.config = config

        self.leaves_emoji = '🍃'
        self.leaves_alias = ':leaves:'
        self.leaves_destroyer = ':fire:'
        self.leaves_sources = ['🍃', '🌳']
        self.cooldown = 30

        self.server_vars = {}

    async def execute(self, message):
        if not message.guild.id in self.server_vars:
            self.server_vars[message.guild.id] = {}
            self.server_vars[message.guild.id][ONGOING] = False
            self.server_vars[message.guild.id][MESSAGE_COUNT] = 0
            self.server_vars[message.guild.id][NUM_WAIT_MESSAGES] = 5
            self.server_vars[message.guild.id][LEAVES_SENT] = 0
            self.server_vars[message.guild.id][TIMES_REPEAT] = 5
            self.server_vars[message.guild.id][CHANNEL] = message.channel
            self.server_vars[message.guild.id][LAST_LEAVES] = datetime.min

        if self.server_vars[message.guild.id][ONGOING] and message.channel == self.server_vars[message.guild.id][CHANNEL]:
            if self.leaves_emoji in message.content:
                self.server_vars[message.guild.id][MESSAGE_COUNT] = 0
            else:
                self.server_vars[message.guild.id][MESSAGE_COUNT] += 1

                if self.server_vars[message.guild.id][MESSAGE_COUNT] == self.server_vars[message.guild.id][NUM_WAIT_MESSAGES]:
                    if self.server_vars[message.guild.id][LEAVES_SENT] < self.server_vars[message.guild.id][TIMES_REPEAT]:
                        await self.server_vars[message.guild.id][CHANNEL].send(content=self.leaves_alias)
                        self.server_vars[message.guild.id][LEAVES_SENT] += 1
                        self.server_vars[message.guild.id][NUM_WAIT_MESSAGES] = random.choice(range(3,6))
                    elif self.server_vars[message.guild.id][LEAVES_SENT] == self.server_vars[message.guild.id][TIMES_REPEAT]:
                        await self.server_vars[message.guild.id][CHANNEL].send(content=random.choices((self.leaves_destroyer, random.choice(self.config['GIFs'])), weights=[90, 10])[0])
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
            elif not message.channel.permissions_for(message.guild.get_member(self.client.user.id)).send_messages:
                print('No permission to send messages in this channel!')
            else:
                print(f'{datetime.now().isoformat()} Throwing leaves!')
                self.server_vars[message.guild.id][CHANNEL] = message.channel
                self.server_vars[message.guild.id][TIMES_REPEAT] = random.choices((random.choice(range(1, 10)), 30), weights=[95, 5])[0]
                self.server_vars[message.guild.id][NUM_WAIT_MESSAGES] = random.choice(range(3,6))
                self.server_vars[message.guild.id][ONGOING] = True
                self.server_vars[message.guild.id][LAST_LEAVES] = datetime.now()
