import discord
import time
from asyncio import Event
from playlist import PlayList, PlayListPager
import asyncio

class SimplePlayer:
    def __init__(self, channel: discord.VoiceChannel, playlist: PlayList=None):
        self.channel: discord.VoiceChannel = channel
        self.voice_client: discord.VoiceClient = None 
        self.playlist = playlist or PlayList()
        self._status_message = None
        self._next = Event()
        self._time = None  # TODO: for time status, currently not used
    
    async def spawn_status_message(self, channel: discord.TextChannel, force: bool=False):
        if self._status_message and not force:
            await self.update_status_message()
            return
        if self._status_message:
            await self._status_message.delete()
        message = await channel.send('< PLACE HOLDER >')
        self._status_message = message
        await self.update_status_message()

    async def update_status_message(self):
        if self._status_message:
            await self._status_message.edit(embed=PlayListPager.get_pagged_list(self.playlist))

    async def play(self):
        if self.is_playing():
            return

        if not self.voice_client or not self.voice_client.is_connected():
            self.voice_client = await self.channel.connect()

        self.playlist.goto(0) # playlist start from first entry
        while not self.playlist.empty():
            def finalize(err: discord.ClientException):
                self._next.set()

            self._next.clear()
            entry = self.playlist.next()
            if not entry:
                break
            
            err = entry.fetch_info()
            if err:
                continue
            FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'}
            self.voice_client.play(discord.FFmpegPCMAudio(entry.real_uri[0], pipe=False, **FFMPEG_OPTIONS), after=finalize)
            await self.update_status_message()
            await asyncio.sleep(3) # prevent flooding discord server if playlist has serious fail
            await self._next.wait()
            self._time = time.time()
        await self.stop()
    
    async def stop(self, leave: bool=True):
        if self.voice_client and self.voice_client.is_connected():
            self.voice_client.stop()

            if leave:
                await self.voice_client.disconnect()
                if self._status_message:
                    await self._status_message.delete()

    def is_playing(self):
        return self.voice_client and self.voice_client.is_playing()

    def pause(self, toggle: bool=True):
        if self.voice_client:
            if self.voice_client.is_paused() and toggle:
                self.voice_client.resume()
            else:
                self.voice_client.pause()

    async def next(self):
        self.playlist.next(force=True)
        await self.stop(leave=False)

    async def prev(self):
        self.playlist.prev()
        await self.stop(leave=False)