from typing import Optional

from lastfmapi import LastFMAPI, LastFMAPIError
from service_length import ServiceABC


class LastFM(ServiceABC):
    def __init__(self, lastfm: LastFMAPI):
        self.lastfm = lastfm

    def get_length_track(self, title: str, artist: str, album: Optional[str] = None) -> Optional[int]:
        try:
            track_info = self.lastfm.get_info_track(title, artist)
        except LastFMAPIError:
            return None

        try:
            if int(track_info['duration']) == 0:
                return None
            # Convert ms to sec
            return int(track_info['duration']) // 1000
        except KeyError:
            return None

