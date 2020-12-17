"""
提供获取网络信息的工具

"""
import json

import requests


def getWebDate(url, date):
    """
    这个函数来获取网站上的数据
    :param url: 网址
    :param date: 需要给网址发送的信息
    :return: 返回一个json数据
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
     Chrome/64.0.3282.168 Safari/537.36'}
    try:
        htmlDate = requests.get(url + date, headers=headers).json()
    except json.decoder.JSONDecodeError:
        print('获取网络数据出错')
        return None
    return htmlDate['data']


if __name__ == '__main__':
    requestDate = 'tn=resultjson_com&ipn=rj&fp=result&ie=utf-8&oe=utf-8&word={0}&pn={1}&rn={2}' \
        .format('', '', '')
    # date = urllib.parse.urlencode(date).encode('utf-8')
    print(getWebDate('https://image.baidu.com/search/acjson?', requestDate))
