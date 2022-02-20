import os
import json
import rootpath
import requests
from requests.auth import HTTPBasicAuth


class Utils:

    def get_user_details(self, user_type):
        with open(os.path.join(rootpath.detect(), 'api/test_data/credentials.json'), 'r') as file:
            data = file.read()
        user_details = json.loads(data)['users'][user_type]
        return user_details

    def get_auth_token(self, user_type):
        user_details = self.get_user_details(user_type)
        response = requests.post('https://accounts.spotify.com/api/token',
                                 auth=HTTPBasicAuth(user_details['client_id'], user_details['client_secret']),
                                 headers={'Content-Type': 'application/x-www-form-urlencoded'},
                                 params={'grant_type': 'client_credentials'})
        return response

    def create_playlist(self, bearer_token, user, playlist_name):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': bearer_token
        }
        request_body = {
            "name": playlist_name,
            "public": False
        }
        response = requests.post(f'https://api.spotify.com/v1/users/{user}/playlists', headers=headers,
                                 json=request_body)
        return response

    def add_songs(self, bearer_token, playlist):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': bearer_token
        }
        request_body = {
            "uris": [
                "spotify:track:3IIyZB7kmc9qp82unLG6Bc",
                "spotify:track:5DngwcGRVP7E35UroYGeCv",
                "spotify:track:7h003XBC6qLjvOWnDezrUl",
                "spotify:track:4yySoWPXUD7vj3voqHmgXd",
                "spotify:track:5ba4VVaG9Cea7S0OJi3pfS",
                "spotify:track:1ZUTAtWC0f0cZtyWdzjXVE",
                "spotify:track:6zKVT6IQNRgGd950filkyy",
                "spotify:track:3Vd2WMlYMADw5NoMNzCEfb",
                "spotify:track:3JbcfkeU6cYz5xt1MIRL8K",
                "spotify:track:0sAzzDG6rVfaEC4c0MfjsX",
                "spotify:track:5v03sKVU7ca8CksEVWCiWk",
                "spotify:track:0rma8iH4cfNBSvdba1Vcn1",
                "spotify:track:3CIdUlf3vM44C04FJe4hiX",
                "spotify:track:0afAKVFujwAayf5xnb6miR",
                "spotify:track:1arStxoEdAk3ZEytaeOGkM",
                "spotify:track:5yESMmwtizQw0rmjWTixF0",
                "spotify:track:1Ekrba78I48P12WPDLR13U"
            ]
        }
        response = requests.post(f'https://api.spotify.com/v1/playlists/{playlist}/tracks', headers=headers,
                                 json=request_body)
        return response

    def retrieve_songs(self, bearer_token, playlist):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': bearer_token
        }
        response = requests.get(f'https://api.spotify.com/v1/playlists/{playlist}/tracks', headers=headers)
        return response

    def remove_song(self, bearer_token, playlist, request_body):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': bearer_token
        }
        response = requests.delete(f'https://api.spotify.com/v1/playlists/{playlist}/tracks', headers=headers,
                                   json=request_body)
        return response
