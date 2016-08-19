#-*- coding:utf-8 -*-
import json
import sys
import os
import urllib.request
import urllib.parse


API_URL = 'https://www.googleapis.com/customsearch/v1?'
QUERY = 'ファッション メンズ'
params = {
    'key': 'Your GCP_API_KEY',
    'q': QUERY,
    'cx': 'Your SearchEngine_ID',
    'alt': 'json',
    'searchType': 'image'
}


def img_search(start=1):
    global params
    params['start'] = int(start)
    img_url = []
    res = urllib.request.urlopen(API_URL + urllib.parse.urlencode(params))
    dump = json.loads(res.read().decode('utf-8'))
    img_url += [result['link'] for result in dump['items']]
    return (img_url, dump['queries']['nextPage'][0]['startIndex'])


def url_download(path,urls,start):
    num = start
    for i in range(len(set(urls))):
        try:
            fn, ext = os.path.splitext(urls[i])
            res = urllib.request.urlopen(urls[i])
            img_file = open(path+'/'+'{0:09d}'.format(num)+ext, 'wb')
            img_file.write(res.read())
            img_file.close()
            num+=1
        except:
            continue

    return num


def update_magic(path, start):
    f = open(path+'/.magic','w')
    if os.path.exists(path+'/.magic')==False:
        f.write('1')
    else:
        f.write(str(start))
    f.close()


def read_magic(path):
    if os.path.exists(path+'/.magic')==False:
        f = open(path+'/.magic','w')
        f.write('1')
        f.close()

    f = open(path+'/.magic','r')
    magic_str = f.read()
    f.close()
    return int(magic_str)


if __name__ == '__main__':
    param = sys.argv
    if len(param) != 2:
        print('python craw save_path')
        sys.exit(-1)

    path = param[1]
    if os.path.exists(path)==False:
        os.mkdir(path)

    magic = read_magic(path)
    
    urls, next_start = img_search(magic)
    url_download(path, urls, magic)

    update_magic(path, next_start)
