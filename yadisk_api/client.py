from . import requester


class YandexDisk:
    _requester_cls = requester.Requester

    def __init__(
        self,
        token,
        app_name=None,
    ):
        self._requester = self._requester_cls(token=token)

    def get_disk_info(self):
        """
        Get info about your disk

        Docs: https://tech.yandex.ru/disk/api/reference/capacity-docpage/
        """
        return self._requester.get(url='disk/')

    def get_meta_info(
        self,
        path,
        sort=None,
        limit=None,
        offset=None,
        fields=None,
        preview_size=None,
        preview_crop=None,
        trash=False,
    ):
        """
        Get meta info about file/directory from disk or trash

        Docs: https://tech.yandex.ru/disk/api/reference/meta-docpage/
        """
        params = {
            'path': path,
            'sort': sort,
            'limit': limit,
            'offset': offset,
            'fields': fields,
            'preview_size': preview_size,
            'preview_crop': preview_crop,
        }
        return self._requester.get(
            url='disk/{}resources'.format('trash/' if trash else ''),
            params=params,
        )

    def get_files_list(
        self,
        limit=None,
        offset=None,
        media_type=None,
        fields=None,
        preview_size=None,
        preview_crop=None,
    ):
        """
        Get files list from disk

        Docs: https://tech.yandex.ru/disk/api/reference/all-files-docpage/
        """
        params = {
            'limit': limit,
            'offset': offset,
            'fields': fields,
            'preview_size': preview_size,
            'preview_crop': preview_crop,
            'media_type': media_type,
        }
        return self._requester.get(
            url='disk/resources/files',
            params=params,
        )

    def get_last_uploaded(
        self,
        limit=None,
        media_type=None,
        fields=None,
        preview_size=None,
        preview_crop=None,
    ):
        """
        Get last uploaded files list

        Docs: https://tech.yandex.ru/disk/api/reference/recent-upload-docpage/
        """
        params = {
            'limit': limit,
            'fields': fields,
            'preview_size': preview_size,
            'preview_crop': preview_crop,
            'media_type': media_type,
        }
        return self._requester.get(
            url='disk/resources/files',
            params=params,
        )

    def set_meta_to_file(self, path, data, fields=None):
        """
        Set meta-data to file

        Docs: https://tech.yandex.ru/disk/api/reference/meta-add-docpage/
        """
        return self._requester.patch(
            url='v1/disk/resources/?',
            data=data,
        )
