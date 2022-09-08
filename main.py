import datetime
import time

import pandas
from cpcb_station_data import get_site_list, CpcbParam
from payload import Payload
import requests
from model.cpcb_response_data import ParseData


def get_data():
    pd: pandas.DataFrame = pandas.DataFrame()
    stations_list = get_site_list()
    for station in stations_list:
        for k, v in station.items():
            payload = Payload(state=v[CpcbParam.STATE_NAME], city=v[CpcbParam.CITY_NAME], site_id=k,
                              start_date=from_date, end_date=to_date).generate()
            response = requests.post('https://app.cpcbccr.com/caaqms/fetch_table_data',
                                     data=payload, headers=headers)
            pd = pandas.concat([pd, pandas.DataFrame.from_dict(ParseData(response.json()).get())], axis=0,
                               ignore_index=True)
        pd.to_csv('cpcb-data.csv')
        time.sleep(1)


headers = {
    'authority': 'app.cpcbccr.com',
    'method': 'POST',
    'path': '/caaqms/fetch_table_data',
    'scheme': 'https',
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US, en;q = 0.9',
    'content-length': '696',
    'content-type': 'text/plain',
    'origin': 'https://app.cpcbccr.com',
    'referer': 'https://app.cpcbccr.com/ccr/',
    'sec-ch-ua': '"Chromium";v = "104", " Not A;Brand";v = "99", "Google Chrome";v = "104"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': "Windows",
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0;Win64;x64) AppleWebKit/537.36 (KHTML, likeGe cko) Chrome/'
                    '104.0.0.0Safari/537.36 '

}
to_date = datetime.datetime.now()
from_date = datetime.datetime(year=to_date.year, month=to_date.month, day=to_date.day-1, hour=00, minute=00, second=00)
get_data()
