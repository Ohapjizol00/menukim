#!/usr/bin/env python3
#
#  Copyright (c) 2020 by 5HAPZIJOL, All rights reserved.
#
#  Project             : MenuKim_SKKU
#
#  Starting date       : July. 08, 2020
#
#  Code Responsibility : Woo Sung Chung  (wsung0011@naver.com)
#
#  py version          : made by CPython 3.8.3, 64-bit
#
#  Modification History:
#     * version 0.1.0, by Woo Sung CHung, Jul. 07, 2020
#       - 1st released on this day.
#
'''Sample of menukim in SKKU
This time, using the findAll()
'''
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
from urllib.error import HTTPError

import pandas as pd
import requests
import time

def a_check(URL):
    """check link"""
    html = urlopen(URL)
    bsobj = bs(html, 'html.parser')
    for link in bsobj.findAll('a'):
        if 'href' in link.attrs:
            print(link.attrs['href'])

def _date_change(URL, now_time):
    """Change the date to now time.

    date which in url in URL is ####-##-##. So this function change that string
    to now date depend on your computer calendar.

    :param URL: URL which would be changed
    :type URL:  list

    :param now_time: date of now
    :type now_time:  string

    :return: none

    :precondition: each url in URL should be string type
    """
    assert isinstance(URL, list), \
        "Input should be list"
    assert isinstance(now_time, str), \
        "Does now_time is string?"

    for index, url in enumerate(URL):
        # Check whether url is string
        assert isinstance(url, str), \
            "element in URL should be str type"
        URL[index] = url.replace('####-##-##', now_time)

def _get_menu(URL, cafe_list):
    """"Fill the cafe_list with menu.

    As SKKU '인문사회과학캠퍼스' set 'class = menue_title' in every site,
    beautifulsoup.select('class')can find menu_title
    But if class name is changed, you should change those also.

    :param URL_list: list of URL which are changed
    :type URL_list:  list

    :param cafe_list: empty list(maybe) which should be filled with menu
    :type cafe_list:  list

    :return: none

    :precondition: each url in URL should be string type
                   cafe_list should be empty

    [Notice]  You should run date_change before running this function."""
    for url in URL:
        html = urlopen(url)
        BSobj = bs(html, "html.parser")
        
        menu_list = BSobj.findAll("",{"class":"menu_title"})
        
        if menu_list == []:
                cafe_list.append('자료없음')

        else:
            # make list which control the data
            d_list = [each_menu.get_text() for each_menu in menu_list]

            # Delete the escape letter in menu
            d_list = [menu.strip() for menu in d_list]
            d_list = [menu.replace('\n', '/') for menu in d_list]

            # If menu is more than two
            if len(d_list) != 1:
                d_list = ['or'.join(d_list)]

            cafe_list += d_list


def _get_cafeteria(URL):
    """Get the name of cafeteria.

    maybe you can skip this function.
    But as the name of caferia is not a CONSTANT, I recommend to us this.

    :param URL: URL where the name of cafeteria exist.
    :type URL:  str

    :return: name of cafeteria
    :rtype:  str

    :precondition: url should be string type"""
    html = urlopen(URL)
    BSobj = bs(html, "html.parser")

    cafe_name = BSobj.find("",{"class":"info_tit"}).h5
    return cafe_name.get_text()

# 패컬티 식당
_FAC_URL = [
    "https://www.skku.edu/skku/campus/support/welfare_11.do?mode=info&srDt=####-##-##&srCategory=L&conspaceCd=10201030&srResId=1&srShowTime=W",
    "https://www.skku.edu/skku/campus/support/welfare_11.do?mode=info&srDt=####-##-##&srCategory=B&conspaceCd=10201030&srResId=1&srShowTime=W",
    "https://www.skku.edu/skku/campus/support/welfare_11.do?mode=info&srDt=####-##-##&srCategory=D&conspaceCd=10201030&srResId=1&srShowTime=W",
    "https://www.skku.edu/skku/campus/support/welfare_11.do?mode=info&srDt=####-##-##&srCategory=S&conspaceCd=10201030&srResId=1&srShowTime=W",
    "https://www.skku.edu/skku/campus/support/welfare_11.do?mode=info&srDt=####-##-##&srCategory=R&conspaceCd=10201030&srResId=1&srShowTime=W"
]

# 은행골
_BAN_URL = [
    "https://www.skku.edu/skku/campus/support/welfare_11.do?mode=info&srDt=####-##-##&srCategory=L&conspaceCd=10201031&srResId=2&srShowTime=D",
    "https://www.skku.edu/skku/campus/support/welfare_11.do?mode=info&srDt=####-##-##&srCategory=B&conspaceCd=10201031&srResId=2&srShowTime=D",
    "https://www.skku.edu/skku/campus/support/welfare_11.do?mode=info&srDt=####-##-##&srCategory=D&conspaceCd=10201031&srResId=2&srShowTime=D",
    "https://www.skku.edu/skku/campus/support/welfare_11.do?mode=info&srDt=####-##-##&srCategory=S&conspaceCd=10201031&srResId=2&srShowTime=D",
    "https://www.skku.edu/skku/campus/support/welfare_11.do?mode=info&srDt=####-##-##&srCategory=R&conspaceCd=10201031&srResId=2&srShowTime=D"
]

