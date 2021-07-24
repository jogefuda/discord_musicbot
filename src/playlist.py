import time
import discord
from YTDL import YTDL_Wrapper
from utils import truncate, process_bar

class LoopMode(Enum):
    NORMAL = 0,
    LIST = 1,
    SINGLE = 2,

class PlayListEntry:
    def __init__(self, uri: str, lazy=True):
        self.uri = uri
        self._touchat = 0

        if not lazy:
            self.fetch_info()
    
    def fetch_info(self):
        if self.cache_avaiable():
            return None
        try:
            info = YTDL_Wrapper.query(self.uri)
        except Exception as e:
            return e

        self.id = info.get('id', None)
        self.title = info.get('title', '<No Title>'),
        self.real_uri = info.get('url', None),
        self.image_url = info.get('thumbnail', None),
        self.duration = info.get('duration', 0)
        self._touchat = time.time()
        return None

    def cache_avaiable(self):
        # cache at least 60 minutes maybe we can go further
        return (time.time() - self._touchat) < (60 * 60) 

class PlayList:
    def __init__(self, name: str='Unnamed', loop: LoopMode=LoopMode.NORMAL):
        self.name = name
        self.loop = loop
        self._list = []
        self._index = 0
    
    def add_entry(self, uri: str):
        self._list.append(PlayListEntry(uri))

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


class PlayListPagger:
    @classmethod
    def get_pagged_list(cls, playlist: PlayList, page: int=None, item_per_page: int=9):
        current_index = playlist._index
        total_pages = len(playlist.get_entries()) // item_per_page
        page = page or (current_index // item_per_page)
        embed = discord.Embed(title='', color=0xffffd5)
        embed.add_field(name='Title', value=process_bar(10), inline=False)
        start, end = (page * item_per_page), min((page + 1) * item_per_page, len(playlist.get_entries()))
        for i in range(start, end):
            name = str(i+1)
            entry = playlist.get_entries()[current_index-1]
            if i == current_index % 9 - 1:
                name += '  :notes: '
            embed.add_field(name=name, value=truncate('[{}](http://youtube.com)'.format(entry.uri)), inline=True)
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