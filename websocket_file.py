from Server import app, WebSocket, Running, Waiting
import time


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
