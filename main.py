import datetime
import json

from cpcb_station_data import get_site_list, CpcbParam
from payload import Payload
import requests


# from_date = input('enter the from date')
# to_date = input('enter the to date')


def get_data():
    stations_list = get_site_list()
    for station in stations_list:
        for k, v in station.items():
            payload = Payload(state=v[CpcbParam.STATE_NAME], city=v[CpcbParam.CITY_NAME], site_id=k,
                              start_date=date, end_date=date).generate()
            response = requests.post('https://app.cpcbccr.com/caaqms/fetch_table_data',
                                     data=payload, headers=headers)
            print(response.json())


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
date = datetime.datetime.now()
