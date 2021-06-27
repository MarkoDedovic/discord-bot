import socket
import asyncio

from datetime import datetime

import discord
import steam.game_servers


SERVER_ONLINE = 'online'
SERVER_MAINTENANCE = 'maintenance'
SERVER_OFFLINE = 'offline'

class StatusCheck:

    def __init__(self, client, config):
        self.client = client
        self.config = config

        self.password_protected = False
        self.failed_checks = 0
        self.server_status = None

    async def execute(self):
        try:
            status, activity = self.get_status()
            if status == discord.Status.idle:
                await self.client.change_presence(status=status, activity=self.client.activity)
            else:
                await self.client.change_presence(status=status, activity=activity)

            print(f'{datetime.now().isoformat()} {status} - {activity}')
        finally:
            await asyncio.sleep(30)
            self.client.loop.create_task(self.execute())

    def get_status(self):
        print('\nChecking status...')
        try:
            data = steam.game_servers.a2s_info((self.config['ip'], self.config['port']))

            self.password_protected =  data['visibility']
            if self.password_protected:
                self.server_status = SERVER_MAINTENANCE
                return discord.Status.dnd, discord.Game('maintenance')
            else:
                game_str = f'{data["players"]} player{"s" if data["players"] != 1 else ""} | {data["map"]}'
                self.failed_checks = 0
                self.server_status = SERVER_ONLINE
                return discord.Status.online, discord.Game(name=game_str)

        except socket.timeout as error:
            print(error, f'Failed checks: {self.failed_checks}')
            self.failed_checks += 1
            if 3 < self.failed_checks:
                if self.failed_checks == 4:
                    if self.server_status == SERVER_ONLINE:
                        self.client.loop.create_task(self.send_crash_alerts())
                    self.server_status = SERVER_OFFLINE
                    return discord.Status.dnd, discord.Game('offline')
            return discord.Status.idle, None

    async def send_crash_alerts(self):
        for channel in self.config['channels_to_alert']:
            await self.client.get_channel(channel['id']).send(f'{channel["mention"]} help! I have crashed :(')
            print(f'{datetime.now().isoformat()} Alerted server crash!')
