import time
import urllib.parse

from . import requester


class YandexDisk:
    _requester_cls = requester.Requester

    def __init__(self, token):
        self._requester = self._requester_cls(token=token)

    def get_disk_info(self):
        """
        Get info about your disk

        Docs: https://tech.yandex.ru/disk/api/reference/capacity-docpage/
        """
        return self._requester.get(url='disk/').json()

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
        ).json()

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
        return self._requester.get(url='disk/resources/files', params=params).json()

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
        return self._requester.get(url='disk/resources/files', params=params).json()

    def set_meta_to_file(self, path, data, fields=None):
        """
        Set meta-data to file

        Docs: https://tech.yandex.ru/disk/api/reference/meta-add-docpage/
        """
        params_string = urllib.parse.urlencode(
            {
                'path': path,
                'fields': fields,
            },
            doseq=False,
        )
        return self._requester.patch(
            url='disk/resources/?{}'.format(params_string),
            data=data,
        ).json()

    def upload_file(self, file_object, path='/', overwrite=False, fields=None):
        """
        Upload file to yandex disk
        Docs: https://tech.yandex.ru/disk/api/reference/upload-docpage/

        Args:
            file_object (file): file to upload
            path (str): path to file place
            overwrite (bool): overwrite file if it exist
            fields (list[str]|None): fields in result
        """
        upload_path_url = self._requester.get(
            url='disk/resources/upload',
            params={
                'path': path,
                'overwrite': overwrite,
                'fields': fields,
            },
        )
        return self._requester.put(
            url=upload_path_url['href'],
            files={'file': file_object},
            absolute_url=True,
        ).json()

    def upload_file_by_url(
        self,
        url,
        path,
        fields=None,
        disable_redirects=False,
        wait_for_finish=True,
        sleep=3,
    ):
        """
        Upload file from url to yandex disk
        Docs: https://tech.yandex.ru/disk/api/reference/upload-ext-docpage/

        Args:
            url (str): url to download file from it
            path (str): path to yandex disk
            fields (list[str]|None): fields in result
            disable_redirects (bool): disable redirects
            wait_for_finish (bool): wait for operation finish
            sleep (int): sleep time in seconds if need wait to finish
        """
        params_string = urllib.parse.urlencode(
            {
                'url': url,
                'path': path,
                'fields': fields,
                'disable_redirects': disable_redirects,
            },
            doseq=False,
        )
        self._waiting_for_finish(
            self._requester.post(
                url='disk/resources/upload?{}'.format(params_string),
            ),
            wait_for_finish=wait_for_finish,
            sleep=sleep,
        )
        return True

    def download_file(self, path, fields=None, stream=False):
        """
        Download file from your disk
        Docs: https://tech.yandex.ru/disk/api/reference/content-docpage/

        Args:
            path (str): path to file
            fields (list[str]): fields in response
            stream (bool): stream response

        Returns:
            bytes: file content
        """
        url_response = self._requester.get(
            url='disk/resources/download',
            params={
                'path': path,
                'fields': fields,
            }
        )
        return self._requester.get(
            url=url_response.json()['href'],
            absolute_url=True,
            stream=stream,
        ).content

    def copy_resource(
        self,
        from_path,
        to_path,
        overwrite=False,
        fields=None,
        wait_for_finish=True,
        sleep=3,
    ):
        """
        Copy file/directory in disk
        Docs: https://tech.yandex.ru/disk/api/reference/copy-docpage/

        Args:
            from_path (str): source path
            to_path (str): destination path
            overwrite (bool): overwrite file/directory if exists
            fields (list[str]|None): response fields list
            wait_for_finish (bool): wait for operation finish
            sleep (int): sleep time in seconds if need wait to finish
        """
        params_string = urllib.parse.urlencode(
            {
                'from': from_path,
                'path': to_path,
                'overwrite': overwrite,
                'fields': fields,
            },
            doseq=False,
        )
        self._waiting_for_finish(
            self._requester.post(url='disk/resources/copy?{}'.format(params_string)),
            wait_for_finish=wait_for_finish,
            sleep=sleep,
        )
        return True

    def move_resource(
        self,
        from_path,
        to_path,
        overwrite=False,
        fields=None,
        wait_for_finish=True,
        sleep=3,
    ):
        """
        Move file/directory in disk
        Docs: https://tech.yandex.ru/disk/api/reference/move-docpage/

        Args:
            from_path (str): source path
            to_path (str): destination path
            overwrite (bool): overwrite file/directory if exists
            fields (list[str]|None): response fields list
            wait_for_finish (bool): wait for operation finish
            sleep (int): sleep time in seconds if need wait to finish
        """
        params_string = urllib.parse.urlencode(
            {
                'from': from_path,
                'path': to_path,
                'overwrite': overwrite,
                'fields': fields,
            },
            doseq=False,
        )
        self._waiting_for_finish(
            self._requester.post(url='disk/resources/move?{}'.format(params_string)),
            wait_for_finish=wait_for_finish,
            sleep=sleep,
        )
        return True

    def _waiting_for_finish(self, response, wait_for_finish=True, sleep=3):
        """
        Waiting for finish operation, if you want

        Args:
            response (requests.Response): response object
            wait_for_finish (bool): wait for operation finish
            sleep (int): sleep time in seconds if need wait to finish

        Returns:
            requests.Response
        """
        if (
            wait_for_finish
            and response.status_code == requester.STATUS_ACCEPTED
        ):
            check_status_url = response.json()['href']
            while True:
                time.sleep(sleep)
                response = self._requester.get(check_status_url, absolute_url=True)
                if (
                    response.status_code == requester.STATUS_OK
                    and response.json()['status'] == 'success'
                ):
                    return response
        return response
