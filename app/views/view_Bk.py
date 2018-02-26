from app import app
import config
from flask import request,send_from_directory,url_for,render_template
from werkzeug.utils import secure_filename
import os,json
from xlutils.copy import copy
from xlutils3.copy import copy
from app.moduler.readfile import read_file
from app.controller.dataprocess import data_process1

#设定配置
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = config.DOWNLOAD_FOLDER
#app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    response_html = 'fileselect.html'
    return render_template(response_html)

#检查上传文件合法性
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1] in config.ALLOWED_EXTENSIONS

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    #return send_from_directory(app.config['DOWNLOAD_FOLDER'],filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

@app.route('/upload',methods=['GET','POST'])
def xlsfilelist():

    if request.method == 'POST':
        data_file = request.files['csvfile']

        data_filename = data_file.filename

        #保存file到Server 上
        upload_path = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'tmp/uploadfiles')
        #print(upload_path)
        data_file.save(os.path.join(upload_path, data_filename))
        #print('OK')
        #file在Server上的URL
        data_file_save_url= os.path.join(upload_path, data_filename)
        #print('@@@@@',data_file_save_url)

        # read excel data
        datalist=data_process1(data_file_save_url)
        #print(datalist.columns[:])
        #print(datalist.ix[:])

        response_html = 'xlsdatalist.html'
        return render_template(response_html,message=datalist)