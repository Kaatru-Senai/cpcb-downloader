
from email import message
import time
import server
import smtplib
from genericpath import isfile
from datetime import datetime 
import os
class util:
    def __init__(self) -> None:
        pass
        
    def schedule(self):
        while True:
            i = 0
            #print(f" OUTSIDE: len(server.Running) = {len(server.Running)} len(server.server.Waiting) = {len(server.Waiting)}")
            while len(server.Running) < 10 and len(server.Waiting)>0:
                i = 1
                temp = server.Waiting.pop(0)
                server.Running[temp.id] = temp

                print(f" len(server.Running) = {len(server.Running)} len(server.Waiting) = {len(server.Waiting)}")
                print(f"The thread {temp.id} is start server.Running")

                temp.thread.start()

            for k , v in list(server.Running.items()):
                # print(f"{v.id} progress = {v.progress}%")
                
                if v.progress >= 100:
                    print(f"The thread {temp.id} is done executing")
                    server.Running.pop(k)
            if i:
                print(f'{len(server.Running)} are server.Running')
            time.sleep(5)


    def find_obj(self,process_id):
        if len(server.Running) >0 or len(server.Waiting) > 0:
            print("inside loop")

            for k,v in list(server.Running.items()):
                # print(f'key: {k} value: {v} v.id = {v.id} process_id: {process_id} type: {type(process_id)}')
                if str(v.id) == process_id:
                    return v
            for v in server.Waiting:
                print("object in Waiting list ",v)
                if str(v.id) == process_id:
                    print(v, " founded item")
                    return v
        else:
            print('No Items found')
            return 0

    def my_func(self,process_id):
        
        obj = self.find_obj(process_id)
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



    def ET(self, id, et):
        if id in server.Running:
            return server.Running[id].et
        lines = len(server.Waiting)//10
        pos = len(server.Waiting)%10

        Dd: util = self.find_nth_smallest_et(pos)

        self.et = Dd.selftime * (lines+1) + Dd.et
        return self.et

    def find_nth_smallest_et(self,pos):
        list1 = []
        for k,v in list(server.Running.items()):
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

    def send_email(self, sender_mail, sender_password, reciver_mail):
        print("Email sending is not occur : NEED enhancement")
        return
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()

       

        message = "Your process created successfully and ready for execution you can check it's progress at link  http://localhost:8000/query"
        s.sendmail(sender_mail, reciver_mail, message)
        s.quit()

    



def clear_directory():
    while True:
        time_list = []
        now = time.mktime(datetime.now().timetuple())
        print(now)

        for file in os.listdir('./Downloaded_csv'):

            if os.path.isfile(f'./Downloaded_csv/{file}'):
                file_time = os.path.getmtime(f'./Downloaded_csv/{file}')
                
                print(now-file_time)
                if now - file_time > 100:
                    os.remove(f'./Downloaded_csv/{file}')
                else:
                    time_list.append(file_time)

        sleep_time = (now - min(time_list)) if time_list else 100 

                    
        time.sleep(sleep_time+30)

