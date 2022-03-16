# -*- coding: UTF-8 -*-

# author:p_ppcjchen
# create by:2022/3/13/1:07 下午

import requests
import json


class ApiRequest(object):
        HOST = "https://interview.doraclp.cn"

        def get(self, url, **kwargs):
            """封装get方法"""
            # 获取请求参数
            params = kwargs.get("params")
            headers = kwargs.get("headers")
            try:
                result = requests.get(url, params=params, headers=headers)
                return result
            except Exception as e:
                print("get请求错误: %s" % e)

        def post(self, url, **kwargs):
            """封装post方法"""
            # 获取请求参数
            params = kwargs.get("params")
            data = kwargs.get("data")
            json = kwargs.get("json")

            url = self.HOST + url
            try:
                result = requests.post(url, params=params, data=data, json=json)
                return result.json()
            except Exception as e:
                print("post请求错误: %s" % e)


if __name__ == '__main__':
    params = {"first_name": "hello", "last_name": "word"}
    responds = ApiRequest().get(url="http://httpbin.org/get", data=params)
    print(responds)

    params = {"username": "admin", "password": "123456"}
    responds = ApiRequest().post(url="http://39.98.138.157:5000/api/login", data=params,headers=None)
    print(responds)
    # print(responds.text)
    # print(responds.url)
        #
