import datetime
import requests
from bs4 import BeautifulSoup


# https://www.learncodewithmike.com/2020/02/python-beautifulsoup-web-scraper.html
def crawl_stock_info(stockCodes, isAddName=True):
    result = []

    for code in stockCodes:
        response = requests.get(f'https://invest.cnyes.com/twstock/TWS/{code}')
        soup = BeautifulSoup(response.text, "html.parser")
        price = soup.select_one('.info-lp').getText()
        changePrice = soup.select_one('.change-net').getText()
        changepercent = soup.select_one('.change-percent').getText()
        name = soup.select_one('.header_second').getText()
        if isAddName:
            result.append(
                f'{code} {name}: {price}  {changePrice}  {changepercent}')
        else:
            result.append(
                f'{code}: {price}  {changePrice}  {changepercent}')

    return ',\n'.join(result)


def crawl_exchage_rate():
    now = datetime.datetime.now()
    year = str(now.year)
    month = '{:02d}'.format(now.month)

    response = requests.post(
        f'https://portal.sw.nat.gov.tw/APGQO/GC331!query?formBean.year={year}&formBean.mon={month}').json()

    cny_list = [x for x in response['data'] if x['CRRN_CD'] in {'CNY', 'USD'}]

    result = []
    for info in cny_list:
        day = None
        if info['TEN_DAY'] == '1':
            day = '1-10'
        elif info['TEN_DAY'] == '2':
            day = '11-20'
        elif info['TEN_DAY'] == '3':
            day = '21-31'

        result.append(
            f"{info['CRRN_CD']} {info['YEAR']}/{info['MON']} {day}=> {info['IN_RATE']}")

    return ',\n'.join(result)
