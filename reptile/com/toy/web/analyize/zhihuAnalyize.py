from com.toy.web.analyize.analyize import Analyize
from bs4 import BeautifulSoup
from com.toy.web import context
from com.toy.web.context import ClientType


class ZhiHuAnalyize(Analyize):
    def __init__(self):
        self.client = context.getClient(ClientType.zhihu)

    def analyizeDate(self, url):
        url = url + '/about'
        rep = self.client.getAction(url)
        soup = BeautifulSoup(rep.content, 'html5lib')
        data = {}
        try:
            name = soup.find('a', {'class': 'name'}).string
            data['name'] = name
        except:
            pass

        try:
            bio = soup.find('div', {'class': 'bio ellipsis'}).string
            data['bio'] = bio
        except:
            pass

        try:
            location = soup.find('span', {'class': 'location item'}).string
            data['location'] = location
        except:
            pass
        try:
            business = soup.find('span', {'class': 'business item'}).string
            data['business'] = business
        except:
            pass

        try:
            employment = soup.find('span', {'class': 'employment item'}).string
            data['employment'] = employment
        except:
            pass
        try:
            position = soup.find('span', {'class': 'position item'}).string
            data['position'] = position
        except:
            pass

        try:
            education = soup.find('span', {'class': 'education item'}).string
            data['education'] = education
        except:
            pass

        try:
            education_extra = soup.find('span', {'class': 'education-extra item'}).string
            data['education_extra'] = education_extra
        except:
            pass

        try:
            content = soup.find('span', {'class': 'content'}).string
            data['content'] = content
        except:
            pass
        del rep
        del data
        return data

    def analyizeUrl(self, url, num=10):
        url1 = url + '/followees'
        rep = self.client.getAction(url1)
        soup = BeautifulSoup(rep.content, 'html5lib')
        followeesurls = []
        followees = soup.find_all('a', {'class': 'zg-link author-link'})
        if followees.__len__() < num:
            num = followees.__len__()
        for i in range(num):
            followeesurls.append(followees[i].get('href'))

        url2 = url + '/followers'
        rep = self.client.getAction(url2)
        soup = BeautifulSoup(rep.content, 'html5lib')
        followersurls = []
        followers = soup.find_all('a', {'class': 'zg-link author-link'})
        if followers.__len__() < num:
            num = followers.__len__()
        for i in range(num):
            followersurls.append(followees[i].get('href'))
        del rep
        del soup
        return followeesurls, followersurls
