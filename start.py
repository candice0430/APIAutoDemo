# -*- coding: UTF-8 -*-

# author:p_ppcjchen
# create by:2022/3/13/10:08 上午

from utils.HTMLTestRunner_cn import HTMLTestRunner
import os
import unittest
from utils.common import get_report_path


def run():
    test_path = os.path.dirname(__file__) + os.sep + "tests"
    report_name = get_report_path()
    suite = unittest.defaultTestLoader.discover(test_path,"test_*",top_level_dir=None)
    with open(report_name,"wb") as f:
        runner = HTMLTestRunner(
            stream = f,
            title = "接口自动化 report",
            description= "自动化测试报告",
            retry = 0,
            save_last_try = True
        )
        runner.run(suite)


if __name__ == '__main__':
    run()

