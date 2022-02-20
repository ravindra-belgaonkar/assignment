# Create a successful test case with valid user credentials to validate Authentication Success Object
# Create a failed test case with invalid user credentials to validate Authentication Error Object

from api.generic.utils import Utils


class TestAuth:
    '''
    Tests to validate valid and invalid authentication
    '''
    util = Utils()

    def test_valid_user(self):
        '''
        Test authentication for valid user
        '''
        response = self.util.get_auth_token('valid')
        assert response.status_code == 200
        assert response.json()['token_type'].lower() == 'bearer'

    def test_invalid_client_id(self):
        '''
        Test authentication for user with invalid client id
        '''
        response = self.util.get_auth_token('invalid_client_id')
        assert response.status_code == 400
        assert response.json()['error'].lower() == 'invalid_client'

    def test_invalid_client_secret(self):
        '''
        Test authentication for user with invalid client id
        '''
        response = self.util.get_auth_token('invalid_client_secret')
        assert response.status_code == 400
        assert response.json()['error_description'].lower() == 'invalid client secret'




