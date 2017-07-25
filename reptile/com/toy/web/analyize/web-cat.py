from bs4 import BeautifulSoup

import zhihu

session = zhihu.getClient()


def getAction(url):
    return session.get(url, headers=zhihu.headers)


def postAction(url, data):
    return session.post(url, data=data, headers=zhihu.headers)


if __name__ == '__main__':
    rep = getAction("https://www.zhihu.com/people/yunshu/about")
    soup = BeautifulSoup(rep.content, 'html5lib')
    data = {}
    try:
        name = soup.find('a', {'class': 'name'}).string
        data['name'] = name
    except:
        name = None

    try:
        bio = soup.find('div', {'class': 'bio ellipsis'}).string
        data['bio'] = bio
    except:
        name = None

    try:
        location = soup.find('span', {'class': 'location item'}).string
        data['location'] = location
    except:
        location = None
    try:
        business = soup.find('span', {'class': 'business item'}).string
        data['business'] = business
    except:
        business = None

    try:
        employment = soup.find('span', {'class': 'employment item'}).string
        data['employment'] = employment
    except:
        employment = None
    try:
        position = soup.find('span', {'class': 'position item'}).string
        data['position'] = position
    except:
        position = None

    try:
        education = soup.find('span', {'class': 'education item'}).string
        data['education'] = education
    except:
        education = None

    try:
        education_extra = soup.find('span', {'class': 'education-extra item'}).string
        data['education_extra'] = education_extra
    except:
        education = None

    try:
        content = soup.find('span', {'class': 'content'}).string
        data['content'] = content
    except:
        education = None

    for zm in soup.find_all('div', {'class': 'zm-profile-module zg-clear'}):
        try:
            moade = zm.span.string
            print(moade)
            for obj in zm.find_all('div', {'class': 'ProfileItem-text ProfileItem-text--bold'}):
                try:
                    v = ''
                    for sub in obj.children:
                        v = v + sub.string
                    print(v)
                except:
                    print()
        except:
            print()
    print(data)
