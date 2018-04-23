import requests
from bs4 import BeautifulSoup
from lxml import etree
from requests import RequestException
def get():
    #requests的Session可以自动保持cookie,不需要自己维护cookie内容
    page = 1
    S = requests.Session()
    target_url = 'http://www.xicidaili.com/nn/%d' % page
    target_headers = {'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer':'http://www.xicidaili.com/nn/',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'zh-CN,zh;q=0.8',
    }
    target_response = S.get(url = target_url, headers = target_headers)
    target_response.encoding = 'utf-8'
    target_html = target_response.text
    bf1_ip_list = BeautifulSoup(target_html, 'lxml')
    bf2_ip_list = BeautifulSoup(str(bf1_ip_list.find_all(id = 'ip_list')), 'lxml')
    ip_list_info = bf2_ip_list.table.contents

    proxys_list = []
    for index in range(len(ip_list_info)):
        if index % 2 == 1 and index != 1:
            dom = etree.HTML(str(ip_list_info[index]))
            ip = dom.xpath('//td[2]')
            port = dom.xpath('//td[3]')
            protocol = dom.xpath('//td[6]')
            proxys_list.append(#protocol[0].text.lower() + '#' + #
                    ip[0].text + ':' + port[0].text)
    print(proxys_list)
    return proxys_list

def print_ip(proxies):
    """利用http://www.whatismyip.com.tw/显示访问的ip"""
    cookies = {
        'sc_is_visitor_unique': 'rx6392240.1508897278.298AFF0AE2624F7BC72BADF517B67AEE.2.2.2.2.2.2.1.1.1',
    }

    headers = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
    }
    url = 'http://www.whatismyip.com.tw/'
    try:
        page = requests.get(url, headers=headers, cookies=cookies, proxies=proxies)
    except RequestException as e:
        print(str(proxies) + 'is wrong')
    else:
        soup = BeautifulSoup(page.text, 'lxml')
        my_ip = soup.find('b').text
        print('成功连接' + my_ip)
        
def get_proxy(aip):
    """构建格式化的单个proxies"""
    proxy_ip = 'http://' + aip
    proxy_ips = 'https://' + aip
    proxy = {'http': proxy_ip, 'https': proxy_ips}
    return proxy

def main():
    proxys_list=get()
    headers = {
        #'cookies': cookies,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'
    }
    url = 'http://www.whatismyip.com.tw/'
    #
    for aip in  proxys_list:
        proxy = get_proxy(aip)
        print_ip(proxy)
    #proxies = {'https': 'https://122.72.18.60:8620',}


if __name__ == '__main__':
	main()