from email import message
import time

import smtplib
from genericpath import isfile
from datetime import datetime 
import os

Running = {}
"""Running is a dict which have process id as key and Downloader obj as value"""
Waiting = []
    
def schedule() -> None:
    """ It's a Non-preemtive schedular running on a different thread, if size of Running dict less than 10 then it
    takes programme from Waiting list, start the process and put it inside running dict"""
    while True:
        i = 0
        
        while len( Running) < 10 and len(Waiting)>0:
            i = 1
            temp = Waiting.pop(0)
            Running[temp.id] = temp 

            print(f" len( Running) = {len( Running)} len(Waiting) = {len(Waiting)}")
            print(f"The thread {temp.id} is start  Running")

            temp.thread.start()

        for k , v in list( Running.items()):
            
            if v.progress >= 100:
                print(f"The thread {temp.id} is done executing")
                Running.pop(k)
        if i:
            print(f'{len( Running)} are  Running')
        time.sleep(5)


def find_obj(process_id):
    """this function find the Downloader object first in Running dict then in Waiting list, if it couldn't find anything 
    then it return 0"""
    if len( Running) >0 or len(Waiting) > 0:
        

        for k,v in list( Running.items()):
            if str(v.id) == process_id:
                return v
        for v in Waiting:
            if str(v.id) == process_id:
                return v
    else:
        print('No Items found')
        return 0

def my_func(process_id):
    """This function takes process id and return the id, progress and estimated time of the process
    in Dict format to websocket endpoint in server.py"""
    
    obj = find_obj(process_id)

    if obj:
        try:

            data = {
                "process_id": process_id,
                "Progress": f'{obj.progress}%',
                "estimated time": f'{str(obj.estimated_time())} seconds'
            }
        except Exception as e:
            print(e)

        return data
    
    print("couldn't find anything")
    return 0



def ET( id,et):
    """This is a function call by estimated_time() in  Downloader class in main.py , it returns the
    total time need for the process to be executed"""
    if id in  Running:
        return  Running[id].et
    lines = len(Waiting)//10
    pos = len(Waiting)%10

    Dd= find_nth_smallest_et(pos)

    et = Dd.selftime * (lines+1) + Dd.et
    return et

def find_nth_smallest_et(pos):
    """Return the Process object which have nth_smallest estimated time."""
    list1 = []
    for k,v in list( Running.items()):
        list1.append(v)
    item = None
    for i in range(pos):
        min = 999999
        index = -1
        for j in range(len(list1)):
            if list1[j].et < min:
                min = list1[j].et
                index = j
                item = list1[j]
        
        if index > -1:
            list1.pop(index)

    return item





def send_email(reciver_mail, id):
    """It takes the receiver mail and the process id, and send the process id and the endpoint to this 
    email address, Runs on a different thred"""
    gmail_user = "SENDER_EMAIL"
    gmail_password = "SENDER_PASSWORD"

    sent_from = gmail_user
    to = [f'{reciver_mail}']
    

    email_text = f"subject: Requested Accepted for Downloading\n\n\t Your process id: {id}\n To check the progress use ws://localhost:8000/ws"

    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(gmail_user, gmail_password)
        smtp_server.sendmail(sent_from, to, email_text)
        smtp_server.close()
        print ("Email sent successfully!")
    except Exception as ex:
        print ("Something went wrong….",ex)




def clear_directory():
    """if a file downloaded and here hour or more then this function automatically delete that file 
    
    """
    if not os.path.isdir('./Downloaded_csv'):
            os.mkdir('Downloaded_csv')
            
    while True:
        time_list = []
        now = time.mktime(datetime.now().timetuple())
        print(now)

        for file in os.listdir('./Downloaded_csv'):

            if os.path.isfile(f'./Downloaded_csv/{file}'):
                file_time = os.path.getmtime(f'./Downloaded_csv/{file}')
                
                print(now-file_time)
                if now - file_time > 3600:
                    os.remove(f'./Downloaded_csv/{file}')
                else:
                    time_list.append(file_time)

        sleep_time = (now - min(time_list)) if time_list else 3600 

                    
        time.sleep(sleep_time+30)

