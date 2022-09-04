from ez_aio import aio, header0, proxy0
from json import loads
from collections import deque
from datetime import datetime
from os import listdir
from thefuzz import fuzz

flag = True
total_pages = 1001
search_data = {
    'AP': None,
    'EU': None,
    'US': None,
}

# search_data = {
#     'AP': {
#         0: {
#             'name1': {(mmr, rank), (mmr, rank)},
#             'name2': {(mmr, rank), (mmr, rank)}
#         },
#         1: {},
#     },
#     'EU': None,
#     'US': None,
# }


def after(raw):
    _data = loads(raw)
    _rows = _data['leaderboard']['rows']
    _results = [(item['rank'], item['accountid'], item['rating']) for item in _rows]
    global total_pages
    _page = _data['leaderboard']['pagination']['totalPages']
    flag0 = True
    if _page in [0, 8]:
        flag0 = False
    elif _page > total_pages:
        total_pages = _page
    return flag0, _results


def dump_all(_region, _mode, _season, li=99, inc=1000):
    global flag, total_pages
    start = 1
    total_pages = 1001
    flag = True
    now = datetime.now().strftime('%Y%m%d_%H_%M_%S')
    fname = f'data/{_region}/{_mode}/{_season}_{now}.txt'
    while flag:
        urls = [
            f'https://hearthstone.blizzard.com/zh-tw/api/community/leaderboardsData?region={_region}&leaderboardId={_mode}&page={page}&seasonId={_season}'
            for page in range(start, min((start + inc), total_pages + 1))]
        _r = aio.get(urls=urls, headers=header0, proxy=proxy0, forced=True, li=li, func=after)
        print(start, start + inc - 1, sep=' -> ', end=' : ')
        data = deque()
        for _recode in _r:
            for _item in _recode:
                data.append(_item)
        print(len(data))
        if len(data) == 0:
            flag = False
        start += inc
        with open(fname, 'a', encoding='utf-8') as f:
            for _item in data:
                print(_item[0], _item[1], _item[2], sep=',', file=f)


def dump_pages(_region, _mode, _season, _range, li=99):
    now = datetime.now().strftime('%Y%m%d_%H_%M_%S')
    fname = f'data/{_region}/{_mode}/{_season}_{now}.txt'
    urls = [
        f'https://hearthstone.blizzard.com/zh-tw/api/community/leaderboardsData?region={_region}&leaderboardId={_mode}&page={page}&seasonId={_season}'
        for page in _range]
    _r = aio.get(urls=urls, headers=header0, forced=True, li=li, func=after)
    data = deque()
    for _recode in _r:
        for _item in _recode:
            data.append(_item)
    with open(fname, 'a', encoding='utf-8') as f:
        for _item in data:
            print(_item[0], _item[1], _item[2], sep=',', file=f)


def search_id(_region, _id, _mmr=None, _mode='battlegrounds'):
    global search_data
    if search_data[_region] is None:
        search_data[_region] = {0: {}, 1: {}}
        files = listdir(f'data/{_region}/{_mode}')
        if files:
            fname = f'data/{_region}/{_mode}/{files[-1]}'
            with open(fname, 'r', encoding='utf-8') as f:
                for line in f.readlines():
                    elements = line.split(',')
                    rank = int(elements[0])
                    mmr = int(elements[-1])
                    name = ','.join(elements[1:-1])
                    if name in search_data[_region][0]:
                        search_data[_region][0][name].add((mmr, rank))
                    else:
                        search_data[_region][0][name] = {(mmr, rank), }
        for file in files[-2:-5:-1]:
            fname = f'data/{_region}/{_mode}/{file}'
            with open(fname, 'r', encoding='utf-8') as f:
                for line in f.readlines():
                    elements = line.split(',')
                    rank = int(elements[0])
                    mmr = int(elements[-1])
                    name = ','.join(elements[1:-1])
                    if name not in search_data[_region][0]:
                        search_data[_region][0][name] = {(mmr, rank), }
    if _id in search_data[_region][0]:
        _id_new = _id
    else:
        _simi, _id_new = max((fuzz.ratio(_id, k), k) for k in search_data[_region][0])
        print(f'{_id} not found. Showing result(s) of {_id_new} with {_simi}/100 simalarity.')
    if _mmr is None:
        res = sorted(search_data[_region][0][_id_new], reverse=True)
        print(f'Found {len(res)} result(s) of {_id_new}: (mmr, rank)')
        for line in res:
            print(line)
    else:
        res = sorted([x for x in search_data[_region][0][_id_new] if (x[0] == _mmr)], reverse=True)
        print(f'Found {len(res)} result(s) of {_id_new} (mmr={_mmr}) : (mmr, rank)')
        for line in res:
            print(line)
    print()


if __name__ == '__main__':
    # region = US EU AP
    # mode = battlegrounds mercenaries standard classic wild
    # season = 战棋4-8赛季=3-7 佣兵7-11 标准狂野经典103-107

    # dump_all usage
    # dump_all('US', 'battlegrounds', 7, 200)
    # dump_all('EU', 'battlegrounds', 7, 200)
    # dump_all('AP', 'battlegrounds', 7, 200)

    # dump_pages usage
    # dump_pages('US', 'battlegrounds', 7, range(5720, 5850), 300)

    # search_id usage
    search_id('US', 'wtybill')
    search_id('US', 'Apple')
    search_id('US', 'Apple', _mmr=171)
    search_id('US', 'M00NLIGHT')
