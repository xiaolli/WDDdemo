import os

#上传文件要储存的目录
upload_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),'tmp/uploadfiles')
download_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),'tmp/download')

UPLOAD_FOLDER = upload_path
DOWNLOAD_FOLDER = download_path

#PROFILE_FILE = "profiles.json"

#允许 上传的文件扩展名的集合
ALLOWED_EXTENSIONS = set(['csv','xls','xlsx'])
#ALLOWED_EXTENSIONS = set(['wav', 'flac'])

#限制文件大小
#MAX_CONTENT_LENGTH = 2 * 1024 * 1024




