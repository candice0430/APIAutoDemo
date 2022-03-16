# -*- coding: UTF-8 -*-

# author:p_ppcjchen
# create by:2022/3/13/11:02 下午
import unittest
from base.req import ApiRequest
from utils.util import *
from ddt import ddt, data, unpack
from common.public import *

dic = get_yaml_data(file_path('data','register.yaml'))
print(dic)

@ddt
class TestRegister(unittest.TestCase):
    url = "/register/"

    # 用例1，按要求正常填写，注册成功
    @data(dic["registerSuccess"])
    def test_register_success(self,params):
        params['email'] = random_email()
        rsp = ApiRequest().post(url="/register/",json=params)
        print(rsp)
        has_access = rsp["user"]
        self.assertEqual(len(has_access)>0,True,"注册成功")

    @data(*dic["registerFail"])
    def test_register_fail_01(self,params):
        params['email'] = random_email()
        rsp = ApiRequest().post(url=self.url,json=params)
        self.assertIsNot("access",rsp,"password为空，注册失败验证")

    @data(*dic["registerNOEmail"])
    def test_register_fail_02(self, params):
        rsp = ApiRequest().post(url=self.url, json=params)
        self.assertIsNot("access", rsp, "password为空，注册失败验证")

    @data(*dic["registerExist"])
    def test_register_fail_03(self, params):
        rsp = ApiRequest().post(url=self.url, json=params)
        self.assertIsNot("access", rsp, "password为空，注册失败验证")


if __name__ == '__main__':
    unittest.main()