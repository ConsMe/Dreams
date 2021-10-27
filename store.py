import boto3
import datetime
import glob
import os

session = boto3.session.Session()
s3 = session.client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net'
)

bucket = 'dreams'

folder = datetime.datetime.now().strftime('%Y_%m_%d')

files = glob.glob('files/*.mp3')
for path in files:
  file_name = os.path.basename(path)
  s3.upload_file(path, bucket, f'{folder}/{file_name}')
  os.remove(path)
# print(files)