# 법고을
_LAW_URL = [
    "https://www.skku.edu/skku/campus/support/welfare_11.do?mode=info&srDt=####-##-##&srCategory=L&conspaceCd=10201034&srResId=4&srShowTime=W",
    "https://www.skku.edu/skku/campus/support/welfare_11.do?mode=info&srDt=####-##-##&srCategory=B&conspaceCd=10201034&srResId=4&srShowTime=W",
    "https://www.skku.edu/skku/campus/support/welfare_11.do?mode=info&srDt=####-##-##&srCategory=D&conspaceCd=10201034&srResId=4&srShowTime=W",
    "https://www.skku.edu/skku/campus/support/welfare_11.do?mode=info&srDt=####-##-##&srCategory=S&conspaceCd=10201034&srResId=4&srShowTime=W",
    "https://www.skku.edu/skku/campus/support/welfare_11.do?mode=info&srDt=####-##-##&srCategory=R&conspaceCd=10201034&srResId=4&srShowTime=W"
]

# 옥류천
_OAK_URL = [
    "https://www.skku.edu/skku/campus/support/welfare_11.do?mode=info&srDt=####-##-##&srCategory=L&conspaceCd=10201032&srResId=5&srShowTime=D",
    "https://www.skku.edu/skku/campus/support/welfare_11.do?mode=info&srDt=####-##-##&srCategory=B&conspaceCd=10201032&srResId=5&srShowTime=D",
    "https://www.skku.edu/skku/campus/support/welfare_11.do?mode=info&srDt=####-##-##&srCategory=D&conspaceCd=10201032&srResId=5&srShowTime=D",
    "https://www.skku.edu/skku/campus/support/welfare_11.do?mode=info&srDt=####-##-##&srCategory=S&conspaceCd=10201032&srResId=5&srShowTime=D",
    "https://www.skku.edu/skku/campus/support/welfare_11.do?mode=info&srDt=####-##-##&srCategory=R&conspaceCd=10201032&srResId=5&srShowTime=D"
]

# 금잔디
_GOL_URL =[
    "https://www.skku.edu/skku/campus/support/welfare_11.do?mode=info&srDt=####-##-##&srCategory=L&conspaceCd=10201033&srResId=6&srShowTime=D",
    "https://www.skku.edu/skku/campus/support/welfare_11.do?mode=info&srDt=####-##-##&srCategory=B&conspaceCd=10201033&srResId=6&srShowTime=D",
    "https://www.skku.edu/skku/campus/support/welfare_11.do?mode=info&srDt=####-##-##&srCategory=D&conspaceCd=10201033&srResId=6&srShowTime=D",
    "https://www.skku.edu/skku/campus/support/welfare_11.do?mode=info&srDt=####-##-##&srCategory=S&conspaceCd=10201033&srResId=6&srShowTime=D",
    "https://www.skku.edu/skku/campus/support/welfare_11.do?mode=info&srDt=####-##-##&srCategory=R&conspaceCd=10201033&srResId=6&srShowTime=D"
]


if __name__ == "__main__":
    _cafe_dict = {}
    _FAC_list = []
    _BAN_list = []
    _LAW_list = []
    _OAK_list = []
    _GOL_list = []
    sort_list = ["중식", "조식", "석식", "간식", "예약"]

    now_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))

    # 패컬티 식당
    _date_change(_FAC_URL, now_time)
    _FAC_name = _get_cafeteria(_FAC_URL[0])
    _get_menu(_FAC_URL, _FAC_list)
    _cafe_dict[_FAC_name] = _FAC_list

    # 은행골
    _date_change(_BAN_URL, now_time)
    _BAN_name = _get_cafeteria(_BAN_URL[0])
    _get_menu(_BAN_URL, _BAN_list)
    _cafe_dict[_BAN_name] = _BAN_list

    # 법고을
    _date_change(_LAW_URL, now_time)
    _LAW_name = _get_cafeteria(_LAW_URL[0])
    _get_menu(_LAW_URL, _LAW_list)
    _cafe_dict[_LAW_name] = _LAW_list

    # 옥류천
    _date_change(_OAK_URL, now_time)
    _OAK_name = _get_cafeteria(_OAK_URL[0])
    _get_menu(_OAK_URL, _OAK_list)
    _cafe_dict[_OAK_name] = _OAK_list

    # 금잔디
    _date_change(_GOL_URL, now_time)
    _GOL_name = _get_cafeteria(_GOL_URL[0])
    _get_menu(_GOL_URL, _GOL_list)
    _cafe_dict[_GOL_name] = _GOL_list

    _csv_file = pd.DataFrame(_cafe_dict, index=sort_list)
    _csv_file.to_csv("menu_HS.csv", encoding="utf-8-sig")
