import traceback
import socket
import asyncio

from datetime import datetime

import discord
import steam.game_servers


class StatusCheck:

    def __init__(self, client, config):
        self.client = client
        self.config = config

        self.failed_checks = 0
        self.maintenance = False

    async def execute(self):
        try:
            status, activity = self.get_status()
            await self.client.change_presence(status=status, activity=activity)
            print(f'{datetime.now().isoformat()} {status} - {activity}')
        finally:
            await asyncio.sleep(30)
            self.client.loop.create_task(self.execute())

    def get_status(self):
        print('\nChecking status...')
        try:
            data = steam.game_servers.a2s_info(('147.135.85.168', 27015))

            if data['visibility']:
                self.maintenance = True
                return discord.Status.dnd, 'maintenance'
            else:
                game_str = f'{data["map"]} | {data["players"]} player' + ('s' if data["players"] != '1' else '')
                self.maintenance = False
                self.failed_checks = 0
                return discord.Status.online, discord.Game(name=game_str)

        except socket.timeout as error:
            print(error, f'Failed checks: {self.failed_checks}')
            self.failed_checks += 1
            if self.failed_checks == 4 and not self.maintenance:
                self.client.loop.create_task(self.alert_sleg())
                return discord.Status.dnd, None
            return None, None

    async def alert_sleg(self):
        sleg = await self.client.fetch_user(self.config['sleg.id'])
        channel = self.client.get_channel(self.config['sleg.channel.id'])
        await channel.send(f'{sleg.mention} Uwu whawt\'s thiws? I think the sewvew cwashed! Hewp me daddy squid!')
        print(f'{datetime.now().isoformat()} Alerted server crash!')
