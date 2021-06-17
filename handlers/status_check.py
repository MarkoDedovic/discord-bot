import requests
import asyncio

from datetime import datetime

import discord


def get_status(data):
    try:
        map_name = data['map']
        playercount = data['playerscount'][:data['playerscount'].index('/')]
        game_str = f'{map_name} | {playercount} player' + 's' if playercount != '1' else ''

        print(datetime.now().isoformat(), game_str)
        return discord.Status.online, discord.Game(name=game_str)

    except KeyError as error:
        print(error, data)
        if data['playerscount'] == 'offline':
            return discord.Status.dnd, None

    except BaseException as error:
        print(error, data)
        return discord.Status.invisible, None


class StatusCheck:

    def __init__(self, client):
        self.client = client

    async def execute(self):
        # TODO stop using while True
        while True:
            print('\nChecking status...')

            try:
                data = requests.get('https://api.trackyserver.com/widget/index.php?id=300852').json()
                status, activity = get_status(data)
                await self.client.change_presence(status=status, activity=activity)
            except BaseException as error:
                print(datetime.now().isoformat(), error)
            finally:
                await asyncio.sleep(60)
