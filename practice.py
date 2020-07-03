import requests
URL = 'http://naver.com/'
response = requests.get(URL)
print(response.text)