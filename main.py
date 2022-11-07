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
from configparser import ConfigParser
import uuid
file = 'configfile.ini'
config = ConfigParser()
config.read(file)

dev_mode = int(config['dev mode']['dev']) 


 

from utility import ET


class Downloader:
    """Takes from_date and to_date and download data from cpcb station save as csv file"""
    def __init__(self, f_date, t_date) -> None:
        self.from_date = f_date
        self.to_date = t_date
        self.id = uuid.uuid1()
        self.progress = 0
        self.thread = threading.Thread(target=self.start_process, args=())
        self.thread_id = self.thread.getName()
        self.selftime = None
        self.et = 0


    def start_process(self):
        """
        This function responsible for calling get_cpcb_data and download save the file, file name is the unique id generated uuid module
        """
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
            
            st = datetime.datetime.now() #time coputation
            if not dev_mode:
                for k, v in station.items():
                    pd = pandas.concat([pd, pandas.DataFrame.from_dict(self.get_cpcb_data(k, v))], axis=0,
                                    ignore_index=True)
                                    
            pd.to_csv(f'./Downloaded_csv/{self.id}.csv', index=False)

        
            time.sleep(1) #Necessary


            if i == 0:   #only for the first iteration it'll compute the loop time
                loop_time = datetime.datetime.now() - st
                total_time = loop_time*len(stations_list)
                self.selftime = total_time.seconds

            temp = (i+1)*loop_time
            self.et = self.selftime - temp.seconds #it'll compute total time remain to be executed completly
            
            i+=1

            self.progress = int((i/len(stations_list))*100)#testing code remove 17 for deployment
            
            if i >= len(stations_list):
                self.progress = 100
                self.et = 0
                

            print(i)
            # print(len(pd))
            

    def get_cpcb_data(self, site_id: str, site_meta_data: dict):
        """This function request to the cpcb api and get the data as json format"""
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
        """Get the estimated time it takes to complete this process. by calling ET() function from util class in utility.py module"""
        
        return ET(self.id, self.et)



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
                    '104.0.0.0Safari/537.36 ',
    "Cookie": "ccr_captcha='0DizAPld0WUvGLNv9wn6QQ3S7fMoEZb1QAefutoonhGZLbv/tTrvK93Q05pfTpB3VNbccYD6I7L0EWhm1idfHiKb51S16z06U1h0TwFZhXGg0H7VtQWngRoHkj/cgi9XdRpWr9X3ADIQ/YWItf3iMZUPLotk2cFjo2VTcKkeu1D/qfkkWOvmReDE3BjitKMpG0z5Wjy3bJnxAc51UDAKUI8nY3x/64D+PhtT7FRbMSuzKCKoOGSdVGQ4dO2huMr4jTVn01zUBi0bM2jHn8rhvw=='; ccr_public='VK9JSEjffBIzb5eC+ygZSgaMAgoic2aiofN659ZrAhSTdHmO9GVKyvfg7dDU1R/49f9gUmuqel525bgsWbvHYX61w43GDbGs8rv4s5ML2MntseeqXNuS9K5Hg7JLqCYkcay/Z25qu6rzpQ8ri7OSWD9rwSxY89DCRvtRaZDfvXf4cTJDculbB5U0fLQ2qlsUBRMDtFIfJpNobaqFOAfMjOJPc7nYLJhopOS3HcLeBtJdu+WHdnOi6gwc2HE4zTxaBzMxzPwupM+Dmf7QcCg4LMAeTK9bfIe7oQ3e7drPpl/rm1XLHlvl62XQ2v/xa9GQ18aDsZlGu3XNetsdg6leSkFVnqAd7iXOoM85w7DhAMWcQRmvCU/4CKBKfLu1vOvI4EVGaI52mhvDwZtT+cyCkQ=='"
  
  }
retry_sleep_time = 0

