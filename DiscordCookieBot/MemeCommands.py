from discord.ext import commands
from Music import MusicCommands


class MemeCommands:
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def zupnik(self):
        await self.client.say('Mega Faggot :eggplant:')

    @commands.command()
    async def simchoni(self):
        await self.client.say('Gets hard from rb6 :gay_pride_flag:')

    @commands.command()
    async def oded(self):
        await self.client.say('עודד חובץ כל יום :sweat_drops: :eggplant:')


def setup(client):
    client.add_cog(MemeCommands(client))
