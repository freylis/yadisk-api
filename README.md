# yadisk-api
Yandex.disk HTTP API Python library

In first get your access token [here](https://tech.yandex.ru/disk/api/concepts/quickstart-docpage/)
In second install package

    pip install yadisk-api

Example usage:

    import yadisk_api

    disk = yadisk_api.YandexDisk('my_token')

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
    setted_result = disk.set_meta_to_resource(
        'my/file/to/extra/meta/data.txt,
        data={'Custom Header': 'custom value'},
    )

    # upload file to yandex disk
    with open('/path/to/my/file.txt', 'rb') as f:
        disk.upload_file(
            f,
            path='app:/directory/file.txt',
            overwrite=True
        )

    # upload file to disk by url
    disk.upload_file_from_url(
        'http://example.com/sitemap.xml',
        path='app:/sitemap_example.xml',
    )

    # download file content from yandex.disk
    content = disk.download_file(
        'app:/sitemap_example.xml',
        stream=False,
    )

    # copy resource in disk
    disk.copy_resource(
        from_path='app:/sitemap_example.xml',
        to_path='app:/sitemap_example_copy.xml',
    )

    # move resource in your disk
    disk.move_resource(
        from_path='app:/sitemap_example_copy.xml',
        to_path='app:/sitemap_example_movied_copy.xml',
    )

    # delete resource
    disk.delete_resource(
        'app:/sitemap_example_movied_copy.xml',
        permanently=False, # to trash
    )

    # create folder in your disk
    disk.create_folder(
        'app:/new_folder',
    )

    # publish
    disk.publish_resource('app:/new_folder')

    # unpublish
    disk.unpublish_resource('app:/new_folder')

    # fully empty trash
    disk.empty_trash()
    # or remove file from trash
    disk.empty_trash('app:/sitemap_example_movied_copy.xml')

    # restore resource from trash
    disk.restore_from_trash('app:/sitemap_example_movied_copy.xml')

    # upload dir to disk
    disk.upload_directory('/path/to/source', 'app:/path/to/disk', overwrite=True)
