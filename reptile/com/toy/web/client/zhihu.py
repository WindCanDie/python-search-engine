from com.toy.web.client.client import Client

try:
    import cookielib
except:
    import http.cookiejar as cookielib
import re
import time
import os.path

try:
    from PIL import Image
except:
    pass


class ZhiHu(Client):
    def __init__(self):
        super().__init__()
        self.cookiess = 'ZhiHuCookies'
        self.agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                     'Chrome/59.0.3071.115 Mobile Safari/537.36 '
        self.headers = {
            "Host": "www.zhihu.com",
            "Referer": "https://www.zhihu.com/",
            'User-Agent': self.agent
        }
        self.account = "*"
        self.secret = "*"
        self.loadCookie()

    def isLogin(self):
        # 通过查看用户个人信息来判断是否已经登录
        url = "https://www.zhihu.com/settings/profile"
        login_code = self.session.get(url, headers=self.headers, allow_redirects=False).status_code
        if login_code == 200:
            return True
        else:
            return False
            # 获取验证码

    def get_captcha(self):
        t = str(int(time.time() * 1000))
        captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
        r = self.session.get(captcha_url, headers=self.headers)
        with open('captcha.jpg', 'wb') as f:
            f.write(r.content)
            f.close()
        # 用pillow 的 Image 显示验证码
        # 如果没有安装 pillow 到源代码所在的目录去找到验证码然后手动输入
        try:
            im = Image.open('captcha.jpg')
            im.show()
            im.close()
        except:
            print(u'请到 %s 目录找到captcha.jpg 手动输入' % os.path.abspath('captcha.jpg'))
        captcha = input("please input the captcha\n>")
        return captcha

    def get_xsrf(self):
        """
            _xsrf 是一个动态变化的参数
        """
        index_url = 'https://www.zhihu.com'
        # 获取登录时需要用到的_xsrf
        index_page = self.session.get(index_url, headers=self.headers)
        html = index_page.text
        pattern = r'name="_xsrf" value="(.*?)"'
        # 这里的_xsrf 返回的是一个list
        _xsrf = re.findall(pattern, html)
        return _xsrf[0]

    def Actiologin(self, secret, account):
        _xsrf = self.get_xsrf()
        self.headers["X-Xsrftoken"] = _xsrf
        self.headers["X-Requested-With"] = "XMLHttpRequest"
        # 通过输入的用户名判断是否是手机号
        if re.match(r"^1\d{10}$", account):
            print("手机号登录 \n")
            post_url = 'https://www.zhihu.com/login/phone_num'
            postdata = {
                '_xsrf': _xsrf,
                'password': secret,
                'phone_num': account
            }
        else:
            if "@" in account:
                print("邮箱登录 \n")
            else:
                print("你的账号输入有问题，请重新登录")
                return 0
            post_url = 'https://www.zhihu.com/login/email'
            postdata = {
                '_xsrf': _xsrf,
                'password': secret,
                'email': account
            }
        # 不需要验证码直接登录成功
        login_page = self.session.post(post_url, data=postdata, headers=self.headers)
        login_code = login_page.json()
        if login_code['r'] == 1:
            # 不输入验证码登录失败
            # 使用需要输入验证码的方式登录
            postdata["captcha"] = self.get_captcha()
            login_page = self.session.post(post_url, data=postdata, headers=self.headers)
            login_code = login_page.json()
            print(login_code['msg'])
        # 保存 cookies 到文件，
        # 下次可以使用 cookie 直接登录，不需要输入账号和密码
        self.session.cookies.save()

    def login(self):
        if self.isLogin():
            print('您已经登录')
        else:
            self.Actiologin(self.secret, self.account)
