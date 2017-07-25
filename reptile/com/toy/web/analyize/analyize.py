from abc import abstractmethod


class Analyize(object):
    @abstractmethod
    def analyizeDate(self, url):
        pass

    @abstractmethod
    def analyzieUrl(self, url):
        pass
