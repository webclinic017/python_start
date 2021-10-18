# -*- coding: utf-8 -*-
import json
import time
from datetime import datetime
import os
import pandas as pd
import random
import requests

pd.set_option('display.max_columns', 500)


def get_content(target_url, max_retry_times=10, sleep_seconds=None):
    if not sleep_seconds:
        sleep_seconds = random.randint(3, 10)

    for times in range(max_retry_times):
        try:
            r = requests.get(target_url)
            content = json.loads(r.text)
            return content
        except Exception as e:
            print("Get Content Error. times=", times, ",", e)
        finally:
            time.sleep(sleep_seconds)
    raise ValueError("Get Content Error. url=" + target_url)


def get_this_data_from_sina():
    target_url = "https://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData"
    payload = {
        "num": 80,
        "sort": "changepercent",
        "asc": 0,
        "node": "hs_a",
        "_s_r_a": "setlen"
    }
    all_list = []
    page = 56
    while True:
        page = page + 1
        payload["page"] = page
        r = requests.get(target_url, params=payload)
        one_page_list = get_content(r.url)
        if not one_page_list:
            break
        all_list.extend(one_page_list)
    return all_list


def get_this_file_name():
    return "../data/stock_daily_incr_data/%s.csv" % (datetime.now().strftime("%Y-%m-%dT%H:00:00"))


def claw_if_file_not_exit():
    this_file_name = get_this_file_name()
    if not os.path.exists(this_file_name):
        content_of_today = get_this_data_from_sina()
        today_dataframe = pd.DataFrame(content_of_today)
        today_dataframe.to_csv(this_file_name, index_label="index")


def main():
    claw_if_file_not_exit()


if __name__ == '__main__':
    main()
