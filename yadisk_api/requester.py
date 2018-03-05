import logging

import requests

from . import errors


logger = logging.Logger('yadisk-api')


_CODE_TO_ERROR = {
    401: errors.UnauthorizedError,
    403: errors.ForbiddenError,
    409: errors.DiskPathError,
    404: errors.NotFoundError,
    412: errors.PreconditionFailed,
    413: errors.PayloadTooLarge,
    500: errors.InternalServerError,
    503: errors.ServiceUnavailable,
    507: errors.InsufficientStorageError,
}

STATUS_OK = 200
STATUS_CREATED = 201
STATUS_ACCEPTED = 202
STATUS_NO_CONTENT = 204

OK_STATUSES = {
    STATUS_OK,
    STATUS_CREATED,
    STATUS_ACCEPTED,
    STATUS_NO_CONTENT,
}


class Requester(object):
    _disk_url = 'https://cloud-api.yandex.net/v1/'

    def __init__(self, token):
        self._token = token

    def get(self, url, params=None, **kwargs):
        return self.wrap(requests.get)(url=url, params=params, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        return self.wrap(requests.post)(url=url, data=data, json=json, **kwargs)

    def put(self, url, data=None, **kwargs):
        return self.wrap(requests.put)(url=url, data=data, **kwargs)

    def patch(self, url, data=None, **kwargs):
        return self.wrap(requests.patch)(url=url, data=data, **kwargs)

    def delete(self, url, **kwargs):
        return self.wrap(requests.delete)(url=url, **kwargs)

    def wrap(self, method):
        """
        - Add extra headers to request
        - Change url
        - Handle response status code
        """
        method_name = {
            self.get: 'GET',
            self.post: 'POST',
            self.put: 'PUT',
            self.patch: 'PATCH',
            self.delete: 'DELETE',
        }[method]

        def wrapped(url, *args, **kwargs):
            absolute_url = kwargs.pop('absolute_url', False)
            if not absolute_url:
                url = '{}{}'.format(self._disk_url, url)
            if 'headers' not in kwargs:
                kwargs['headers'] = {}

            logger.debug('Call {!r} method by url={!r}'.format(method_name, url))
            if kwargs.pop('without_auth', False) is not True:
                kwargs['headers']['Authorization'] = 'OAuth {}'.format(self._token)
            response = method(url, *args, **kwargs)
            logger.debug('Response status_code={} by url={}/{}'.format(
                response.status_code,
                url,
                method_name
            ))
            if response.status_code in OK_STATUSES:
                return response

            try:
                response_msg = response.json()['message']
            except ValueError:
                response_msg = str(response.content)

            logger.error(
                'Status_code={}; response body: {}; request_url={!r}; method={!r}'.format(
                    response.status_code,
                    response_msg,
                    url,
                    method,
                )
            )

            # handle status code
            if response.status_code not in _CODE_TO_ERROR:
                raise errors.RequestError(response_msg)

            raise _CODE_TO_ERROR[response.status_code](response_msg)

        return wrapped
