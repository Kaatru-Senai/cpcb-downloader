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
            print(f"The thread {temp.id} is start running")

            temp.thread.start()

        for k , v in list(Running.items()):
            print(f"{v.id} progress = {v.progress}%")
            if v.progress >= 100:
                print(f"The thread {temp.id} is done executing")
                Running.pop(k)
        time.sleep(3)

Sche = threading.Thread(target=Scheduling, args=())
Sche.start()



def Find_obj(process_id):
    if len(Running) >0 or len(Waiting) > 0:
        print("inside loop")

        for k,v in list(Running.items()):
            print(f'key: {k} value: {v} v.id = {v.id} process_id: {process_id} type: {type(process_id)}')
            if str(v.id) == process_id:
                return v
        for v in Waiting:
            if str(v.id) == process_id:
                return v
    else:
        print('No Items found')
        return None
def my_func(process_id):
    
    obj = Find_obj(process_id)
    if obj:
        data = {
            "process_id": process_id,
            "Progress": f'{obj.progress}%',
            "estimated time": f'{str(obj.estimated_time())} miliseconds'
        }
        return data
    print("couldn't find anything")



@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, process_id: str):
    await websocket.accept()
    print(process_id)
    while True:
        # data = await websocket.receive_text()
        obj = {
            "Default": "Value"
        }
        try:
            obj = my_func(process_id)
        except Exception as e:
            print(e)
        # print(Obj)
        await websocket.send_json(obj)
        time.sleep(5)
