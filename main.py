import datetime
import logging
from dataclasses import dataclass
from typing import Optional, List, TYPE_CHECKING

from yandex_music import Client as YMClient

import service_length
from lastfmapi import LastFMAPI
from statistics import Statistics

if TYPE_CHECKING:
    from service_length import ServiceABC

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
    def __init__(self, lastfm_api: LastFMAPI, username: str, services: List['ServiceABC']):
        self.lastfm_api = lastfm_api
        self.username = username
        self.services = services
        self.logger = logging.getLogger(self.__class__.__name__)

    def get_history_listen(self) -> List[Track]:
        page = 1
        tracks = list()

        while True:
            page_history = self.lastfm_api.get_recent_tracks(self.username, 1000, page)
            self.logger.info(f'Get page history {page}/{page_history["@attr"]["totalPages"]}')
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

    def get_statistics(self) -> Statistics:
        history_tracks = self.get_history_listen()
        stat = Statistics()
        cache_length = {}

        for num, track in enumerate(history_tracks):
            if track.mbid != "" and track.mbid in cache_length:
                length = cache_length[track.mbid]
                self.logger.info(f'Found length for "{track.artist} - {track.title}": {length} (Cache) ({num}/{len(history_tracks)})')
            else:
                length = None
                for service in self.services:
                    length = service.get_length_track(track.title, track.artist, track.album)
                    if length is not None:
                        if track.mbid != "":
                            cache_length[track.mbid] = length
                        self.logger.info(f'Found length for "{track.artist} - {track.title}": {length} (Service: {service.__class__.__name__}) ({num}/{len(history_tracks)})')
                        break

            if length is not None:
                stat.add_listening(track.date.date(), length)
            else:
                self.logger.warning(f'Not found length for "{track.artist} - {track.title}"')

        return stat


def main():
    lastfm_api = LastFMAPI('19ab4773cf02ed33bb1354017e3286ef')
    service = [service_length.LastFM(lastfm_api), service_length.YandexMusic(YMClient(report_new_fields=False))]
    lastfm_time = LastFMTime(lastfm_api, 'glebliutsko', service)
    statistics = lastfm_time.get_statistics()
    print(statistics.get_time_listening())


if __name__ == '__main__':
    main()
