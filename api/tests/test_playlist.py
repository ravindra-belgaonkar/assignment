# ii) Create a random name Public playlist and add 10 -20 songs via API
# iii) Retrievesong number 3-8
# iv) Remove a song with an invalid id key
# v) Remove song numbers 3rd and 10th from the list

from api.generic.utils import Utils
import pytest


class TestPlaylist:
    util = Utils()
    user = util.get_user_details('valid')['user']

    @pytest.fixture(scope="class")
    def valid_token(self):
        token = self.util.get_auth_token('valid')
        token = 'Bearer BQBNKo-uvPXm5eLXh6JDh2CGjrtRFvu7ho-gfOMnaDKNdxD-KW_c7ySXW2MJeFfDjXMLjRPCuYg1a1pmXjcDZz29-hCc-Pc94M43_3Q3UyPM4GPJ06je7d5h_eHdj3brbAqSwCDAyMq_ELrOV6AQh2UzBHgRDXX3xLQgHF36IyxOSZBAp_FvU7t0H8SBhf5GgomYi2vebWrFO9E0U0nHLczwNPpPDXni'
        return token

    @pytest.fixture(scope="class")
    def invalid_token(self):
        token = 'Bearer BQBsxEwEDTEhgheHbTUdqqR8vjuFtCGHK9DhWuWftzARj-ObCivVwIHf8otnk9315Qw86d-6jaqqxhZqzhU'
        return token

    @pytest.fixture(scope="class")
    def expired_token(self):
        token = 'Bearer BQDJnJd_suTE0tm6bDd9Gdz6QGrfrWUi8Sp8DiBllvz5q_-N_w7DkO8bZbQCOLhZg8kbTbwZGL6OU4loDfz_L2efxh7ujffp0WAQOb2_S_mUzlS_Uk7-giyGwNqyKlakTw2uTfMJ0MUaq81nodGG9kzFOnaDpVkdcuezEIJiW8qeL9LhaIppiDV9D3PDFmm8aStca-upQflo9hHEW9hxRQeGnMZHRo-xpdmuszHi_x7DAGNR1LmZXXIK9cPNiZhZv3lCC7foVFsEtQzACA8inS7L50AmLQJH5m-CzdQePkuTxaNB8tLrwHTtzgbL'
        return token

    def test_create_playlist(self, valid_token):
        response = self.util.create_playlist(valid_token, self.user, 'MyTest')
        assert response.status_code == 201
        assert response.json()['id'] != ''
        global playlist
        playlist = response.json()['id']

    def test_create_playlist_unauthorized(self, invalid_token):
        response = self.util.create_playlist(invalid_token, self.user, 'MyTest')
        assert response.status_code == 401

    def test_add_songs(self, valid_token):
        response = self.util.add_songs(valid_token, playlist)
        assert response.status_code == 201

    def test_add_songs_expired_token(self, expired_token):
        response = self.util.add_songs(expired_token, playlist)
        assert response.status_code == 401

    def test_retrieve_songs(self, valid_token):
        response = self.util.retrieve_songs(valid_token, playlist)
        print(response.content)
        songs = response.json()['items'][3:9]
        for song in songs:
            print(song['track']['uri'])

    def test_remove_songs(self, valid_token):
        response = self.util.retrieve_songs(valid_token, playlist)
        songs_list = response.json()['items']
        delete_songs = {
            "tracks": []
        }
        delete_songs['tracks'].append({"uri": songs_list[3]['track']['uri']})
        delete_songs['tracks'].append({"uri": songs_list[10]['track']['uri']})
        response = self.util.remove_song(valid_token, playlist, delete_songs)
        assert response.status_code == 200
        response = self.util.retrieve_songs(valid_token, playlist)
        assert delete_songs['tracks'][0]['uri'] not in response.text
        assert delete_songs['tracks'][1]['uri'] not in response.text

    def test_remove_song_invalid_playlist(self, valid_token):
        delete_songs = {
            "tracks": [{"urii": "spotify:track:4iV5W9uYEdYU45345435Va79Axb7Rh"}]
        }
        response = self.util.remove_song(valid_token, 'nonexisitngplay', delete_songs)
        assert response.status_code == 404
        assert response.json()["error"]['message'].lower() == 'invalid playlist id'

    def test_remove_invalid_song(self, valid_token):
        delete_songs = {
            "tracks": [{"uri": "spotify:track:7eQl3Yqv35ioqUfveKHitEz"}]
        }
        response = self.util.remove_song(valid_token, playlist, delete_songs)
        print(response.content)
        assert response.status_code == 400
        assert response.json()["error"]['message'].lower() == 'json body contains an invalid track uri: spotify:track:7eQl3Yqv35ioqUfveKHitEz'.lower()
