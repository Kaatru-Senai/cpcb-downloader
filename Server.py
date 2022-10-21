import asyncio
from concurrent.futures import thread
import email
from hashlib import new
import threading
import os
from fastapi import FastAPI, Body, WebSocket
from pydantic import BaseModel
import datetime
from main import Downloader
import time
from fastapi.responses import StreamingResponse
import io
import pandas as pd

from utility import util, clear_directory,send_email


util_instance: util = util()

app = FastAPI()

class Post(BaseModel):
    fdate: datetime.datetime
    tdate: datetime.datetime
    mail: str
    

Running = {}
Waiting = []


def query_helper_func(f_date, t_date, mail):
    
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
                    Dd: Downloader = Downloader(from_date, to_date,"hello")
                    res = {}
                    res['Status'] = "process created"
                    res['id'] = Dd.id
                    

                    Waiting.append(Dd)
                    threading.Thread(target=send_email, args=(mail, Dd.id)).start()
                    
                    return res   
            else:
                return 'ERROR: from date should come before to date'
        except ValueError as err:
            return 'ERROR: entered date format is not right '+ err
    else:
        return 'ERROR: required arguments missing'


@app.post("/query")
async def get_date(data: Post):
    f_date = data.fdate
    t_date = data.tdate
    email = data.mail
    
    res = query_helper_func(f_date, t_date, email)
    return res






Sche = threading.Thread(target=util_instance.schedule, args=())
Sche.start()


delete_file = threading.Thread(target=clear_directory, args=())
delete_file.start()



@app.get("/get_csv")
async def get_csv(id: str):
    print(id)

    if os.path.exists(f'./Downloaded_csv/{id}.csv'):

        df = pd.read_csv(f'./Downloaded_csv/{id}.csv')

        stream = io.StringIO()

        df.to_csv(stream, index = False)

        response = StreamingResponse(iter([stream.getvalue()]),
                            media_type="text/csv"
        )

        response.headers["Content-Disposition"] = f"attachment; filename={id}.csv"

        return response

    else:
        return {"status": "File with the name doesn't exists"}




@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, process_id: str):
#     th = threading.Thread(target=helper, args=(websocket, process_id))
#     th.start()

    await websocket.accept()
    print(process_id)
    
    while True:
        
        try:
            obj = util_instance.my_func(process_id)
        except Exception as e:
            print(e, " Websocket going to stop: ")
            print(obj)

        # print(obj)
        if obj != 0:
            await websocket.send_json(obj)
            await asyncio.sleep(5)
            
        else: 
            await websocket.send_json({"status": "process completed"})
            await websocket.close()
            break #This line makes it non-blocking function instead of time.sleep()

   


