from ast import arg
import datetime
from email.policy import default
import os.path
import time
import pandas
from cpcb_station_raw_data_parser import get_site_list, CpcbParam
from payload import Payload
import requests
from requests.exceptions import Timeout
from model.response_data import ParseData
import threading

from fastapi import FastAPI, Body, WebSocket
from pydantic import BaseModel
import uuid
from fastapi.responses import HTMLResponse


app = FastAPI()

class Post(BaseModel):
    fdate: datetime.datetime
    tdate: datetime.datetime

class Data_download:
    def __init__(self, f_date, t_date) -> None:
        self.from_date = f_date
        self.to_date = t_date
        self.id = uuid.uuid1()
        self.progress = 0
        self.thread = threading.Thread(target=self.start_process, args=())
        self.thread_id = self.thread.getName()

    def start_process(self):
        if os.path.exists('cpcb-data.csv'):
            pd: pandas.DataFrame = pandas.read_csv('cpcb-data.csv')
        else:
            pd: pandas.DataFrame = pandas.DataFrame()

        i = 0
        stations_list = get_site_list()
        for station in stations_list:
            for k, v in station.items():
                pd = pandas.concat([pd, pandas.DataFrame.from_dict(self.get_cpcb_data(k, v))], axis=0,
                                ignore_index=True)
            pd.to_csv('cpcb-data.csv', index=False)

            i+=1
            self.progress = int((i/len(stations_list))*100)
            if i == len(stations_list):
                self.progress = 100

            print(len(pd))
            time.sleep(1)

    def get_cpcb_data(self, site_id: str, site_meta_data: dict):
        global retry_sleep_time
        payload = Payload(state=site_meta_data[CpcbParam.STATE_NAME], city=site_meta_data[CpcbParam.CITY_NAME],
                        site_id=site_id, start_date=self.from_date, end_date=self.to_date).generate()
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



@app.post("/query")
async def get_date(data: Post):

    f_date = data.fdate
    t_date = data.tdate

    if f_date or t_date:
        try:
            x = f_date.strftime("%d-%m-%y %H:%M")
            y = t_date.strftime("%d-%m-%y %H:%M")
            print(x, type(x), y, type(y))
            
            from_date = datetime.datetime.strptime(x, '%d-%m-%y %H:%M')
            to_date = datetime.datetime.strptime(y, '%d-%m-%y %H:%M')

            print(type(from_date), type( to_date))

            if from_date < to_date:
                if to_date > datetime.datetime.now():
                    return 'ERROR: to datetime should not exceed present datetime'
                else:
                    print('Fetching data')
                    Dd: Data_download = Data_download(from_date, to_date)
                    res = {}
                    res['Status'] = "process created"
                    res['id'] = Dd.id
                    res['thread_id'] = Dd.thread_id

                    Dd.thread.start()
                    

                    return res

                    
            else:
                return 'ERROR: from date should come before to date'
        except ValueError as err:
            return 'ERROR: entered date format is not right '+ err
    else:
        return 'ERROR: required arguments missing'
