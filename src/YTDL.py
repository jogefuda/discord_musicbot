import youtube_dl as yt

class YTDL_Wrapper:
    YDL_OPTIONS = {'format': 'bestaudio', 'extract_flat': True}
    @classmethod
    def query(cls, s: str):
        ytdl = yt.YoutubeDL(cls.YDL_OPTIONS)
        # TODO: handle exception and retry
        info = ytdl.extract_info(s, download=False)
        return info