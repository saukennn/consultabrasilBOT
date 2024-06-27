import ssl
import asyncio
from time import sleep
import websockets
import queue
import threading
from websockets.server import WebSocketServerProtocol
from bot import Bot
import json

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain('cert/cert.pem', 'cert/key.pem')

def bot_handler(queue1: queue.Queue, queue2: queue.Queue):
    bot = Bot()
    bot.start()
    bot.get_link_via_rg()
    
    is_logged = False
    post = False
    setInfo = False
    date = {}
    hour = ""

    while True:
        try:
            message = queue1.get()

            if isinstance(message, str):
                if message == "quit":
                    bot.close()
                    return
            
            if (not is_logged and (message["cpf"] and message["pass"])):
                bot.login(message["cpf"], message["pass"])
                queue2.put(not bot.in_login())
                if bot.in_login():
                    bot.start()
                    bot.get_link_via_rg()

                    continue

                is_logged = True
                bot.skip()
                queue1.task_done()

            if message["post"] and not post:
                post = True

                try:
                    bot.select_post(message["post"])
                except:
                    queue2.put("exists")
                    queue1.task_done()
                    break


                dates = bot.get_date()
                queue2.put(dates)
                queue1.task_done()

                continue

            if message["date"] and not date:
                splited = message["date"].split("-")
                date = {
                    "year": int(splited[0]),
                    "month": int(splited[1]) - 1,
                    "day": int(splited[2])
                }
                bot.select_date(date)

                hours = bot.get_hours()
                queue2.put(hours)
                queue1.task_done()

                continue

            if message["hour"] and not hour:
                hour = message["hour"]
                bot.select_hour(hour)

                info = bot.get_info()
                queue2.put(info)
                queue1.task_done()

                continue

            if message["orig"] and message["option"] and message["email"] and not setInfo:
                resp = dict()
                setInfo = {
                    "rg": message["option"],
                    "naturalidade": message["orig"],
                    "email": message["email"],
                    "phone": None
                }

                if "phone" in message:
                    setInfo["phone"] = message["phone"]

                while True:
                    bot.set_info(setInfo["rg"], setInfo["naturalidade"], setInfo["email"], setInfo["phone"])
                    sleep(1)

                    try:
                        resp = bot.finish()
                    except:
                        continue

                    break

                queue2.put(resp)
                queue1.task_done()

                continue
        
        except Exception as err:
            print(err)

            break

    queue2.put("timeout")
    bot.close()


async def handle_websocket(websocket: WebSocketServerProtocol, path):
    q1 = queue.Queue()
    q2 = queue.Queue()
    t = threading.Thread(target=bot_handler, args=(q1, q2))
    t.start()

    while True:
        try:
            message = json.loads(await websocket.recv())
                
            q1.put(message)

            while True:
                try:
                    await asyncio.sleep(1)
                    msg = q2.get(False)

                    if isinstance(msg, str):
                        if msg == "timeout":
                            raise websockets.exceptions.ConnectionClosedOK
                        
                    await websocket.send(json.dumps(msg))
                    q2.task_done()
                    break

                except websockets.exceptions.ConnectionClosedOK:
                    raise websockets.exceptions.ConnectionClosedOK

                except Exception as err:
                    pass

        except websockets.exceptions.ConnectionClosedOK:
            print("Conexão fechada.")
            break

        except Exception as err:
            print(err)

            await websocket.send(json.dumps("timeout"))

    q1.put("quit")

async def start_server():
    async with websockets.serve(handle_websocket, "0.0.0.0", 8765, ssl=ssl_context):
        print("Servidor WebSocket iniciado.")

        await asyncio.Future()  # Aguarda indefinidamente

if __name__ == "__main__":
    asyncio.run(start_server())
