from typing import Optional

from lastfmstatistics import LastFMAPI, LastFMAPIError
from service_length import ServiceABC


class LastFM(ServiceABC):
    def __init__(self, lastfm: LastFMAPI):
        self.lastfm = lastfm

    def get_length_track(self, title: str, artist: str, album: Optional[str]) -> Optional[int]:
        try:
            track_info = self.lastfm.get_info_track(title, artist)
        except LastFMAPIError:
            return None

        try:
            # Convert ms to sec
            return int(track_info['duration']) // 1000
        except KeyError:
            return None

