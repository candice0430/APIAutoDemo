# -*- coding: UTF-8 -*-

# author:p_ppcjchen
# create by:2022/3/13/10:56 下午
import json
import random
import string
import yaml


# 随机生成一个邮箱，避免邮箱重复
def random_email(email_min=7,email_max=20,list_email=['@163.com', '@sina.com', '@qq.com', '@yy.com']):
    # 根据指定范围，随机邮箱字符串最大最小长度
    ranLen = random.randint(email_min, email_max)
    # 随机邮箱后缀,从一个存储邮箱的list里选择
    email_form = random.choice(list_email)
    # 可供选的字符串
    str = ""
    letters1 = string.ascii_letters.lower()  # 字母
    letters2 = string.digits  # 数字
    for i in range(1, 3):
        str = str + letters1 + letters2 + letters2 + letters2 + letters2
    # 通过join()方法连接字符,去掉空格
    GetEmailStr = ''.join(random.sample(str, ranLen))

    # 字符串连接,加上邮箱后缀
    Email = GetEmailStr + email_form
    return Email

def check_json_format(raw_msg):
    """
    用于判断一个字符串是否符合Json格式
    """
    if isinstance(raw_msg, str):  # 首先判断变量是否为字符串
        try:
            json.loads(raw_msg, encoding='utf-8')
        except ValueError:
            return False
        return True
    else:
        return False


def get_yaml_data(yaml_file='../data/register.yaml'):
    # 打开yaml文件
    print("***获取yaml文件数据***")
    file = open(yaml_file, 'r', encoding="utf-8")
    file_data = file.read()
    file.close()

    print(file_data)
    print("类型：", type(file_data))

    # 将字符串转化为字典或列表
    print("***转化yaml数据为字典或列表***")
    data = yaml.load(file_data,Loader=yaml.SafeLoader)
    print(data)
    print("类型：", type(data))
    return data


if __name__ == '__main__':
    # print(random_email())
    get_yaml_data()