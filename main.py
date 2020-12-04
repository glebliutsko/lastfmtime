import datetime
import logging
from dataclasses import dataclass
from typing import Optional, List, TYPE_CHECKING

from yandex_music import Client as YMClient
import service_length
from lastfmstatistics import LastFMAPI

if TYPE_CHECKING:
    from service_length import ServiceABC

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@dataclass
class Track:
    mbid: Optional[str]
    date: datetime.datetime
    title: str
    artist: str
    album: str

    def __str__(self):
        return f'{self.artist} - {self.title}'

    def __repr__(self):
        return f'<{str(self)}>'


class LastFMTime:
    def __init__(self, lastfm_api: LastFMAPI, username: str, service: List[ServiceABC]):
        self.lastfm_api = lastfm_api
        self.username = username
        self.service = service

    def get_history_listen(self) -> List[Track]:
        page = 1
        tracks = list()

        while True:
            page_history = self.lastfm_api.get_recent_tracks(self.username, 1000, page)
            logger.info(f'Get page history {page}/{page_history["@attr"]["totalPages"]}')
            for track in page_history['track']:
                tracks.append(Track(
                    mbid=track['mbid'],
                    date=datetime.datetime.fromtimestamp(int(track['date']['uts'])),
                    title=track['name'],
                    artist=track['artist']['#text'],
                    album=track['album']['#text']
                ))

            if page >= int(page_history["@attr"]["totalPages"]):
                break

            page += 1

        return tracks


def main():
    lastfm_api = LastFMAPI('19ab4773cf02ed33bb1354017e3286ef')
    service = [service_length.LastFM(lastfm_api), service_length.YandexMusic(YMClient())]
    lastfm_time = LastFMTime(lastfm_api, 'glebliutsko', service)


if __name__ == '__main__':
    main()
