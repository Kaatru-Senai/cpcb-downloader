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
"""Running is a dict which have process id as key and Downloader obj as value"""
Waiting = []


def query_helper_func(f_date, t_date, mail):
    """Process the datetime obj it got from post request, and create the process with this and push that into waiting list, to be schedule by the schedule function inside utility.py
    also return a response containing status and processs id as a json format."""
    
    if f_date or t_date:
        try:
            x = f_date.strftime("%d-%m-%y %H:%M")
            y = t_date.strftime("%d-%m-%y %H:%M")
           
            
            from_date = datetime.datetime.strptime(x, '%d-%m-%y %H:%M')
            to_date = datetime.datetime.strptime(y, '%d-%m-%y %H:%M')

            

            if from_date < to_date:
                if to_date > datetime.datetime.now():
                    return 'ERROR: to datetime should not exceed present datetime'
                else:
                    print('Fetching data')
                    Dd: Downloader = Downloader(from_date, to_date)
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
    """ Take from_date, to_date and email from client and call query_helper_func() and return the json response"""
    f_date = data.fdate
    t_date = data.tdate
    email = data.mail
    
    res = query_helper_func(f_date, t_date, email)
    return res






threading.Thread(target=util_instance.schedule, args=()).start()
"""Start the Schedule function in a different thread which is responsible for Scheduling and manage the process that had been created"""

threading.Thread(target=clear_directory, args=()).start()
"""Responsible for deleting the downloaded csv inside Dowloaded_csv folder, which are more than 1 hour here."""




@app.get("/get_csv")
async def get_csv(id: str):
    """Take process id as get request and return the csv file downloaded by that process"""

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
    """Takes process_id for connection and emit the progress of the process in every 5 seconds in json format"""

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

   


