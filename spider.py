from selenium import webdriver
# from bs4 import BeautifulSoup
import os
import json
import time

import hashlib


# url 种子：40页内容
url_seeds = [
    'https://news.nwpu.edu.cn/gdyw/1585.htm',
    'https://news.nwpu.edu.cn/gdyw/1584.htm',
    'https://news.nwpu.edu.cn/gdyw/1583.htm',
    'https://news.nwpu.edu.cn/gdyw/1582.htm',
    'https://news.nwpu.edu.cn/gdyw/1581.htm',
    'https://news.nwpu.edu.cn/gdyw/1580.htm',
    'https://news.nwpu.edu.cn/gdyw/1579.htm',
    'https://news.nwpu.edu.cn/gdyw/1578.htm',
    'https://news.nwpu.edu.cn/gdyw/1577.htm',
    'https://news.nwpu.edu.cn/gdyw/1576.htm',
    'https://news.nwpu.edu.cn/gdyw/1575.htm',
    'https://news.nwpu.edu.cn/gdyw/1574.htm',
    'https://news.nwpu.edu.cn/gdyw/1573.htm',
    'https://news.nwpu.edu.cn/gdyw/1572.htm',
    'https://news.nwpu.edu.cn/gdyw/1571.htm',
    'https://news.nwpu.edu.cn/gdyw/1570.htm',
    'https://news.nwpu.edu.cn/gdyw/1569.htm',
    'https://news.nwpu.edu.cn/gdyw/1568.htm',
    'https://news.nwpu.edu.cn/gdyw/1567.htm',
    'https://news.nwpu.edu.cn/gdyw/1566.htm',
    # 'https://news.nwpu.edu.cn/gdyw/1565.htm',
    # 'https://news.nwpu.edu.cn/gdyw/1564.htm',
    # 'https://news.nwpu.edu.cn/gdyw/1563.htm',
    # 'https://news.nwpu.edu.cn/gdyw/1562.htm',
    # 'https://news.nwpu.edu.cn/gdyw/1561.htm',
    # 'https://news.nwpu.edu.cn/gdyw/1560.htm',
    # 'https://news.nwpu.edu.cn/gdyw/1559.htm',
    # 'https://news.nwpu.edu.cn/gdyw/1558.htm',
    # 'https://news.nwpu.edu.cn/gdyw/1557.htm',
    # 'https://news.nwpu.edu.cn/gdyw/1556.htm',
    # 'https://news.nwpu.edu.cn/gdyw/1555.htm',
    # 'https://news.nwpu.edu.cn/gdyw/1554.htm',
    # 'https://news.nwpu.edu.cn/gdyw/1553.htm',
    # 'https://news.nwpu.edu.cn/gdyw/1552.htm',
    # 'https://news.nwpu.edu.cn/gdyw/1551.htm',
    # 'https://news.nwpu.edu.cn/gdyw/1550.htm',
    # 'https://news.nwpu.edu.cn/gdyw/1559.htm',
    # 'https://news.nwpu.edu.cn/gdyw/1558.htm',
    # 'https://news.nwpu.edu.cn/gdyw/1557.htm',
    # 'https://news.nwpu.edu.cn/gdyw/1556.htm',
]

# 从url-seed中解析到的需要访问的url
urls = []

Dic = {}

# 模拟浏览器，使用谷歌浏览器，将chromedriver.exe复制到谷歌浏览器的文件夹内
chromedriver = r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
# 设置浏览器
os.environ["webdriver.chrome.driver"] = chromedriver

# 原始网页索引
pageIndex = [
    {'No': 0, 'offset':0, 'md5': None}
    ]
# url索引
urlIndex = []



# 初始化visited矩阵，记录哪些页面已经被爬过了
def init_dic():
    for i in range(100000):
        Dic[str(i)] = 0

    js = json.dumps(Dic)
    file = open('visited-set.json', 'w')
    file.write(js)
    file.close()

# 加载 visited矩阵
def load_dic():
    global Dic
    file = open('visited-set.json', 'r', encoding='UTF-8')
    js = file.read()
    Dic = json.loads(js)
    # print(Dic['0'])
    file.close()

