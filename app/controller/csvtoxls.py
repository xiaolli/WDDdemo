# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 09:50:26 2018

@author: MeiLingYan
"""

from pandas import read_excel;
#from pandas import Series
from pandas import read_csv;
#from pandas import Series
import xlwings as xw;

dfWDD2 = read_csv(
    #r"C:\WDD\TEST\EntitySet_Gene Validate Set_2018-02-21_13-02-58.csv")
    '/Users/xiaolli/Desktop/WDD/EntitySet_Gene Validate Set_2018-02-21_13-02-58.csv')

"""group cut"""
dfWDD=dfWDD2[dfWDD2['Entity type'].str.contains('GENE', na=False)]
"""group cut"""

#===============================================
dfOLD = read_excel(
    #r"C:\WDD\TEST\LincRNA.xlsx",
    '/Users/xiaolli/Desktop/WDD/LincRNA.xlsx',
    sheet_name='Sheet1'
)
"""alias symbol列から、”｜”で分ける"""
cutDF = dfOLD['alias symbol'].str.split("|", expand=True)
col_size=len(cutDF.columns)
"""alias symbol列から、”｜”で分ける"""

#================================================

ap = xw.App(visible=True,add_book=False)
#wb=ap.books.open(r"C:\WDD\TEST\LincRNA.xlsx")
wb=ap.books.open('/Users/xiaolli/Desktop/WDD/LincRNA.xlsx')
#sht = wb.sheets[0]
sht=wb.sheets['Sheet1']
row_size=dfOLD.iloc[:,0].size
print(row_size)
for i_index in range(0,row_size):
    if dfOLD.iloc[i_index]['gene name'] in dfWDD['User entity name'].values:
        aaa='B'+str(i_index+2)
        rng = sht.range(aaa)   
        rng.color = (255,242,204)
    else:
#        set1 = set(cutDF.loc[i_index])
#        set2 = set(dfWDD['User entity name'])
        if set(cutDF.loc[i_index]) & set(dfWDD['User entity name'].values):
            
            aaa='B'+str(i_index+2)
            rng = sht.range(aaa)   
            rng.color = (255,242,204)
wb.save()
wb.close()
ap.quit()  