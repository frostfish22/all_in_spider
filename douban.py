import sys
import time
import urllib
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

#代理
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
}

def book_spider(book_tag,page_num=0):
    book_list = []
    try_times = 0

    url = 'http://book.douban.com/tag/'+str(book_tag)+'?start='+str(page_num*20)
    time.sleep(np.random.rand()*5)

    try:
        response = requests.get(url, headers=headers)
    except:
        print('Oops! Error!')

    soup = BeautifulSoup(response.text, 'html.parser')
    list_soup = soup.find_all('li',{'class':'subject-item'})
    for book_div in list_soup:
        book_name = book_div.find('h2').find('a').get_text().strip().replace(' ','').replace('\n','')

        '''
            @TODO
            1. 这里缺少对作者、出版社、出版日期、豆瓣评分的精确提取
            2. 这里容易出现一个问题，有的书数据不全，而且没有评分，就会导致提取的时候出现报错（越位情况）
        '''
        try:
            book_author = book_div.find('div',{'class':'pub'}).get_text().split('/')[0].strip()
            book_press = book_div.find('div',{'class':'pub'}).get_text().split('/')[1].strip()
            book_date = book_div.find('div',{'class':'pub'}).get_text().split('/')[2].strip()
            book_score = book_div.find('span',{'class':'rating_nums'}).get_text().strip()
        except:
            continue
        # book_price = book_div.find('div',{'class':'price'}).get_text().strip()
        book_list.append([
            book_name,
            book_author,
            book_press,
            book_date,
            book_score
            ])
    # 把结果转换为DataFrame
    book_df = pd.DataFrame(book_list, columns=['书名', '作者', '出版社', '出版日期', '豆瓣评分'])
    print(book_df)


if __name__ == "__main__":
    book_spider('python',1)