from app import app
import config
from flask import request,send_from_directory,url_for,render_template,send_file,make_response,abort
import os
from app.controller.dataprocess import data_process1,data_process2


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

@app.route('/select',methods=['GET','POST'])
def xlsfilelist():

    if request.method == 'POST':
        data_file = request.files['excelfile']

        data_filename = data_file.filename

        #保存file到Server 上
        #upload_path = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'tmp/uploadfiles')
        upload_path = os.path.join(app.root_path, 'tmp/uploadfiles')
        #print(upload_path)
        data_file.save(os.path.join(upload_path, data_filename))
        #print('OK')
        #file在Server上的URL
        data_file_save_url= os.path.join(upload_path, data_filename)

        # read excel data and
        # analysis to creat csv
        df_object = data_process1(data_file_save_url)
        datalist= df_object[0]
        csv_file_url = df_object[1]

        #datalist = data_read(data_file_save_url)
        data_head = datalist.head(100)
        data_tail =datalist.tail(100)
        data_total_count = datalist.shape[0]
        out_message = 'There are ' + str(data_total_count) + ' records in file. ' \
                    'The first 100 records and the lastest 100 records are displayed as following! '
        response_html = 'xlsdatalist.html'
        return render_template(response_html,
                               data_head=data_head,
                               data_tail = data_tail,
                               out_message =out_message,
                               csvfile =csv_file_url)

@app.route('/analysis', methods=['GET','POST'])
def analysis():
    #filename = 'GENANAME.csv'
    filename = request.form['csvfile']
    dirpath = os.path.join(app.root_path, 'tmp/download')
    return send_from_directory(dirpath, filename, as_attachment=True)

    '''
    try:
        file_path = os.path.join(app.root_path, 'tmp/download')
        print(file_path)
        url = os.path.join(file_path, filename)

        r = request.get(url, timeout=500)
        if r.status_code != 200:
            raise Exception("Cannot connect with oss server or file is not existed")
        response = make_response(r.content)
        mime_type = mimetypes.guess_type(filename)[0]
        response.headers['Content-Type'] = mime_type
        response.headers['Content-Disposition'] = 'attachment; filename={}'.format(filename.encode().decode('latin-1'))
        return response
    except Exception as err:
        print('download_file error: {}'.format(str(err)))
        logging.exception(err)
        return 'Download oss files failed!'''

@app.route('/filemerge',methods=['GET','POST'])
def csvtoexcel():
    if request.method == 'POST':
        excel_file = request.files['excelfile']
        excel_filename = excel_file.filename

        csv_file = request.files['csvfile']
        csv_filename = csv_file.filename

        #保存file到Server 上
        #upload_path = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'tmp/uploadfiles')
        upload_path = os.path.join(app.root_path, 'tmp/uploadfiles')
        #print(upload_path)
        excel_file.save(os.path.join(upload_path, excel_filename))
        csv_file.save(os.path.join(upload_path, csv_filename))
        #print('OK')
        #file在Server上的URL
        excel_file_save_url= os.path.join(upload_path, excel_filename)
        csv_file_save_url = os.path.join(upload_path, csv_filename)
        # read excel data and csv data to merge
        df_object = data_process2(excel_file_save_url,csv_file_save_url )

        #datalist= df_object[0]
        #csv_file_url = df_object[1]
        #datalist = data_read(data_file_save_url)
        #data_head = datalist.head(100)
        #data_tail =datalist.tail(100)
        #data_total_count = datalist.shape[0]

        out_message = df_object
        response_html = 'filemerge.html'
        return render_template(response_html,
                            #data_head=data_head,
                            #data_tail = data_tail,
                            out_message =out_message,
                            excel_filename = excel_filename)
                            #csvfile =csv_file_url )
    else:
        response_html = 'filemerge.html'
        return render_template(response_html)

@app.route('/downloadfile', methods=['GET','POST'])
def downloadfile():
    #filename = 'LincRNA.xlsx'
    filename = request.form['excel_filename']
    dirpath = os.path.join(app.root_path, 'tmp/uploadfiles')
    return send_from_directory(dirpath, filename, as_attachment=True)
