# write your Topcomments
'''
write your docstring
'''
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
from urllib.error import HTTPError

import pandas as pd
import requests
import time

html=urlopen("https://www.inha.ac.kr/diet/kr/2/view.do") #7/13~17
a=bs(html.read(),"html.parser")
print(a)
