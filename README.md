# yadisk-api
Yandex.disk HTTP API Python library

Get your access token first [here](https://tech.yandex.ru/disk/api/concepts/quickstart-docpage/)

Example usage:

    import yadisk_api

    disk = yadisk_api.YandexDisk('my_token', app_name='my_app_name')

    # get info about my disk
    info = disk.get_disk_info()

    # get meta info about file/directory in my app directory/trash
    meta_info = disk.get_meta_info(
        path='path/to/my/file.jpg',
        preview_size='100x100',
    )

    # get audio files list in my disk
    files_info = disk.get_files_list(
        limit=50,
        media_type='audio',
    )

    # get last uploaded files list
    last_uploaded = disk.get_last_uploaded(
        limit=10,
        media_type='video',
    )

    # set meta data to file in your app directory
    setted_result = disk.set_meta_to_file(
        'my/file/to/extra/meta/data.txt,
        data={'Custom Header': 'custom value'},
    )
