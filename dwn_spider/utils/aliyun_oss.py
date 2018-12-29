# -*- coding: utf-8 -*-
import hashlib

import oss2
import requests

from dwn_spider import settings

auth = oss2.Auth(settings.ACCESS_KEY_ID, settings.ACCESS_KEY_SECRET)
bucket = oss2.Bucket(auth, settings.OSS_ENDPOINT, settings.OSS_BUCKETNAME)


def upload_object(data, file_path, file_type):
    md5 = hashlib.md5()
    if isinstance(data, str):
        md5.update(bytes(data, encoding='utf-8'))
    else:
        md5.update(data)
    sign = md5.hexdigest()
    file_name = file_path + '/' + sign + file_type
    result = bucket.put_object(file_name, data)
    return result.resp.response.url


def upload_from_url(url, file_path, file_type):
    response = requests.get(url)
    data = response.content
    return upload_object(data, file_path, file_type)
