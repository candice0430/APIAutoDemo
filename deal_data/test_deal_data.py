# -*- coding: UTF-8 -*-

# author:p_ppcjchen
# create by:2022/3/15/7:58 下午
import unittest
from utils.util import *
from ddt import ddt, data
from common.public import *
from deal_data.cargo_data_source import CargoDataSource


dic = get_yaml_data(file_path('data','cargo_data.yaml'))
@ddt
class TestDealData(unittest.TestCase):

    # 文件数据格式都正确，验证通过
    @data(dic["valid_success"])
    def test_valid_success(self,params):
        cargo_data = CargoDataSource()
        cargo_data.load(params['data_path'])
        is_success = cargo_data.data_valid()
        self.assertEqual(is_success,True)

    # form head test case
    @data(*dic['form_head_valid'])
    def test_form_head(self,params):
        cargo_data = CargoDataSource()
        is_success = cargo_data.valid_head(params)
        res = params['result']
        self.assertEqual(is_success, res,'form head valid')

    # file_type test case
    @data(*dic["valid_file_type"])
    def test_file_type(self, params):
        cargo_data = CargoDataSource()
        cargo_data.file_path = params['data_path']
        res = cargo_data.file_type_valid()
        self.assertEqual(res, params['result'], '文件类型验证')

    # field index test case
    @data(*dic["index_none"])
    def test_index_none(self, params):
        cargo_data = CargoDataSource()
        print(params)
        res = cargo_data.valid_index(params)
        self.assertEqual(res, False, 'field index is none...')

    # field index unique test case
    @data(dic["index_not_unique"])
    def test_index_none(self, params):
        cargo_data = CargoDataSource()
        print(params)
        cargo_data.valid_index(params[0])
        res = cargo_data.valid_index(params[1])
        self.assertEqual(res, False, 'field index is not unique...')

    # field dimensions test case
    @data(*dic["dimensions_invalid"])
    def test_valid_dimensions(self, params):
        cargo_data = CargoDataSource()
        res1 = cargo_data.valid_dimension(params)
        res = params['result']
        self.assertEqual(res, res1, 'field dimensions valid')

    # field weight test case
    @data(*dic["weight_invalid"])
    def test_valid_weight(self, params):
        cargo_data = CargoDataSource()
        res1 = cargo_data.valid_weight(params)
        res = params['result']
        self.assertEqual(res, res1, 'field weight valid')

    # field destination test case
    @data(*dic["destination_valid"])
    def test_valid_destination(self, params):
        cargo_data = CargoDataSource()
        res1 = cargo_data.destination_valid(params)
        res = params['result']


if __name__ == '__main__':
    unittest.main()


