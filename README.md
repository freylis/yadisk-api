# yadisk-api
Yandex.disk HTTP API Python library

Example usage:

    import yadisk_api

    yad_client = yadisk_api.YandexDisk('my_token', app_name='my_app_name')

    # get info about my disk
    info = yad_client.get_disk_info()

    # get meta info about file/directory in my app directory/trash
    meta_info = yad_client.get_meta_info(
        path='path/to/my/file.jpg',
        preview_size='100x100',
    )

    # get audio files list in my disk
    files_info = yad_client.get_files_list(
        limit=50,
        media_type='audio'
    )

    # set meta data to file in your app directory
    setted_result = yad_client.get_last_uploaded(
        'my/file/to/extra/meta/data.txt,
        data={'Custom Header': 'custom value'},
    )
