import requests
from bs4 import BeautifulSoup
import re
import json
import execjs  # 导入 execjs

# 获取用户输入
name = input("请输入要搜索的名称: ")

cookies = {
    '_ga': 'GA1.1.501277304.1733721213',
    '_ga_60FB8R25EJ': 'GS1.1.1733721213.1.1.1733721341.0.0.0',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9',
    # 'cookie': '_ga=GA1.1.501277304.1733721213; _ga_60FB8R25EJ=GS1.1.1733721213.1.1.1733721341.0.0.0',
    'priority': 'u=0, i',
    'referer': 'https://cilijia.net/search',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
}

page = 1
data_total = 0
total_page = 1
total_data_list = []

def get_search_page(page):
    params = {
        'q': name,
        'p': page,
    }
    response = requests.get('https://cilijia.net/search', params=params, cookies=cookies, headers=headers)
    print(response.text)
    
    
def get_search_data():
    params = {
        'q': name,
    }
    response = requests.get('https://cilijia.net/search', params=params, cookies=cookies, headers=headers)
    html_content = response.text
    html_text = BeautifulSoup(html_content, 'html.parser')
    
    total_meta = html_text.find('p', class_='total-meta')
    if total_meta:
        numbers = re.findall(r'\d+', total_meta.get_text())
        data_total = int(numbers[0]) if numbers else 0
        total_page = data_total // 10 + (1 if data_total % 10 > 0 else 0)
    else:
        print("没有找到class为total-meta的标签")
    
    script_tags = html_text.find_all('script')
    if script_tags:
        for index, script in enumerate(script_tags):
            script_content = script.string
            if script_content:
                if 'window.__NUXT__' in script_content:
                    print(script_content)
                    # function_body = script_content.split('=')[1]
                    # context = execjs.compile(function_body)
                    # result = context.call("getData") 
                    # print(result)
    else:
        print("没有找到任何script标签")

get_search_data()

# print(total_data_list)
