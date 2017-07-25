from enum import Enum

from com.toy.web.client.zhihu import ZhiHu

client = {}


class ClientType(Enum):
    zhihu = 1


def getClient(clientType):
    if not client.get(clientType) is None:
        return client.get(clientType)
    if clientType == ClientType.zhihu:
        client[clientType] = ZhiHu().session
        return ZhiHu().session


if __name__ == '__main__':
    client = getClient(ClientType.zhihu)
