'''
@Author: your name
@Date: 2020-06-24 00:12:12
@LastEditTime: 2020-06-26 20:47:40
@LastEditors: your name
@Description: In User Settings Edit
@FilePath: \SimpleSearchEngine\process.py
'''
import spider
import jieba
import re


invert_dic = {}

# 将一篇文档的所有token加入倒排文件
def insert_invertion(token, id):

    for tk in token:
        if tk[0] in invert_dic:
            # 当前词在字典已经出现过
            # print(invert_dic[tk[0]])
            if id == invert_dic[tk[0]][-1][0]:
                invert_dic[tk[0]][-1][1] += 1
                invert_dic[tk[0]][-1].append(tk[1])
            else:
                invert_dic[tk[0]].append([id, 1, tk[1]])

        else:
            invert_dic[tk[0]] = []
            invert_dic[tk[0]].append([id, 1, tk[1]])

def sort_function(data):
    return data[1]
    

def read_raw_info(file, offset):
    file.seek(offset)
    file.readline()
    file.readline()
    url = file.readline()[5:-1]
    file.readline()
    len = int(file.readline()[8:-1])
    file.readline()
    
    data = file.read(len)

    return url, data


if __name__ == "__main__":
    rawfile = open("raw.txt", 'r', encoding='UTF-8')

    # url, data = read_raw_info(rawfile, 0)

    pageIndexs = spider.load_json('pageIndex.json')
    # 逐步处理所有文档
    cnt = 0
    for pageIndex in pageIndexs:
        if None == pageIndex['md5']:
            break
        else:
            url, data = read_raw_info(rawfile, pageIndex['offset'])
            #data = data.decode('utf-8')
            data_list = re.findall('[\u4e00-\u9fa5]', data)

            data_str = "".join(data_list)

            token = jieba.tokenize(data_str, mode='search')

            insert_invertion(token, cnt)
            cnt += 1
            
    # 倒排文件按照词频排序
    for d in invert_dic:
        invert_dic[d].sort(key=sort_function, reverse = True)

    # 保存倒排文件
    spider.save_json(invert_dic, "invert.json")
    
    #aaaa = spider.load_json("invert.json")
    #print(len(aaaa))
    

