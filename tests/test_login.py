# -*- coding: UTF-8 -*-

# author:p_ppcjchen
# create by:2022/3/14/12:22 上午
import unittest
from base.req import ApiRequest
from common.public import *
from utils.util import *
from ddt import ddt, data


dic = get_yaml_data(file_path('data','login.yaml'))

@ddt
class TestLogin(unittest.TestCase):
    url = "/login/"

    # 正确的用户名和密码，登录成功验证
    @data(dic["loginSuccess"])
    def test_login_success(self,params):
        rsp = ApiRequest().post(url=self.url,json=params)
        print(rsp)
        self.assertIn('tokens',rsp,'正确的用户名和密码，登录成功验证')


    # 2.不存在的用户名，登录失败
    @data(*dic["loginFail"])
    def test_login_fail_01(self,params):
        rsp = ApiRequest().post(url=self.url, json=params)
        self.assertIsNot('tokens', rsp, '接口参数错误')


if __name__ == '__main__':
    unittest.main()


