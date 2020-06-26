import spider
import process
import re
from bs4 import BeautifulSoup


max_page_list = 15
abstract_ahead_offset = 40
abstract_len = 200
pageIndexs = []

def get_abstract(data, offset):
    if(offset > abstract_ahead_offset):
        offset -= abstract_ahead_offset
    else:
        offset = 0
    return data[offset : offset + abstract_len]


def general_pageinfo(page):
    no = page[0]
    # time = page[1]
    pos = page[2:]

    raw_offset = pageIndexs[no]['offset']

    rawfile = open('raw.txt', 'r', encoding='UTF-8')
    url, data = process.read_raw_info(rawfile, raw_offset)

    soup = BeautifulSoup(data, 'html.parser')
    title = soup.find("title")

    data_list = re.findall('[\u4e00-\u9fa5]', data)

    data_str = "".join(data_list)
    abstract = get_abstract(data_str, pos[0])
    
    rawfile.close()
    return title.text, url, abstract

# 打印 结果
def print_result(results):
    for result in results:
        print('标题：' + result[0])
        print('摘要：' + result[2])
        print('url：' + result[1])
        print('\n')
    pass

if __name__ == '__main__':
    search_str = input('请输入查询词：')
    invert_dic = spider.load_json("invert.json")
    pageIndexs = spider.load_json('pageIndex.json')
    # 要显示的列表
    page_info_list = []

    if search_str in invert_dic:
        page_invert_list = invert_dic[search_str]
        if max_page_list < len(page_invert_list):
            page_invert_list = page_invert_list[0:max_page_list]

        for page in page_invert_list:
            page_info_list.append(general_pageinfo(page))

        print_result(page_info_list)

    else:
        print('暂未找到相关词汇')

    