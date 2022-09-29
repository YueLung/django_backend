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
        nameDict = {'2330': '台積', '1584': '精剛', '2345': '智邦',
                    '2377': '微星', '00642U': '石油', '00635U': '黃金'}

        if isAddName:
            result.append(
                f'{code} {nameDict[code]}: \n {price}  {changePrice}  {changepercent}\n --------------------------')
        else:
            result.append(
                f'{code}: \n {price}  {changePrice}  {changepercent}\n --------------------------')

    return ',\n'.join(result)


def crawl_exchage_rate(currency):
    response = requests.get('https://portal.sw.nat.gov.tw/APGQO/GC331')
    soup = BeautifulSoup(response.text, "html.parser")
    yearSelected = soup.select_one('#yearList').find(
        attrs={"selected": "selected"}).getText()
    monthSelected = soup.select_one('#monList').find(
        attrs={"selected": "selected"}).getText()
    tenDaySelected = soup.select_one('#tenDayList').find(
        attrs={"selected": "selected"})['value']
    # print(yearSelected, monthSelected, tenDaySelected)

    req_url = 'https://portal.sw.nat.gov.tw/APGQO/GC331!query?formBean.year={}&formBean.mon={}&formBean.tenDay={}'

    response = requests.post(req_url.format(
        yearSelected, monthSelected, tenDaySelected)).json()
    cny_list = [x for x in response['data'] if x['CRRN_CD'] in currency]

    now = datetime.datetime.now()
    now_day = now.day
    ten_day = None
    if now_day < 11:
        ten_day = '1'
    elif now_day < 21:
        ten_day = '2'
    elif now_day < 32:
        ten_day = '3'

    if ten_day != tenDaySelected:
        year = str(now.year)
        month = '{:02d}'.format(now.month)
        response2 = requests.post(req_url.format(year, month, ten_day)).json()
        cny_list2 = [x for x in response2['data'] if x['CRRN_CD'] in currency]
        cny_list.extend(cny_list2)

    cny_list.sort(reverse=True, key=lambda x: x['UP_DATE'])
    cny_list.sort(key=lambda x: x['CRRN_CD'])

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
