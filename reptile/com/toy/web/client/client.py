from abc import abstractmethod

import requests

try:
    import cookielib
except:
    import http.cookiejar as cookielib


class Client(object):
    def __init__(self):
        self.cookiess = 'Cookies'
        self.session = requests.session()

    def loadCookie(self):
        self.session.cookies = cookielib.LWPCookieJar(filename=self.cookiess)
        try:
            self.session.cookies.load(ignore_discard=True)
        except:
            print("Cookie 未能加载")
            self.login()

    @abstractmethod
    def login(self):
        pass

    def getAction(self, url):
        return self.session.get(url, headers=self.headers)

    def postAction(self, url, data):
        return self.session.post(url, data=data, headers=self.headers)
