# write your Topcomments
'''
write your docstring
'''


from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
from urllib.error import HTTPError

import pandas as pd
import requests

URL ='https://www.ewha.ac.kr/ewha/life/restaurant.do?mode=view&articleNo=905&article.offset=0&articleLimit=10&srDt=2020-07-20'
html = urlopen(URL)
BS = bs(html, "html.parser")
menu = BS.find("", {"class":"b-menu b-menu-l lunch"})
