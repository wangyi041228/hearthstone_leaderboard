from ez_aio import aio, header0
from json import loads
from collections import deque
from datetime import datetime


def after(raw):
    _data = loads(raw)
    _rows = _data['leaderboard']['rows']
    _results = [(item['rank'], item['accountid'], item['rating']) for item in _rows]
    return _results


def main(_region, _mode, _season):
    start = 1
    inc = 1000
    flag = True
    now = datetime.now().strftime('%Y%m%d_%H_%M_%S')
    fname = f'{_region}_{_mode}_{_season}_{now}.txt'
    while flag:
        urls = [
            f'https://hearthstone.blizzard.com/zh-tw/api/community/leaderboardsData?region={_region}&leaderboardId={_mode}&page={page}&seasonId={_season}'
            for page in range(start, start + inc)]
        _r = aio.get(urls=urls, headers=header0, forced=True, func=after)
        print(start, start + inc - 1, sep=' -> ', end=' : ')
        data = deque()
        for _recode in _r:
            for _item in _recode:
                data.append(_item)
        print(len(data))
        if len(data) == 0:
            flag = False
        else:
            start += inc
            with open(fname, 'a', encoding='utf-8') as f:
                for _item in data:
                    print(_item[0], _item[1], _item[2], sep=',', file=f)


if __name__ == '__main__':
    # region = US EU AP
    # mode = battlegrounds mercenaries standard classic wild
    # season = 战棋4-8赛季=3-7 佣兵7-11 标准狂野经典103-107
    main('US', 'battlegrounds', 7)
    main('EU', 'battlegrounds', 7)
    main('AP', 'battlegrounds', 7)
