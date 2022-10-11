import threading

from fastapi import FastAPI, Body, WebSocket
from pydantic import BaseModel
import datetime
from main import Data_download
import time

app = FastAPI()

class Post(BaseModel):
    fdate: datetime.datetime
    tdate: datetime.datetime

Running = {}
Waiting = []



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

                    Waiting.append(Dd)
                    return res   
            else:
                return 'ERROR: from date should come before to date'
        except ValueError as err:
            return 'ERROR: entered date format is not right '+ err
    else:
        return 'ERROR: required arguments missing'



def Scheduling():
    while True:
        #print(f" OUTSIDE: len(running) = {len(Running)} len(Waiting) = {len(Waiting)}")
        while len(Running) < 10 and len(Waiting)>0:
            temp = Waiting.pop(0)
            Running[temp.id] = temp

            print(f" len(running) = {len(Running)} len(Waiting) = {len(Waiting)}")
            print(f"The thread {temp.thread_id} is start running")

            temp.thread.start()

        for k , v in list(Running.items()):
            print(f"{v.thread_id} progress = {v.progress}%")
            if v.progress >= 100:
                print(f"The thread {temp.thread_id} is done executing")
                Running.pop(k)
        time.sleep(3)

Sche = threading.Thread(target=Scheduling, args=())
Sche.start()

