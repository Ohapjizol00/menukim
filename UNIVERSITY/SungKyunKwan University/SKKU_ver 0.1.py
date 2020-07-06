#!/usr/bin/env python3
#
#  Copyright (c) 2020 by 5HAPZIJOL, All rights reserved.
#
#  Project             : MenuKim_SKKU
#
#  Starting date       : June. 30, 2020
#
#  Code Responsibility : Woo Sung Chung  (wsung0011@naver.com)
#
#  py version          : made by CPython 3.8.3, 64-bit
#
#  Modification History:
#     * version 0.1, by Woo Sung CHung, Jul. 07, 2020
#       - 1st released on this day.
#
'''Sample of menukim in SKKU

make the csv file contains menu in nowaday. Only SKKU '자연과학캠퍼스'
csv encoding = 'utf-8-sig,'

_date_change   : get the right url with changing the url's date
_get_menu      : Fill the cafe_list with menu
_get_cafeteria : Get the name of cafeteria *recommended
_###_URL       : URL of campussite (might be changed)

What should be Imporved:
    1. Korean brokens when encoding='uft-8', we will not use 'CP949'.
    2. unefficient and slow.
    3. we donot know all bs4 so should be changed.
    4. '인문사회과학캠퍼스' should be considered.
    5. If university change the url a little, it does not works.
    6. Could not confirm the operation on other os except window.
'''
from bs4 import BeautifulSoup
from urllib.request import urlopen

import pandas as pd
import csv
import requests
import re
import time


def _date_change(URL):
    """Change the date to now time.

    date which in url in URL is ####-##-##. So this function change that string
    to now date depend on your computer calendar.

    :param URL: URL which would be changed
    :type URL:  list

    :return: none

    :precondition: each url in URL should be string type
    """
    assert isinstance(URL, list), \
        "Input should be list"

    now_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    for index, url in enumerate(URL):
        # Check whether url is string
        assert isinstance(url, str), \
            "element in URL should be str type"
        URL[index] = url.replace('####-##-##', now_time)


def _get_menu(URL_list, cafe_list):
    """Fill the cafe_list with menu.

    As SKKU '자연과학캠퍼스' set 'class = menue_title' in every site,
    beautifulsoup.select('class')can find menu_title
    But if class name is changed, you should change those also.

    :param URL_list: list of URL which are changed
    :type URL_list:  list

    :param cafe_list: empty list(maybe) which should be filled with menu
    :type cafe_list:  list

    :return: none

    :precondition: each url in URL should be string type
                   cafe_list should be empty

    [Notice]  You should run date_change before running this function.
    """
    assert isinstance(cafe_list, list),\
        'cafe_list should be list'
    assert cafe_list == [],\
        'cafe_list should be empty'

    for URL in URL_list:
        req = requests.get(URL)
        html = req.text

        # html을 beautifulsoup에 적용
        bs = BeautifulSoup(html, 'html.parser')
        # menu select
        menu_list = bs.select('.menu_title')

        if menu_list == []:
            cafe_list.append('자료없음')

        else:
            # make list which control the data
            d_list = []
            for x in range(len(menu_list)):
                d_list.append(bs.select(".menu_title")[x].get_text())

            # Delete the escape letter in menu
            d_list = [menu.strip() for menu in d_list]
            d_list = [menu.replace('\n', '/') for menu in d_list]

            # If menu is more than two
            if len(d_list) != 1:
                d_list = ['or'.join(d_list)]

            cafe_list += d_list


def _get_cafeteria(URL):
    '''
    Get the name of cafeteria.

    maybe you can skip this function.
    But as the name of caferia is not a CONSTANT, I recommend to us this.

    :param URL: URL where the name of cafeteria exist.
    :type URL:  str

    :return: name of cafeteria
    :rtype:  str

    :precondition: url should be string type
    '''
    assert isinstance(URL, str),\
        'Is URL is real url?'
    req = requests.get(URL)
    html = req.text

    # html을 beautifulsoup에 적용
    bs = BeautifulSoup(html, 'html.parser')
    # menu select
    name = bs.select('.info_tit')[0].get_text()
    name = name.strip()

    return name


