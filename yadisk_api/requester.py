import requests

from . import errors


class Requester:
    _disk_url = 'https://cloud-api.yandex.net/v1/'

    def __init__(self, token):
        self._token = token

    def get(self, url, params=None, **kwargs):
        response = self.wrap(requests.get)(url=url, params=params, **kwargs)
        return response.json()

    def post(self, url, data=None, json=None, **kwargs):
        response = self.wrap(requests.post)(url=url, data=data, json=json, **kwargs)
        return response.json()

    def put(self, url, data=None, **kwargs):
        response = self.wrap(requests.put)(url=url, data=data, **kwargs)
        return response.json()

    def patch(self, url, data=None, **kwargs):
        response = self.wrap(requests.patch)(url=url, data=data, **kwargs)
        return response.json()

    def delete(self, url, **kwargs):
        response = self.wrap(requests.delete)(url=url, **kwargs)
        return response.json()

    def wrap(self, method):
        """
        Add extra headers
        Change url
        etc
        """
        def wrapped(url, *args, **kwargs):
            url = '{}{}'.format(self._disk_url, url)
            if 'headers' not in kwargs:
                kwargs['headers'] = {}
            kwargs['headers']['Authorization'] = 'OAuth {}'.format(self._token)
            response = method(url, *args, **kwargs)
            response_data = response.json()
            # handle status code
            if response.status_code == 401:
                raise errors.UnauthorizedError(response_data['message'])

            if response.status_code == 403:
                raise errors.ForbiddenError(response_data['message'])

            if response.status_code == 409:
                raise errors.DiskPathDoesntExistsError(response_data['message'])

            return response
        return wrapped
