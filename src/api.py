import urllib.parse
import http.client
import json
import webbrowser
import sys


class VKError(Exception):
    pass


class API():
    def __init__(self, access_token=None):
        self.access_token = access_token

    def request(self, method_name, **method_parameters):
        if self.access_token:
            method_parameters.update(access_token=self.access_token)
        query = 'https://api.vk.com/method/{0}?{1}'.format(method_name,
                                     urllib.parse.urlencode(method_parameters))
        connection = http.client.HTTPSConnection('api.vk.com')
        connection.request('GET', query)
        response = connection.getresponse().read()
        #TODO: To deal with exception http.client.BadStatusLine: ''
        connection.close()
        response = json.loads(response.decode('utf8'))
        if 'response' in response:
            return response['response']
        elif 'error' in response:
            error = response['error']
            if error['error_code'] == 6:
                print(error['error_msg'], file=sys.stderr)
                return self.request(method_name, **method_parameters)
            else:
                raise VKError(error)
        else:
            raise NotImplementedError(response)


def get_access_token(*rights):
    url = 'https://oauth.vk.com/authorize?client_id=3463254&'\
            'scope={0}&'\
            'redirect_uri=http://oauth.vk.com/blank.html&'\
            'display=touch&'\
            'response_type=token'.format(','.join(rights))
    webbrowser.open_new_tab(url)
