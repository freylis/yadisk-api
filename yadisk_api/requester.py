import requests

from . import errors


_CODE_TO_ERROR = {
    401: errors.UnauthorizedError,
    403: errors.ForbiddenError,
    409: errors.DiskPathDoesntExistsError,
    404: errors.NotFoundError,
    412: errors.PreconditionFailed,
    413: errors.PayloadTooLarge,
    500: errors.InternalServerError,
    503: errors.ServiceUnavailable,
    507: errors.InsufficientStorageError,
}


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
        return response.json() if response.text else True

    def patch(self, url, data=None, **kwargs):
        response = self.wrap(requests.patch)(url=url, data=data, **kwargs)
        return response.json()

    def delete(self, url, **kwargs):
        response = self.wrap(requests.delete)(url=url, **kwargs)
        return response.json()

    def wrap(self, method):
        """
        - Add extra headers to request
        - Change url
        - Handle response status code
        etc
        """
        def wrapped(url, *args, **kwargs):
            absolute_url = kwargs.pop('absolute_url', False)
            if not absolute_url:
                url = '{}{}'.format(self._disk_url, url)
            if 'headers' not in kwargs:
                kwargs['headers'] = {}
            kwargs['headers']['Authorization'] = 'OAuth {}'.format(self._token)
            response = method(url, *args, **kwargs)
            if response.status_code in {200, 201, 202}:
                return response

            response_data = response.json()
            if response.status_code not in _CODE_TO_ERROR:
                raise errors.RequestError(response_data['message'])

            # handle status code
            raise _CODE_TO_ERROR[response.status_code](response_data['message'])

        return wrapped
