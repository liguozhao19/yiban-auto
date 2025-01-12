#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Rekord
# @Date: 2022-02-06


import time
import datetime
import json
from yiban import Yiban
import requests
from sendemail import start_email


def main_handler(data=None, extend=None):
    # load json datas
    with open('config.json', encoding='utf-8') as f:
        json_datas = json.load(f)['Forms']
    # print(json_datas)

    total_msg = ''
    for data in json_datas:
        success_flag = False
        max_run_count = 10 # 最大运行次数
        while success_flag == False and max_run_count > 0:
            success_flag = True
            nickname = data['UserInfo']['NickName']
            # Time converted to UTC/GMT+08:00
            today = datetime.datetime.today() + datetime.timedelta(hours=8-int(time.strftime('%z')[0:3]))
            msg = f"%d-%02d-%02d %02d:%02d {nickname}|yiban punch：" % (today.year, today.month, today.day, today.hour, today.minute)
            address_info = data['FormInfo']['AddressInfo']
            try:
                yiban = Yiban(data['UserInfo']['Mobile'], data['UserInfo']['Password'], today)
                yiban.submit_task(address_info)
                msg = f'{msg}Success.'
            # If an error occurs due to network problems, the program will continue to run
            except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
                success_flag = False
                max_run_count -= 1
            except Exception as e:
                msg = f'{msg}{e}'
            finally:
                if success_flag == True:                
                    print(msg)
                    total_msg = f'{total_msg}\n\n{msg}'
                time.sleep(1)
    # print(total_msg)
    # send email
    start_email(total_msg)


if __name__ == '__main__':
    main_handler()