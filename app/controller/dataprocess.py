import os
from app import app
from pandas import Series,DataFrame
from app.moduler.readfile import read_file,read_csv_file
import numpy as np
import xlrd
from xlutils.copy import copy
from xlwt import Style
import xlwt
import time
#import time

#def data_read(file_url):
#    df = read_file(file_url, sheet_name='Sheet1')
#    x = DataFrame(df)
#    data_replace = x.replace(np.nan, '')
#    return data_replace

def data_process1(file_url):
    #read file
    df = read_file(file_url,sheet_name='Sheet1')

    data_replace = df.replace(np.nan, '')

    """group cut"""
    intergenic = str('lncRNA, intergenic')
    df2 = df[df['gene class'].str.contains(intergenic, na=False)]
    df2 = df2.drop_duplicates('gene name')
    """group cut"""

    """alias symbol列から、”｜”で分ける"""
    newDF = df2['alias symbol'].str.split("|", expand=True)
    newDF = newDF.fillna(".")

    col_size = len(newDF.columns)

    # array_alias=[]
    namefile = Series()
    current_number = 0
    while current_number < col_size:
        namefile1 = newDF[~newDF[current_number].str.contains('\.', na=False)]
        namefile1 = namefile1[current_number]
        namefile = namefile.append(namefile1)
        current_number += 1
    namefile2 = namefile

    """削除."""
    genename2 = df2[~df2['gene name'].str.contains('\.', na=False)]
    genename2 = genename2['gene name']

    """名称を合わせる"""
    namefile = namefile.append(genename2)

    """CSV"""
    #down_path = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'tmp/download')
    #data_file.save(os.path.join(upload_path, data_filename))
    timestampe = time.strftime("%Y%m%d%H%M%S", time.localtime())
    csv_file_name = 'GENANAME' + '_' + timestampe + '.csv'
    down_path = os.path.join(app.root_path, 'tmp/download')
    #csv_file_name = 'GENANAME.csv'
    csv_file_save_url = os.path.join(down_path, csv_file_name)
    csv_file = namefile.to_csv(
        #r"C:\WDD\OUTPUT\GENANAME.CSV"
        csv_file_save_url
    )

    #return csv_file_save_url
    return data_replace,csv_file_name

def data_process2(excel_file_url,csv_file_url):
    #dfWDD2 = read_csv(
    #    r"C:\WDD\TEST\EntitySet_Gene Validate Set_2018-02-21_13-02-58.csv")
    dfWDD2 = read_csv_file(csv_file_url)

    """group cut"""
    dfWDD = dfWDD2[dfWDD2['Entity type'].str.contains('GENE', na=False)]
    """group cut"""

    # ===============================================
    #dfOLD = read_excel(
    #    r"C:\WDD\TEST\LincRNA.xlsx",
    #    sheetname='Sheet1'
    #)
    dfOLD = read_file(excel_file_url, sheet_name='Sheet1')

    """alias symbol列から、”｜”で分ける"""
    cutDF = dfOLD['alias symbol'].str.split("|", expand=True)
    col_size = len(cutDF.columns)
    """alias symbol列から、”｜”で分ける"""

    # ================================================

    def writeExcel(row, col, str, styl=Style.default_style):
        ws.write(row, col, str, styl)

    #rb = xlrd.open_workbook("C:\\WDD\\input\\LincRNA.xls", formatting_info=True)
    rb = xlrd.open_workbook(excel_file_url, formatting_info=True)
    wb = copy(rb)
    ws = wb.get_sheet(0)

    row_size = dfOLD.iloc[:, 0].size
    for i_index in range(0, row_size):
        if dfOLD.iloc[i_index]['gene name'] in dfWDD['User entity name'].values:
            style = xlwt.easyxf("font: name Arial;"
                                "pattern: pattern solid, fore_colour gold;")
            writeExcel(i_index + 1, 1, dfOLD.iloc[i_index]['gene name'], style)

    wb.save(excel_file_url)


    return 'Merge is completed!!!'

