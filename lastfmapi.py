import requests


class LastFMAPIError(Exception):
    pass


class LastFMAPI:
    URL_API = 'https://ws.audioscrobbler.com/2.0/'

    def __init__(self, api_key: str):
        self.api_key = api_key

    def _request(self, method: str, params: dict) -> dict:
        params['method'] = method
        params['format'] = 'json'
        params['api_key'] = self.api_key
        result: dict = requests.get(self.URL_API, params=params).json()

        if 'error' in result:
            raise LastFMAPIError(result)

        return result

    def get_recent_tracks(self, username, limit: int, page: int, ignore_now_playing: bool = True) -> dict:
        response = self._request('user.getRecentTracks', {
            'user': username,
            'limit': limit,
            'page': page
        })
        if ignore_now_playing and len(response['recenttracks']['track']) != 0:
            try:
                if response['recenttracks']['track'][0]['@attr']['nowplaying'] == 'true':
                    del response['recenttracks']['track'][0]
            except KeyError:
                pass

        return response['recenttracks']

    def get_info_track(self, track: str, artist: str) -> dict:
        response = self._request('track.getInfo', {
            'track': track,
            'artist': artist
        })

        return response['track']
