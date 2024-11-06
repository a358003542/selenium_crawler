import time
import logging
import os
from urllib.parse import urlsplit

import requests
from pywander.pathlib import normalized_path, mkdirs

logger = logging.getLogger(__name__)


def to_absolute_path(path):
    """
    返回标准化的绝对路径
    在normalized_path的基础上还引入当前路径添加等
    """
    return os.path.abspath(normalized_path(path))


def download(url, filename, download_timeout=30, override=False, **kwargs):
    """
    将目标url先下载到临时文件,然后再保存到命名文件.
    # https://github.com/kennethreitz/requests/issues/1803

    :param url: the url
    :param filename: 指定文件名

    """
    logger.info(f'start downloading file {url} to {filename}')
    start = time.time()

    filename = to_absolute_path(filename)

    # make sure folder exists
    mkdirs(os.path.dirname(filename))

    if os.path.exists(filename):
        if override:
            logger.info(f'{filename} exist. but i will override it.')
        else:
            logger.info(f'{filename} exist.')
            return

    content = requests.get(url, stream=True, **kwargs)

    with open(filename, 'wb') as f:
        for chunk in content.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
            if time.time() - start > download_timeout:
                content.close()
                os.unlink(filename)
                logger.warning('{0} download failed'.format(filename))
                return False

    return filename


def get_url_path(url):
    """
    获取url的path属性
    """
    p = urlsplit(url)
    return p.path


def get_download_filename(url):
    """
    从下载url中获得文件名, 不一定是有意义的.
    """
    path = get_url_path(url)
    filename = os.path.basename(path)
    return filename


def download_image(image_url, title):
    filename = get_download_filename(image_url)
    base_dir = 'download'
    new_filename = os.path.join(base_dir, title, filename)

    download(image_url, filename=new_filename)
