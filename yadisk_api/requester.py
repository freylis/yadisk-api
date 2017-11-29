import requests


class Requester:
    # TODO handle it
    _disk_url = 'https://cloud-api.yandex.net/v1/'

    def __init__(self, token):
        self._token = token

    def get(self, url, params=None, **kwargs):
        response = requests.get(
            url=url,
            params=params,
            **kwargs
        )
        return response.json()

    def post(self, url, data=None, json=None, **kwargs):
        response = requests.post(
            url=url,
            data=data,
            json=json,
            **kwargs
        )
        return response.json()

    def put(self, url, data=None, **kwargs):
        response = requests.put(url=url, data=data, **kwargs)
        return response.json()

    def patch(self, url, data=None, **kwargs):
        response = requests.patch(
            url=url,
            data=data,
            **kwargs
        )
        return response.json()

    def delete(self, url, **kwargs):
        response = requests.delete(url=url, **kwargs)
        return response.json()
