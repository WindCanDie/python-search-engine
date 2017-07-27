import queue
import threading


from com.toy.web.analyize.zhihuAnalyize import ZhiHuAnalyize
from com.toy.web.util.query import ArrayQuery


class myThread(threading.Thread):
    def __init__(self, query):
        threading.Thread.__init__(self)
        self.query = query

    def run(self):
        while True:
            url = self.query.get()
            print(url)
            followees, followers = ZhiHuAnalyize().analyizeUrl(url)
            for f in followees:
                print(f)
                self.query.put(f)
            for f in followers:
                print(f)
                self.query.put(f)


if __name__ == '__main__':
    query = queue.Queue(10000000)
    query.put('https://www.zhihu.com/people/yunshu')
    list = []
    for i in range(10):
        t = myThread(query)
        t.start()
        list.append(t)
    for t in list:
        t.join()
