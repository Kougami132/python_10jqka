import httpx, time
from lxml import etree
from database import DataBase

class Spider:
    def __init__(self):
        self.db = DataBase()
    
    def query(self):
        cur = 1
        while True:
            url = f'http://q.10jqka.com.cn/index/index/board/all/field/zdf/order/desc/page/{cur}'
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.37"
            }
            html = httpx.get(url=url, headers=headers, timeout=10)
            table = etree.HTML(html.text)
            id = table.xpath('//*[@id="maincont"]/table/tbody/tr/td[1]/text()')
            code = table.xpath('//*[@id="maincont"]/table/tbody/tr/td[2]/a/text()')
            name = table.xpath('//*[@id="maincont"]/table/tbody/tr/td[3]/a/text()')
            value = table.xpath('//*[@id="maincont"]/table/tbody/tr/td[4]/text()')
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
        print(f'[{time.strftime("%H:%M:%S")}] 数据爬取完毕, 等待一分钟')

def check(timestamp):
    timestamp %= 60 * 60 * 24
    timestamp //= 60
    if timestamp % 5 != 0:
        return False
    elif timestamp >= 90 and timestamp <= 210:        # 9:30 —— 11:30
        return True
    elif timestamp >= 300 and timestamp <= 420:     # 13:00 —— 15:00
        return True
    else:
        return False

if __name__ == '__main__':
    spd = Spider()
    while True:
        now = int(time.time())
        if (check(now)):
            print(f'[{time.strftime("%H:%M:%S")}] 定时器: 开始爬取数据')
            spd.query()
            time.sleep(60)
        else:
            print(f'[{time.strftime("%H:%M:%S")}] 定时器: 等待中, 开始时间: 9:30 —— 11:30 , 13:00 —— 15:00')
            time.sleep(1)