import time

from classes.server import Server


NUM_OF_CLIENTS = 128
PORT = 8800

server = Server("0.0.0.0", PORT)

while True:
    try:
        server.binding(NUM_OF_CLIENTS)

    except Exception as e:
        print("Error on connecting:", e)
        time.sleep(60)
        continue

    break

server.listen_all()
server.close()