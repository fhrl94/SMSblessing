import glob

import sys

import os
import xlrd
import xlwt


def readxlsx(exclefile, ws, j):
    workbook = xlrd.open_workbook(filename=exclefile)
    if j == 0:
        temp = 1
    else:
        temp = 2
    for sheet, one in enumerate(workbook.sheet_names()):
        print(one)
        if '离职' not in one and '司龄补回表' not in one:
            for i in range(temp, workbook.sheet_by_name(one).nrows):
                if workbook.sheet_by_name(one).cell_value(i, 8) != "":
                    # print(workbook.sheet_by_name(one).cell_value(i, 8 - 1))
                    # print(workbook.sheet_by_name(one).cell_value(i, 9 - 1))
                    # print(workbook.sheet_by_name(one).cell_value(i, 15 - 1))
                    # print(workbook.sheet_by_name(one).cell_value(i, 16 - 1))
                    # print(workbook.sheet_by_name(one).cell_value(i, 20 - 1))
                    # print(workbook.sheet_by_name(one).cell_value(i, 22 - 1))
                    # print(workbook.sheet_by_name(one).cell_value(i, 53 - 1))
                    ws.write(j, 0, workbook.sheet_by_name(one).cell_value(i, 8 - 1))
                    ws.write(j, 1, workbook.sheet_by_name(one).cell_value(i, 9 - 1))
                    ws.write(j, 2, workbook.sheet_by_name(one).cell_value(i, 53 - 1))
                    # ws.write(j, 2, workbook.sheet_by_name(one).cell_value(i, 15 - 1))
                    # ws.write(j, 3, workbook.sheet_by_name(one).cell_value(i, 16 - 1))
                    ws.write(j, 3, workbook.sheet_by_name(one).cell_value(i, 20 - 1))
                    ws.write(j, 4, workbook.sheet_by_name(one).cell_value(i, 22 - 1))
                    j += 1
    return j


files = glob.glob(sys.path[0] + os.sep + 'temp' + os.sep + '*.xlsx')
print(files)
sheet = xlwt.Workbook()
ws = sheet.add_sheet('人员名单')
j = 0
for file in files:
    print(file)
    j = readxlsx(file, ws, j)
sheet.save('祝福短信人员.xls')
