import time
import discord
import math
from enum import Enum
from YTDL import YTDL_Wrapper
from utils import truncate, process_bar

class LoopMode(Enum):
    NORMAL = 0,
    LIST = 1,
    SINGLE = 2,

class PlayListEntry:
    def __init__(self, uri: str, discriminator: str, lazy=True):
        self.uri = uri
        self.discriminator = discriminator
        self._touchat = 0
        self._bad = False

        if not lazy:
            self.fetch_info()
    
    # TODO: return exception instead of fetched info seem weired
    def fetch_info(self):
        if self.cache_avaiable() and not self._bad:
            return None
        try:
            info = YTDL_Wrapper.query(self.uri)
        except Exception as e:
            self._bad = True # somethimes youtube return 403 Forbidden, so refresh url next time if possible
            return e

        self.id = info.get('id', None)
        self.title = info.get('title', '<No Title>'),
        self.real_uri = info.get('url', None),
        self.image_url = info.get('thumbnail', None),
        self.duration = info.get('duration', 0)
        self._touchat = time.time()
        self._bad = False
        return None

    def cache_avaiable(self):
        # cache at least 60 minutes maybe we can go further
        return (time.time() - self._touchat) < (60 * 60) 

    def set_bad(self, flag=True):
        self._bad = flag

class PlayList:
    def __init__(self, name: str='Unnamed', loop: LoopMode=LoopMode.NORMAL):
        self.name = name
        self.loop = loop
        self._list = []
        self._index = 0
    
    def add_entry(self, uri: str, discriminator: str=''):
        self._list.append(PlayListEntry(uri, discriminator))

    def get_entries(self):
        return self._list

    def clear_entries(self):
        self._list = []

    def goto(self, index):
        self._index = min(max(0, index), len(self._list)-1)

    def empty(self):
        return len(self._list) == 0

    def next(self, force=False):
        if self.empty():
            return None
        
        try:
            upnext = self._list[self._index]
        except IndexError as e:
            return None

        # only handle for single mode
        # for other mode voice_client.stop() is good enough.
        if force:
            if self.loop == LoopMode.SINGLE: 
                self._index += 1
            return
        
        if self.loop == LoopMode.NORMAL:
            self._index += 1
        elif self.loop == LoopMode.LIST:
            self._index = (self._index + 1) % len(self._list)
        
        return upnext

    def prev(self):
        self._index = max(0, self._index - 2)


class PlayListPager:
    @classmethod
    def get_pagged_list(cls, playlist: PlayList, page: int=None, item_per_page: int=9):
        current_index = max(0, playlist._index - 1)
        total_pages = math.ceil(len(playlist.get_entries()) / item_per_page)
        current_page = page or (current_index // item_per_page)
        embed = discord.Embed(title='', color=0xffffd5)
        paging_info = '[{}] {}/{} pages'.format(current_index + 1, current_page + 1, total_pages)
        embed.add_field(name='Title', value=paging_info, inline=False)
        start, end = (current_page * item_per_page), min((current_page + 1) * item_per_page, len(playlist.get_entries()))
        for i in range(start, end):
            entry = playlist.get_entries()[i]
            err = entry.fetch_info() # TODO: put this to background 
            name = '{}, #{}'.format(i+1, entry.discriminator)
            if i % 9 == current_index % 9:
                name += '  :notes:'

            prep = {}
            if entry._bad:
                name += '  :x:'
                prep = {
                    'uri': entry.uri,
                    'title': '<Fail to load>'
                }
            else:
                prep = {
                    'uri': entry.uri,
                    'title': truncate(entry.title[0])
                }
            embed.add_field(name=name, value='[{title}](https://youtube.com/watch?v={uri})'.format(**prep), inline=True)

        #time.strftime('%H:%M:%S', time.gmtime(12345))
        #bar = '{} {} {}'.format('00:00', process_bar(20, width=72), '00:00')
        #embed.add_field(name='', value='', inline=False)
        return embed








'''

playlists_path = '{}/{}'.format(os.path.dirname(__file__), 'playlists')
if not os.path.isdir(playlists_path):
    os.mkdir(playlists_path)

# TODO:  SECURITY ISSUE ??
def load(self, filename: str):
    path = os.path.relpath(playlists_path, filename)
    with open(path, 'r') as f:
        j = json.load(f)
        ## CONVERT TO OBJECT

def get_all(cls):
    playlists = [os.path.basename(path).split()[0] for path in os.listdir(playlists_path)]
    return playlists
'''