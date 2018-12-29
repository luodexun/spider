# -*- coding: utf-8 -*-
import requests
from boto3.session import Session
from urllib3 import disable_warnings
from dwn_spider import settings

aws_key = settings.AWS_KEY
aws_secret = settings.AWS_SECRET
region_name = settings.REGION_NAME
bucket = settings.BUCKET


def upload_object(key, upload_data):
    session = Session(aws_access_key_id=aws_key,
                      aws_secret_access_key=aws_secret,
                      region_name=region_name)
    s3 = session.resource('s3')
    s3_client = session.client('s3')
    # 上传
    resp = s3.Bucket(bucket).put_object(Key=key, Body=upload_data)
    # 设置公开
    s3_client.put_object_acl(Bucket=bucket, Key=key, ACL='public-read')

    try:
        # 检查是否上传成功
        s3_client.head_object(Bucket=bucket, Key=key)
        return resp.key
    except Exception as e:
        print(e)
        return None


def upload_from_url(key, source_url):
    disable_warnings()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36',
    }
    response = requests.get(source_url, verify=False, headers=headers)
    upload_data = response.content
    return upload_object(key, upload_data)


if __name__ == '__main__':
    download_url = upload_from_url('test2.zip',
                                   'https://assrt.net//download/638220/american.horror.story.s08e02.720p.webrip.x264-tbs.zip')
    print(download_url)
