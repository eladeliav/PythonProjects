import discord
from discord.ext import commands
import youtube_dl


class MusicCommands:
    def __init__(self, client):
        self.client = client
        self.PLAYERS = {}
        self.QUEUE = {}
        self.SONG_PLAYING = False

    def check_queue(self, server_id):
        if self.QUEUE[server_id]:
            player = self.QUEUE[server_id].pop(0)
            self.PLAYERS[server_id] = player
            player.start()
        else:
            self.SONG_PLAYING = False

    @commands.command(pass_context=True)
    async def play(self, ctx, url='https://www.youtube.com/watch?v=dQw4w9WgXcQ'):
        server = ctx.message.server
        voice_client = self.client.voice_client_in(server)
        if voice_client is None:
            await self.client.join_voice_channel(ctx.message.author.voice.voice_channel)
            voice_client = self.client.voice_client_in(server)
        ydl_opts = {'outtmpl': 'C:/downloadedsongs/%(title)s.%(ext)s',
                    'noplaylist': True, }
        if not self.SONG_PLAYING:
            player = await voice_client.create_ytdl_player(url, ytdl_options=ydl_opts,
                                                           after=lambda: self.check_queue(server.id))
            self.PLAYERS[server.id] = player
            player.start()
            await self.client.say('Video Playing.')
            self.SONG_PLAYING = True
        else:
            player = await voice_client.create_ytdl_player(url, ytdl_options=ydl_opts,
                                                           after=lambda: self.check_queue(server.id))

            if server.id in self.QUEUE:
                self.QUEUE[server.id].append(player)
            else:
                self.QUEUE[server.id] = [player]

            await self.client.say("Video Queued.")

    @commands.command(pass_context=True)
    async def play_playlist(self, ctx, url='https://www.youtube.com/watch?v=dQw4w9WgXcQ'):
        server = ctx.message.server
        voice_client = self.client.voice_client_in(server)
        if voice_client is None:
            await self.client.join_voice_channel(ctx.message.author.voice.voice_channel)
            voice_client = self.client.voice_client_in(server)
        ydl_opts = {'outtmpl': './downloadedsongs/%(title)s.%(ext)s',
                    'noplaylist': False, }
        if not self.SONG_PLAYING:
            player = await voice_client.create_ytdl_player(url, ytdl_options=ydl_opts,
                                                           after=lambda: self.check_queue(server.id))
            self.PLAYERS[server.id] = player
            player.start()
            await self.client.say('Video Playing.')
            self.SONG_PLAYING = True
        else:
            player = await voice_client.create_ytdl_player(url, ytdl_options=ydl_opts,
                                                           after=lambda: self.check_queue(server.id))

            if server.id in self.QUEUE:
                self.QUEUE[server.id].append(player)
            else:
                self.QUEUE[server.id] = [player]

            await self.client.say("Video Queued.")

    @commands.command(pass_context=True)
    async def queue(self, ctx):
        server = ctx.message.server
        number_in_queue = 1
        to_send = ""
        if not self.QUEUE or not self.QUEUE[server.id]:
            await self.client.say('Queue Empty')
            return
        for player in self.QUEUE[server.id]:
            to_send += '{}. {}\n'.format(number_in_queue, player.title)
            number_in_queue += 1
        await self.client.say(to_send)

    @commands.command(pass_context=True)
    async def reset_queue(self, ctx):
        server_id = ctx.message.server.id
        self.QUEUE[server_id] = []
        await self.client.say("Queue Empty")

    @commands.command(pass_context=True)
    async def stop(self, ctx):
        self.PLAYERS[ctx.message.server.id].stop()
        server = ctx.message.server
        voice_client = self.client.voice_client_in(server)
        await voice_client.disconnect()
        self.SONG_PLAYING = False

    @commands.command(pass_context=True)
    async def skip(self, ctx):
        self.PLAYERS[ctx.message.server.id].stop()

    @commands.command(pass_context=True)
    async def pause(self, ctx):
        self.PLAYERS[ctx.message.server.id].pause()
        self.SONG_PLAYING = False

    @commands.command(pass_context=True)
    async def resume(self, ctx):
        self.PLAYERS[ctx.message.server.id].resume()
        self.SONG_PLAYING = True


def setup(client):
    client.add_cog(MusicCommands(client))
