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
import server
from utility import util


class Downloader:
    def __init__(self, f_date, t_date, user_mail) -> None:
        self.from_date = f_date
        self.to_date = t_date
        self.id = uuid.uuid1()
        self.progress = 0
        self.thread = threading.Thread(target=self.start_process, args=())
        self.thread_id = self.thread.getName()
        self.selftime = None
        self.et = 0
        self.email = "custom email" #demo
        self.reciver_mail = user_mail
        self.password = "password"#demo

    def start_process(self):
        if not os.path.isdir('./Downloaded_csv'):
            os.mkdir('Downloaded_csv')
        if os.path.exists(f'./Downloaded_csv/{self.id}.csv'):
            pd: pandas.DataFrame = pandas.read_csv(f'./Downloaded_csv/{self.id}.csv')
        else:
            pd: pandas.DataFrame = pandas.DataFrame()


        i = 0
        loop_time= 0

        stations_list = get_site_list()
        for station in stations_list:
            

           
            st = datetime.datetime.now()

            for k, v in station.items():
                pd = pandas.concat([pd, pandas.DataFrame.from_dict(self.get_cpcb_data(k, v))], axis=0,
                                ignore_index=True)
                
                # # pd = pandas.concat([pd, df1], axis=1)#Only for testing
                # time.sleep(2)

            pd.to_csv(f'./Downloaded_csv/{self.id}.csv', index=False)

        


            if not i:   #only for the first iteration it'll compute the loop time
                loop_time = datetime.datetime.now() - st
                self.selftime = (loop_time.seconds*len(stations_list))
            
            self.et = self.selftime - (i+1)*(loop_time.seconds) #it'll compute total time remain to be executed completly

            print('Estimated time',self.et)
            i+=1

            self.progress = int((i/len(stations_list))*100)#testing code remove 17 for deployment
            
            if i >= len(stations_list):
                self.progress = 100
                #testing code line
            if self.progress >= 100:
                print("End of a loop")
                break

            print(i)
            # print(len(pd))
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
                return ParseData(response.text, site_meta_data).get()
            except ValueError:
                print(site_id)
                print(response.text)
        except Timeout:
            retry_sleep_time += 3 
            time.sleep(retry_sleep_time)


    def estimated_time(self):
        Ut:util = util()
        return Ut.ET(self.id, self.et)



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

