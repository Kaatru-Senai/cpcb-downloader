import datetime
import os.path
import time
import argparse
import pandas
from cpcb_station_raw_data_parser import get_site_list, CpcbParam
from payload import Payload
import requests
from requests.exceptions import Timeout
from model.response_data import ParseData


def start_process():
    if os.path.exists('cpcb-data.csv'):
        pd: pandas.DataFrame = pandas.read_csv('cpcb-data.csv')
    else:
        pd: pandas.DataFrame = pandas.DataFrame()
    stations_list = get_site_list()
    for station in stations_list:
        for k, v in station.items():
            pd = pandas.concat([pd, pandas.DataFrame.from_dict(get_cpcb_data(k, v))], axis=0,
                               ignore_index=True)
        pd.to_csv('cpcb-data.csv', index=False)
        print(len(pd))
        time.sleep(1)


def get_cpcb_data(site_id: str, site_meta_data: dict):
    global retry_sleep_time
    payload = Payload(state=site_meta_data[CpcbParam.STATE_NAME], city=site_meta_data[CpcbParam.CITY_NAME],
                      site_id=site_id, start_date=from_date, end_date=to_date).generate()
    try:
        response = requests.post('https://app.cpcbccr.com/caaqms/fetch_table_data',
                                 data=payload, headers=headers, timeout=10)
        retry_sleep_time = 0
        try:
            return ParseData(response.json(), site_meta_data).get()
        except ValueError:
            print(site_id)
            print(response.text)
    except Timeout:
        retry_sleep_time += 3
        time.sleep(retry_sleep_time)


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
retry_sleep_time = 0
parser = argparse.ArgumentParser()
parser.add_argument(
    '-fd', help='enter the from datetime in following format dd-mm-yyyy hh:mm (use 24H)')
parser.add_argument(
    '-td', help='enter the to datetime in following format dd-mm-yyyy hh:mm (use 24H)')
args = parser.parse_args()
if args.fd or args.td:
    try:
        from_date = datetime.datetime.strptime(args.fd, '%d-%m-%Y %H:%M')
        to_date = datetime.datetime.strptime(args.td, '%d-%m-%Y %H:%M')
        if from_date < to_date:
            if to_date > datetime.datetime.now():
                print('ERROR: to datetime should not exceed present datetime')
            else:
                print('Fetching data')
                start_process()
        else:
            print('ERROR: from date should come before to date')
    except ValueError as err:
        print('ERROR: entered date format is not right')
else:
    print('ERROR: required arguments missing')
