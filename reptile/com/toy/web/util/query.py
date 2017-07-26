import threading


class ArrayQuery:
    def __init__(self, upperNum=10000):
        self.notFull = threading.Condition()
        self.array = []
        self.upperNum = upperNum
        self.num = 0
        self.notEmpty = threading.Condition()
        self.numLock = threading.Lock()
        self.head = self.last = Node(None)

    def getAndIncrement(self):
        self.numLock.acquire()
        try:
            c = self.num
            self.num = self.num + 1
            return c
        finally:
            self.numLock.release()

    def getAndDecrement(self):
        self.numLock.acquire()
        try:
            c = self.num
            self.num = self.num - 1
            return c
        finally:
            self.numLock.release()

    def signalNotEmpty(self):
        self.notEmpty.acquire()
        try:
            self.notEmpty.notify()
        finally:
            self.notEmpty.release()

    def signalNotFull(self):
        self.notFull.acquire()
        try:
            self.notFull.notify()
        finally:
            self.notFull.release()

    def enqueue(self, data):
        self.last.next = data
        self.last = data

    def dequeue(self):
        h = self.head
        first = h.next
        h.next = h
        self.head = first
        x = first.item
        first.item = None
        return x

    def put(self, data):
        if data is None: raise Exception("data is None")
        self.notFull.acquire()
        try:
            count = self.num
            while count == self.upperNum:
                self.notFull.wait()
            self.enqueue(Node(data))
            c = self.getAndIncrement()
            self.num = + 1
            if c + 1 < self.upperNum:
                self.notFull.notify()
        finally:
            self.notFull.release()
        if c is 0:
            self.signalNotEmpty()

    def take(self):
        self.notEmpty.acquire()
        try:
            count = self.num
            while count is 0:
                self.notEmpty.wait()
            data = self.dequeue()
            c = self.getAndDecrement()
            self.num = - 1
            if c - 1 > 0:
                self.notEmpty.notify()
        finally:
            self.notEmpty.release()
        if c is self.upperNum:
            self.signalNotFull()
        return data


class Node:
    def __init__(self, data):
        self.item = data
        self.next = None


if __name__ == '__main__':
    list = ArrayQuery()
    for i in range(1000):
        list.put(i)
    for i in range(1000):
        print(list.take())
