class YandexDiskError(Exception):
    pass


class UnauthorizedError(YandexDiskError):
    pass


class ForbiddenError(YandexDiskError):
    pass


class DiskPathError(YandexDiskError):
    pass


class NotFoundError(YandexDiskError):
    pass


class RequestError(YandexDiskError):
    pass


class PreconditionFailed(YandexDiskError):
    pass


class PayloadTooLarge(YandexDiskError):
    pass


class ServerError(YandexDiskError):
    pass


class InternalServerError(ServerError):
    pass


class ServiceUnavailable(ServerError):
    pass


class InsufficientStorageError(YandexDiskError):
    pass