# 保存 visited矩阵
def save_dic():
    # Dic['0'] = 1
    js = json.dumps(Dic)
    file = open('visited-set.json', 'w', encoding='UTF-8')
    
    file.write(js)
    file.close()

# 读取json文件到字典
def load_json(filename):
    file = open(filename, 'r', encoding='UTF-8')
    js = file.read()
    file.close()

    dic = json.loads(js)
    return dic

# 从字典到json
def save_json(data, filename):
    js = json.dumps(data)
    file = open(filename, 'w', encoding='UTF-8')
    file.write(js)
    file.close()


# 睡眠时间
def sleep(int):
    time.sleep(int)


# 检查当前网页是否已经爬取过了
def check_curent_visited(url):
    index = url.split('/')[-1]
    index = index.split('.')[0]
    # print(index)
    if Dic[str(index)] == 0:
        Dic[str(index)] = 1
        return True
    else:
        return False


# 保存到原始网页库
def save_raw_page(data, rawfile, url):
    # data.replace('\n', '')
    rawfile.write('\nversion: 1.0\n')
    
    rawfile.write('url: ' + url + '\n')
    
    rawfile.write('date: ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n')
    
    rawfile.write('length: ' + str(len(data)) + '\n\n')
    
    rawfile.write(str(data)) 
    # 当前文件指针所在位置
    # print(rawfile.tell())
    rawfile.write('\n')
    return rawfile.tell()

# 传入字符串，返回 hash值
def get_md5(data):
    # 应用MD5算法
    md5 = hashlib.md5()
    
    md5.update(data.encode('utf-8'))

    return md5.hexdigest()

# 原始网页索引列表添加新项
def append_pageIndex(data, cnt, index):
    data_md5 = get_md5(data)

    pageIndex[-1]['md5'] = data_md5
    #pageIndex[-1]['pagelen'] = len(data)
    pageIndex.append({'No': cnt, 'offset':index, 'md5': None})
    

# 原始网页url索引列表添加新项
def append_urlIndex(url, cnt):
    url_md5 = get_md5(url)
    urlIndex.append({'url':url_md5, 'No':cnt})

# 用于排序
def function(data):
    return data['url']

# 从种子中解析需要爬取的urls
def get_urls():
    browser = webdriver.Chrome(chromedriver)

    load_dic()

    for url_seed in url_seeds:
        browser.get(url_seed)

        for i in range(6):
            path = '//*[@id="line_u12_' + str(i) + '"]/div[2]/a'
            
            url = browser.find_element_by_xpath(path).get_attribute('href')
            # 如果未访问过，则加入url列表
            if(check_curent_visited(url)):
                urls.append(url)

    # 保存字典
    # save_dic()

    browser.close()
    
# 根据urls列表获取原始网页，保存到原始网页库；
# 生成网页索引文件和URL索引文件
def get_sourcepage():
    
    # 开启浏览器
    browser = webdriver.Chrome(chromedriver)
    
    
    ##### 需要修改写入模式， 正常应该是追加模式     后只考虑 一次性的， 从新写入
    rawfile = open("raw.txt", 'w+', encoding='UTF-8')
    # writefile = open("raw.txt", 'a+', encoding='UTF-8')


    # 开始获取原始网页
    # 文档编号 cnt
    cnt = 0
    for url in urls:
        browser.get(url)
        
        print('%d:' % cnt + url)
        cnt = cnt + 1


        # 保存原始网页 到 网页库
        raw_page_offset = save_raw_page(browser.page_source, rawfile, url)

        # 网页索引文件
        append_pageIndex(browser.page_source, cnt, raw_page_offset)
        # url索引文件
        append_urlIndex(url, cnt - 1)



    

    # 根据url的hash值排序
    urlIndex.sort(key=function)
    # 保存网页索引文件和url索引文件
    save_json(pageIndex, 'pageIndex.json')
    save_json(urlIndex, 'urlIndex.json')
    # 关闭文件和浏览器
    rawfile.close()
    browser.close()



if __name__ == '__main__':
    #init_dic()
    #save_dic()
    
    get_urls()
    
    get_sourcepage()

