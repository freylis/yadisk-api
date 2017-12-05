class YandexDiskError(Exception):
    pass


class UnauthorizedError(YandexDiskError):
    pass


class ForbiddenError(YandexDiskError):
    pass


class DiskPathDoesntExistsError(YandexDiskError):
    pass
