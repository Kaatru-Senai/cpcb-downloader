import asyncio
from concurrent.futures import thread
import uvicorn
import threading
import os
from fastapi import FastAPI, Body, WebSocket
from pydantic import BaseModel
import datetime
from dateutil import parser
import time
from fastapi.responses import StreamingResponse
import io
import pandas as pd
from configparser import ConfigParser
from utility import clear_directory,send_email,schedule, my_func, Running, Waiting
from main import Downloader
from zoneinfo import ZoneInfo

app = FastAPI()

class Post(BaseModel):
    fdate: str 
    tdate: str
    src_type: str
    mail: str
    
file = 'configfile.ini'
config = ConfigParser()
config.read(file)

dev_mode = int(config['dev mode']['dev'])




def query_helper_func(f_date, t_date, flag, mail):
    """Process the datetime obj it got from post request, and create the process with this and push that into waiting list, to be schedule by the schedule function inside utility.py
    also return a response containing status and processs id as a json format."""
    

    if f_date or t_date:
        try:
           
            try:
                from_date = parser.parse(f_date)
                to_date = parser.parse(t_date)
            except Exception as e:
                print(e)
            

            if from_date < to_date:
                k = datetime.datetime.now(tz=ZoneInfo('Asia/Kolkata'))
                current_time = parser.parse(k.strftime("%Y-%m-%d %H:%M:%S"))
                
                if to_date > current_time: #Taking IST as standard time for container
                    
                    return 'ERROR: to datetime should not exceed present datetime'
                else:
                    print('Fetching data')
                    Dd: Downloader = Downloader(from_date, to_date, flag)
                    res = {}
                    res['Status'] = "process created"
                    res['id'] = Dd.id
                    

                    Waiting.append(Dd)
                    threading.Thread(target=send_email, args=(mail, Dd.id)).start()
                    
                    return res   
            else:
                return 'ERROR: from date should come before to date'
        except ValueError as err:
            return 'ERROR: entered date format is not right '+ str(err)
    else:
        return 'ERROR: required arguments missing'


@app.post("/query")
async def get_date(data: Post):
    """ Take from_date, to_date and email from client and call query_helper_func() and return the json response"""

    # print(data)
    
    f_date = data.fdate
    t_date = data.tdate
    email = data.mail
    flag = data.src_type
    
    res = query_helper_func(f_date, t_date, flag, email)
    return res






threading.Thread(target=schedule, args=()).start()
"""Start the Schedule function in a different thread which is responsible for Scheduling and manage the process that had been created"""

threading.Thread(target=clear_directory, args=()).start()
"""Responsible for deleting the downloaded csv inside Dowloaded_csv folder, which are more than 1 hour here."""




@app.get("/get_csv")
async def get_csv(id: str):
    """Take process id as get request and return the csv file downloaded by that process"""

    if os.path.exists(f'./Downloaded_csv/{id}.csv'):
        if not dev_mode:
            df = pd.read_csv(f'./Downloaded_csv/{id}.csv')
        else:
            df = pd.read_csv(f'./file0.csv')

        stream = io.StringIO()

        df.to_csv(stream, index = False)

        response = StreamingResponse(iter([stream.getvalue()]),
                            media_type="text/csv"
        )

        response.headers["Content-Disposition"] = f"attachment; filename={id}.csv"

        return response

    else:
        return {"status": None}




@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, process_id: str):
    """Takes process_id for connection and emit the progress of the process in every 5 seconds in json format"""

    await websocket.accept()
    print(process_id)
    
    while True:
        
        try:
            obj = my_func(process_id)
        except Exception as e:
            print(e, " Websocket going to stop: ")
            print(obj)

        if obj != 0:
            await websocket.send_json(obj)
            await asyncio.sleep(5)
            
        else: 
            await websocket.send_json({"status": "process completed"})
            await websocket.close()
            break 



@app.get("/estimated_time")
def get_estimated_time(process_id: str):
    obj = {"estimated time": 0}
    try:
        obj = my_func(process_id)
    except Exception as e:
        print(e, " Websocket going to stop: ")
        print(obj)
    return obj

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=3000)
    
