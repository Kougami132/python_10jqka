import httpx, time, execjs
from lxml import etree
from database import DataBase

class Spider:
    def __init__(self):
        self.db = DataBase()
    
    def query(self):
        cur = 1
        # 获取反爬Cookie
        f = open('demo.js', encoding='utf-8').read()
        def get_headers():
            print(f'[{time.strftime("%H:%M:%S")}] 正在计算反爬Cookie')
            v = execjs.compile(f).call('generate_cookie')
            return {
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
                        "application/signed-exchange;v=b3;q=0.9",
                        "Accept-Encoding": "gzip, deflate",
                        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6",
                        "Cache-Control": "max-age=0",
                        "Connection": "keep-alive",
                        "Cookie": "v={}".format(v),
                        "Host": "q.10jqka.com.cn",
                        "Upgrade-Insecure-Requests": "1",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.37"
                    }
        headers = get_headers()
        while True:
            url = f'http://q.10jqka.com.cn/index/index/board/all/field/zdf/order/desc/page/{cur}/ajax/1/'
            html = httpx.get(url=url, headers=headers, timeout=10)
            # Cookie过期重新计算
            while html.status_code != 200:
                print(f'[{time.strftime("%H:%M:%S")}] Cookie失效')
                headers = get_headers()
                print(f'[{time.strftime("%H:%M:%S")}] Cookie计算完成')
                html = httpx.get(url=url, headers=headers, timeout=10)
            table = etree.HTML(html.text)
            id = table.xpath('/html/body/table/tbody/tr/td[1]/text()')
            code = table.xpath('/html/body/table/tbody/tr/td[2]/a/text()')
            name = table.xpath('/html/body/table/tbody/tr/td[3]/a/text()')
            value = table.xpath('/html/body/table/tbody/tr/td[4]/text()')
            # 将无效数据数值改为0
            for i in range(len(value)):
                if value[i] == '--':
                    value[i] = 0
            self.db.save(id, code, name, value, int(time.time()))

            page_info = table.xpath('//*[@id="m-page"]/span/text()')[0].split('/')
            cur = int(page_info[0])
            total = int(page_info[1])
            print(f'[{time.strftime("%H:%M:%S")}] 爬取进度: {cur}/{total}')
            
            if cur == total:
                break

            cur += 1
        print(f'[{time.strftime("%H:%M:%S")}] 数据爬取完毕')

def check(second):
    if second % 5 != 0:
        return False
    if second >= 90 & second <= 210:        # 9:30 —— 11:30
        return True
    elif second >= 300 & second <= 420:     # 13:00 —— 15:00
        return True
    else:
        return False

if __name__ == '__main__':
    spd = Spider()
    while True:
        now = int(time.time())
        now %= 60 * 60 * 24
        now //= 60
        if (check(now)):
            print(f'[{time.strftime("%H:%M:%S")}] 定时器: 开始爬取数据')
            spd.query()
        else:
            print(f'[{time.strftime("%H:%M:%S")}] 定时器: 等待中, 开始时间: 9:30 —— 11:30 , 13:00 —— 15:00')
            time.sleep(1)