# 행단골
_HDG_URL = [
    "https://www.skku.edu/skku/campus/support/welfare_11_1.do?mode=info&srDt=####-##-##&srCategory=L&conspaceCd=20201104&srResId=3&srShowTime=D",
    "https://www.skku.edu/skku/campus/support/welfare_11_1.do?mode=info&srDt=####-##-##&srCategory=B&conspaceCd=20201104&srResId=3&srShowTime=D",
    "https://www.skku.edu/skku/campus/support/welfare_11_1.do?mode=info&srDt=####-##-##&srCategory=D&conspaceCd=20201104&srResId=3&srShowTime=D",
    "https://www.skku.edu/skku/campus/support/welfare_11_1.do?mode=info&srDt=####-##-##&srCategory=S&conspaceCd=20201104&srResId=3&srShowTime=D",
    "https://www.skku.edu/skku/campus/support/welfare_11_1.do?mode=info&srDt=####-##-##&srCategory=R&conspaceCd=20201104&srResId=3&srShowTime=D"
]

# 구시재
_GSJ_URL = [
    "https://www.skku.edu/skku/campus/support/welfare_11_1.do?mode=info&srDt=####-##-##&srCategory=L&conspaceCd=20201040&srResId=11&srShowTime=D",
    "https://www.skku.edu/skku/campus/support/welfare_11_1.do?mode=info&srDt=####-##-##&srCategory=B&conspaceCd=20201040&srResId=11&srShowTime=D",
    "https://www.skku.edu/skku/campus/support/welfare_11_1.do?mode=info&srDt=####-##-##&srCategory=D&conspaceCd=20201040&srResId=11&srShowTime=D",
    "https://www.skku.edu/skku/campus/support/welfare_11_1.do?mode=info&srDt=####-##-##&srCategory=S&conspaceCd=20201040&srResId=11&srShowTime=D",
    "https://www.skku.edu/skku/campus/support/welfare_11_1.do?mode=info&srDt=####-##-##&srCategory=R&conspaceCd=20201040&srResId=11&srShowTime=D"
]

# 해오름
_HOR_URL = [
    "https://www.skku.edu/skku/campus/support/welfare_11_1.do?mode=info&srDt=####-##-##&srCategory=L&conspaceCd=20201097&srResId=10&srShowTime=D",
    "https://www.skku.edu/skku/campus/support/welfare_11_1.do?mode=info&srDt=####-##-##&srCategory=B&conspaceCd=20201097&srResId=10&srShowTime=D",
    "https://www.skku.edu/skku/campus/support/welfare_11_1.do?mode=info&srDt=####-##-##&srCategory=D&conspaceCd=20201097&srResId=10&srShowTime=D",
    "https://www.skku.edu/skku/campus/support/welfare_11_1.do?mode=info&srDt=####-##-##&srCategory=S&conspaceCd=20201097&srResId=10&srShowTime=D",
    "https://www.skku.edu/skku/campus/support/welfare_11_1.do?mode=info&srDt=####-##-##&srCategory=R&conspaceCd=20201097&srResId=10&srShowTime=D"
]

if __name__ == "__main__":

    _cafe_dict = {}
    _HDG_list = []
    _GSJ_list = []
    _HOR_list = []
    sort_list = ["중식", "조식", "석식", "간식", "예약"]

    #
    # 행단골
    #
    _date_change(_HDG_URL)
    _HDG_name = _get_cafeteria(_HDG_URL[0])
    _get_menu(_HDG_URL, _HDG_list)
    _cafe_dict[_HDG_name] = _HDG_list

    #
    # 구시재
    #
    _date_change(_GSJ_URL)
    _GSJ_name = _get_cafeteria(_GSJ_URL[0])
    _get_menu(_GSJ_URL, _GSJ_list)
    _cafe_dict[_GSJ_name] = _GSJ_list

    #
    # 해오름
    #
    _date_change(_HOR_URL)
    _HOR_name = _get_cafeteria(_HOR_URL[0])
    _get_menu(_HOR_URL, _HOR_list)
    _cafe_dict[_HOR_name] = _HOR_list

    _csv_file = pd.DataFrame(_cafe_dict, index=sort_list)
    _csv_file.to_csv("test.csv", "w", encoding="utf-8-sig")
