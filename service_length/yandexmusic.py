from yandex_music import Client
from typing import Optional

from service_length import ServiceABC


class YandexMusic(ServiceABC):
    def __init__(self, yandex_music: Client):
        self.yandex_music = yandex_music

    def get_length_track(self, title: str, artist: str, album: Optional[str] = None) -> Optional[int]:
        result_search = self.yandex_music.search(f'{artist} - {title}')
        if result_search.tracks is None:
            return None

        find_track = result_search.tracks.results[0]

        if title.lower() != find_track.title.lower():
            return None

        if artist.lower() not in [i.name.lower() for i in find_track.artists]:
            return None

        return find_track.duration_ms // 1000
