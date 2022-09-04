Hearthstone Leaderboard Scraper and Searcher  
炉石传说外服排行榜数据下载器和查询器
# 使用方式
以200个线程下载三服酒馆战棋第8赛季的数据。  
```
dump_all('US', 'battlegrounds', 7, 200)
dump_all('EU', 'battlegrounds', 7, 200)
dump_all('AP', 'battlegrounds', 7, 200)
```

查询某服、某ID（可限定MMR）的MMR和排名。
```
search_id('US', 'wtybill')
search_id('US', 'Apple', _mmr=171)
search_id('US', 'M00NLIGHT')
```
查询结果。
```
Find 11 result(s) of wtybill: (mmr, rank)
(9727, 9)
(7494, 242)
(4306, 12705)
(3939, 16982)
(3232, 28300)
(2326, 54756)
(2317, 55084)
(1168, 119529)
(607, 170984)
(514, 182414)
(316, 204102)

Find 1 result(s) of Apple (mmr=171) : (mmr, rank)
(171, 237705)

M00NLIGHT not found. Showing result(s) of M00NL1GHT with 89/100 simalarity.
Find 1 result(s) of M00NL1GHT: (mmr, rank)
(814, 151210)
```

# 服务器异常
查询条件超出范围时会返回：  
`"rows":[],"pagination":{"totalPages":0,"totalSize":0}`    
但正常查询时有微小概率返回上面的结果，小概率返回：  
`"rows":[],"pagination":{"totalPages":8,"totalSize":200}`
# 特殊说明
* 数据源几乎实时更新，因为诸多原因（数据量大，回复中无用信息多，网速慢），抓到的数据一定有错有漏。
* [ez_aio](https://pypi.org/project/ez-aio )是土制封装，本地修改未上传，可自行手搓。
# 下载速度
以移动宽带WiFi直连为例：  
99线程直连：
  * 欧服20000页用31分钟
  * 美服9000页用14分钟
  * 亚服4000页用5分钟

200线程直连：
  * 欧服21000页用20分钟
  * 美服9000页用9分钟
  * 亚服4100页用3分钟

200线程+不稳定的代理：
  * 欧服21000页用14-16分钟
  * 美服9000页用4-8分钟
  * 亚服4100页用2分钟
