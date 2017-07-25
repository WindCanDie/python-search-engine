from abc import abstractmethod

import requests

try:
    import cookielib
except:
    import http.cookiejar as cookielib


class Client:
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
