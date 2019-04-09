#! /usr/bin/env python
# -*- coding: utf-8 -*-

#    File Name：       check_account_expires
#    Description :
#    Author :          SanYapeng
#    date：            2019-04-04
#    Change Activity:  2019-04-04

import time
import json
import requests


account_info = {
    "linuxsan@163.com": "2019-11-10 00:00:00",
}
day30 = 2592000
day10 = 864000
day5 = 432000
day1 = 86400   # 18714


def send_info(message):

    api_url = "https://oapi.dingtalk.com/robot/send"
    querystring = {"access_token": "钉钉机器人token"}
    data = {
        "megtype": "text",
        "text": {
            "content": message
            },
        "at": {
            'isAtAll': True
            }

        }
    json_str = json.dumps(data)
    headers = {
        'content-type': "application/json",
        'cache-control': "no-cache",
    }

    req = requests.post(url=api_url, data=json_str, headers=headers, params=querystring)
    if req.status_code == requests.codes.ok:
        return True
    else:
        return False


def check():
    """
    检查并返回信息
    :return:
    """
    for k, v in account_info.items():

        # 将到期时间转换为时间戳
        expire_time_stamp = time.mktime(time.strptime(v, '%Y-%m-%d %H:%M:%S'))

        # 获取现在的时间戳
        now_time_stamp = time.time()

        # 获取时间戳的差值

        time_difference = int(expire_time_stamp) - int(now_time_stamp)

        # 调试时间
        # 30天
        # time_difference = 2505610
        # 10天
        # time_difference = 259210
        # 5天以内
        # time_difference = 259210
        # 通过对比报警
        if day30 - day1 <= time_difference <= day30:
            message = "此 {} 账户到期时间还有30天，请注意续费情况".format(k)
            send_info(message)

        elif day10 - day1 <= time_difference <= day10:
            message = "此 {} 账户到期时间还有10天，请注意续费情况".format(k)
            send_info(message)

        elif time_difference <= day5:
            day = time_difference / 24 / 60 / 60
            message = "此 {} 账户到期时间还有{}天，请注意续费情况".format(k, day)
            send_info(message)
            print time_difference
        else:
            message = "此 {} 账户到期时间还有N多天".format(k)
            send_info(message)
            continue


if __name__ == '__main__':
    check()
