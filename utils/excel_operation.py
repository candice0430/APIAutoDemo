# -*- coding: UTF-8 -*-

# author:p_ppcjchen
# create by:2022/3/13/3:02 下午

import xlrd
import xlwt
from common.public import *


class ExcelOperation(object):
    def __init__(self,dir,file_name):
        self.dir = dir
        self.file_name = file_name

    # 获取sheet表
    def get_sheet(self):
        book = xlrd.open_workbook(file_path(self.dir,self.file_name))
        return book.sheet_by_index(0)

    # 以列表形式获取出所有数据
    def get_excel_datas(self):
        data = []
        title = self.get_sheet().row_values(0)
        print(title)
        for row in range(1,self.get_sheet().nrows):
            row_value = self.get_sheet().row_values(row)
            data.append(dict(zip(title,row_value)))
        return data


class ExcelVarles(object):
    case_Id="用例Id"
    case_module="用例模块"
    case_name="用例名称"
    case_url="用例地址"
    case_method="请求方式"
    case_type="请求类型"
    case_data="请求参数"
    case_headers="请求头"
    case_preposition="前置条件"
    case_isRun="是否执行"
    case_code="状态码"
    case_result="期望结果"


if __name__ == '__main__':
    print(ExcelOperation().get_excel_datas())
