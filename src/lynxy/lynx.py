import requests
try:
    requests.post(url='https://www.google.com')
except Exception as e:
    print('cannot make connection')
    print(e)