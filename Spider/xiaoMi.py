# encoding: utf-8
"""
@author: jason
@contact: scnu_wang@163.com
@site: www.163.com

"""
import requests
import json
import urllib.parse

#构建访问参数，获取所有的产品列表
headers = {'Connection':'keep-alive','Accept-Encoding':'gzip, deflate, br','Accept-Language':'zh-CN,zh;q=0.8','content-type':'application/x-www-form-urlencoded','Referer':'https://home.mi.com/crowdfundinglist','User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'}
data = 'data=%7B%22HomeList%22%3A%7B%22model%22%3A%22Homepage%22%2C%22action%22%3A%22BuildHome%22%2C%22parameters%22%3A%7B%22id%22%3A12%7D%7D%7D'
r=requests.post("https://home.mi.com/app/shopv3/pipe",params=data,headers=headers)
print(r.json())
#美化json格式
jsondata = json.dumps(r.json(), sort_keys=True, indent=4, separators=(',', ': '))#indent=4表示缩进4格
#解析产品数据列表
resultData = json.loads(jsondata)['result']['HomeList']['data']
#初始化一个空的set集合用于存放产品的详细地址
urls = ([])
#循环遍历将地址插入到地址集合:由于每个项目详细页面的地址都是http://home.mi.com/shop/detail?gid+上产品的编号，故这里只需要存入产品编号即可
for product in resultData:
    urls.append(product['gid'])

#遍历urls,抓取单个项目的详细信息
for gid in urls:
    # 获取产品的详细信息
    detailparm = "{\"detail\":{\"model\":\"Shopv2\",\"action\":\"getDetail\",\"parameters\":{\"gid\":\"+%s+\"}},\"comment\":{\"model\":\"Comment\",\"action\":\"getList\",\"parameters\":{\"goods_id\":\"+%s+\",\"orderby\":\"1\",\"pageindex\":\"0\",\"pagesize\":\"2\"}},\"activity\":{\"model\":\"Activity\",\"action\":\"getAct\",\"parameters\":{\"gid\":\"+%s+\"}}}" % (gid,gid,gid)
    detailreq = urllib.parse.quote(detailparm)
    detailreq = "data=" + detailreq
    detailresponse = requests.post("https://home.mi.com/app/shop/pipe", headers=headers, data=detailreq)

    # 美化json格式
    detailResultJsondata = json.dumps(detailresponse.json(), sort_keys=True, indent=4, separators=(',', ': '))  # indent=4表示缩进4格
    good = json.loads(detailResultJsondata)['result']['detail']['data']['good']
    print(good['gid']+"====="+good['name']+"======"+good['summary'])

"""
    总结;
        1、发送携带参数的post请求时，参数的命名关键字参数使用data
        2、json串的取值以及转换
        3、python的变量组合的时候要将变量放在后面，不能像Java一样将变量直接组合
        4、set数据类型的插入取值操作
        5、url编码：urllib.parse.quote和urllib.parse.urlencode
            urllib.parse.urlencode是将字典类型或者有两个元素的元祖用&符合连接起来，参数名以及参数值都不变
            urllib.parse.quote对请求参数进行编码
"""
