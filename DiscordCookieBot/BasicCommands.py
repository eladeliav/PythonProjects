from discord.ext import commands


class BasicCommands:
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self):
        await self.client.say('Pong!')

    @commands.command()
    async def prefix(self, args='!'):
        if not args:
            return
        self.client.command_prefix = args
        await self.client.say("New command prefix: {}".format(args))

    @commands.command()
    async def math(self, args):
        result = eval(args)
        await self.client.say('{} = {}'.format(args, result))

    @commands.command(pass_context=True)
    async def clear(self, ctx, amount=100):
        channel = ctx.message.channel
        messages = []
        async for message in self.client.logs_from(channel, limit=int(amount)):
            messages.append(message)
        await self.client.delete_messages(messages)

    @commands.command(pass_context=True)
    async def join(self, ctx):
        channel = ctx.message.author.voice.voice_channel
        await self.client.join_voice_channel(channel)

    @commands.command(pass_context=True)
    async def leave(self, ctx):
        server = ctx.message.server
        voice_client = self.client.voice_client_in(server)
        await voice_client.disconnect()


def setup(client):
    client.add_cog(BasicCommands(client))
