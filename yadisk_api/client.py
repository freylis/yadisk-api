import json
import time
import logging
import urllib.parse

from . import requester


logger = logging.Logger('yadisk-api')


class YandexDisk(object):
    _SLEEP = 3
    _requester_cls = requester.Requester

    def __init__(self, token):
        self._requester = self._requester_cls(token=token)

    def get_disk_info(self):
        """
        Get info about your disk

        Docs: https://tech.yandex.ru/disk/api/reference/capacity-docpage/
        """
        logger.info('Get disk info')
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
        logger.info('Get meta info (from trash={}) with params {}'.format(trash, params))
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
        logger.info('Get files list with params {}'.format(params))
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
        logger.info('Get last uploaded with params {}'.format(params))
        return self._requester.get(url='disk/resources/files', params=params).json()

    def set_meta_to_resource(self, path, data, fields=None):
        """
        Set meta-data to file/directory

        Docs: https://tech.yandex.ru/disk/api/reference/meta-add-docpage/
        """
        url_params = {'path': path}
        if fields:
            url_params['fields'] = fields
        params_string = urllib.parse.urlencode(url_params, doseq=False)
        logger.info('Set meta {!r} to resource {!r}'.format(data, path))
        return self._requester.patch(
            url='disk/resources/?{}'.format(params_string),
            data=json.dumps({'custom_properties': data}),
        ).json()

    def upload_file(self, file_object, path='/', overwrite=False):
        """
        Upload file to yandex disk
        Docs: https://tech.yandex.ru/disk/api/reference/upload-docpage/

        Args:
            file_object (file): file to upload
            path (str): path to file place
            overwrite (bool): overwrite file if it exist
        """
        logger.info('Upload file to {!r}'.format(path))
        upload_path_url = self._requester.get(
            url='disk/resources/upload',
            params={
                'path': path,
                'overwrite': overwrite,
            },
        )
        self._requester.put(
            url=upload_path_url.json()['href'],
            files={'file': file_object},
            absolute_url=True,
        )
        return True

    def upload_file_from_url(
        self,
        url,
        path,
        fields=None,
        disable_redirects=False,
        wait_for_finish=True,
        sleep=None,
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
        logger.info('Upload file from url {!r} to {!r}'.format(url, path))
        return self._waiting_for_finish(
            self._requester.post(
                url='disk/resources/upload?{}'.format(params_string),
            ),
            wait_for_finish=wait_for_finish,
            sleep=sleep,
        ).json()

    def download_file(self, path, stream=False):
        """
        Download file from your disk
        Docs: https://tech.yandex.ru/disk/api/reference/content-docpage/

        Args:
            path (str): path to file
            stream (bool): stream response

        Returns:
            bytes: file content
        """
        logger.info('Download file from {!r}'.format(path))
        url_response = self._requester.get(
            url='disk/resources/download',
            params={'path': path}
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
        sleep=None,
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
        logger.info('Copy resource from {!r} to {!r}'.format(from_path, to_path))
        params_string = urllib.parse.urlencode(
            {
                'from': from_path,
                'path': to_path,
                'overwrite': overwrite,
                'fields': fields,
            },
            doseq=False,
        )
        return self._waiting_for_finish(
            self._requester.post(url='disk/resources/copy?{}'.format(params_string)),
            wait_for_finish=wait_for_finish,
            sleep=sleep,
        ).json()

    def move_resource(
        self,
        from_path,
        to_path,
        overwrite=False,
        wait_for_finish=True,
        sleep=None,
    ):
        """
        Move file/directory in disk
        Docs: https://tech.yandex.ru/disk/api/reference/move-docpage/

        Args:
            from_path (str): source path
            to_path (str): destination path
            overwrite (bool): overwrite file/directory if exists
            wait_for_finish (bool): wait for operation finish
            sleep (int): sleep time in seconds if need wait to finish
        """
        logger.info('Move resource from {!r} to {!r}'.format(from_path, to_path))
        params_string = urllib.parse.urlencode(
            {
                'from': from_path,
                'path': to_path,
                'overwrite': overwrite,
            },
            doseq=False,
        )
        return self._waiting_for_finish(
            self._requester.post(url='disk/resources/move?{}'.format(params_string)),
            wait_for_finish=wait_for_finish,
            sleep=sleep,
        ).json()

    def delete_resource(self, path, permanently=False, wait_for_finish=True, sleep=None):
        """
        Remove file/directory to trash or at all
        Docs: https://tech.yandex.ru/disk/api/reference/delete-docpage/

        Args:
            path (str): path to file/directory
            permanently (bool): true if your want remove resource without trash
            wait_for_finish (bool): wait for operation finish
            sleep (int): sleep time in seconds if need wait to finish
        """
        logger.info('Delete resource from {!r}'.format(path))
        params_string = urllib.parse.urlencode(
            {
                'path': path,
                'permanently': permanently,
            },
            doseq=False,
        )
        self._waiting_for_finish(
            self._requester.delete(
                url='disk/resources?{}'.format(params_string)
            ),
            wait_for_finish=wait_for_finish,
            sleep=sleep,
        )
        return True

    def create_folder(self, path, fields=None):
        """
        Create folder in your disk
        Docs: https://tech.yandex.ru/disk/api/reference/create-folder-docpage/
        """
        logger.info('Create folder {!r}'.format(path))
        params_string = urllib.parse.urlencode(
            {
                'path': path,
                'fields': fields,
            },
            doseq=False,
        )
        return self._requester.put(url='disk/resources/?{}'.format(params_string)).json()

    def publish_resource(self, path):
        """
        Publish_resource
        Docs: https://tech.yandex.ru/disk/api/reference/publish-docpage/

        Args:
            path (str): path to resource
        """
        logger.info('Publish resource {!r}'.format(path))
        params_string = urllib.parse.urlencode({'path': path})
        return self._requester.put(
            url='disk/resources/publish?{}'.format(params_string)
        ).json()

    def unpublish_resource(self, path):
        """
        Unpublish resource
        Docs: https://tech.yandex.ru/disk/api/reference/publish-docpage/#unpublish-q

        Args:
            path (str): path to resource
        """
        logger.info('Unpublish resource {!r}'.format(path))
        params_string = urllib.parse.urlencode({'path': path})
        return self._requester.put(
            url='disk/resources/unpublish?{}'.format(params_string)
        ).json()

    def empty_trash(self, path=None, wait_for_finish=True, sleep=None):
        """
        Empty trash or delete resource from trash
        Docs: https://tech.yandex.ru/disk/api/reference/trash-delete-docpage/
        """
        logger.info('Empty trash')
        path_param = '?{}'.format(
            urllib.parse.urlencode({'path': path})
        ) if path else ''
        self._waiting_for_finish(
            self._requester.delete(url='disk/trash/resources/{}'.format(path_param)),
            wait_for_finish=wait_for_finish,
            sleep=sleep,
        )
        return True

    def restore_from_trash(self, path, name=None, overwrite=False):
        """
        Restore resource from trash
        Docs: https://tech.yandex.ru/disk/api/reference/trash-restore-docpage/
        """
        logger.info('Restore {!r} from trash'.format(path))
        params_string = urllib.parse.urlencode(
            {
                'path': path,
                'name': name,
                'overwrite': overwrite,
            },
            doseq=False,
        )
        return self._waiting_for_finish(
            self._requester.put(
                url='disk/trash/resources/restore?{}'.format(params_string),
            )
        ).json()

    def _waiting_for_finish(self, response, wait_for_finish=True, sleep=None):
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
            sleep = sleep or self._SLEEP
            while True:
                time.sleep(sleep)
                response = self._requester.get(check_status_url, absolute_url=True)
                if (
                    response.status_code == requester.STATUS_OK
                    and response.json()['status'] == 'success'
                ):
                    return response
        return response
