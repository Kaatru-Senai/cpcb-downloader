# from Server import app, WebSocket, Running, Waiting, BaseModel
# import pandas as pd

# # def Find_obj(process_id):
# #     if len(Running) >0 or len(Waiting) > 0:
# #         print("inside loop")

# #         for k,v in list(Running.items()):
# #             print(f'key: {k} value: {v} v.id = {v.id} process_id: {process_id} type: {type(process_id)}')
# #             if str(v.id) == process_id:
# #                 return v
# #         for v in Waiting:
# #             if str(v.id) == process_id:
# #                 return v
# #     else:
# #         print('No Items found')
# #         return None
# # def my_func(process_id):
    
# #     obj = Find_obj(process_id)
# # #     if obj:
# # #         data = {
# # #             "process_id": process_id,
# # #             "Progress": f'{obj.progress}%',
# # #             "estimated time": f'{str(obj.estimated_time())} miliseconds'
# # #         }
# # #         return data
# # #     print("couldn't find anything")





# # # @app.websocket("/ws")
# # # async def websocket_endpoint(websocket: WebSocket, process_id: str):
# # #     await websocket.accept()
# # #     print(process_id)
# # #     while True:
# # #         # data = await websocket.receive_text()
# # #         obj = {
# # #             "Default": "Value"
# # #         }
# # #         # try:
# # #         #     obj = my_func(process_id)
# # #         # except Exception as e:
# # #         #     print(e)
# # #         # # print(Obj)
# # #         await websocket.send_json(obj)
# # #         time.sleep(5)


# # # class Filename(BaseModel):
# # #     name: str

# # # @app.get("/get_file")
# # # async def send_csv(id: Filename ):
# # #     re

# # from fastapi.responses import StreamingResponse
# # import io

# # @app.get("/get_csv")
# # async def get_csv():

# #     df = pd.read_csv('cpcb-data.csv')

# #     stream = io.StringIO()

# #     df.to_csv(stream, index = False)

# #     response = StreamingResponse(iter([stream.getvalue()]),
# #                         media_type="text/csv"
# #     )

# #     response.headers["Content-Disposition"] = "attachment; filename=cpcb-data.csv"

# #     return response




# import pandas as pd

# df = pd.DataFrame()

# data = [['34342', 23.434, 34.4545]]

# d1 = {"Name": ["Pankaj", "Lisa"], "ID": [1, 2]}
# d2 = {"Role": ["Admin", "Editor"]}

# df1 = pd.DataFrame(d1, index={1, 2})
# df2 = pd.DataFrame(d2, index={1, 2})




# for i in range(10):
#     df1 = pd.concat([df1, df2], axis=1)
    
# print(df1)


# import Server
# import threading
# WebSocket = Server.WebSocket
# import asyncio
# import time
# app = Server.app


# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket, process_id: str):
#     # th = threading.Thread(target=asyncio.run, args=(ws_endpoint(websocket, process_id),))
#     # th.start()
#     await ws_endpoint(websocket, process_id)





# async def ws_endpoint(websocket: WebSocket, process_id: str):
#     await websocket.accept()
#     print(process_id)
#     while True:
#         # data = await websocket.receive_text()
#         obj = {
#             "Default": "Value"
#         }
#         # try:
#         #     obj = my_func(process_id)
#         # except Exception as e:
#         #     print(e)
#         # # print(Obj)
#         await websocket.send_json(obj)
#         time.sleep(5)

# list1 = {"k":1, "k1":2}
# list2 = [3,4,5]
# def func():

#     if len(list1) > 0 or len(list2)>0:
#         for k,v in list(list1.items()):
#             print(k,v)
#             if v == 3:
#                 return i
#         for i in list2:
#             if i == 3:
#                 return i

#     print("couldn't find anything")
#     return 0

# print(func())

# import smtplib

# s = smtplib.SMTP('smtp.gmail.com', 587)
# s.ehlo()
# s.starttls()

# s.login("mycoursepm@gmail.com", "uzoqdufuwprwrdid")

# message = "Your process created successfully and ready for execution you can check it's progress at link  http://localhost:8000/query"
# s.sendmail("mycoursepm@gmail.com", "ashismaity651@gmail.com", message)
# s.quit()