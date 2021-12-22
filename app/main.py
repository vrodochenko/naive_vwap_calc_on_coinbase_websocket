import sys
from time import sleep

from app.client import MyWebsocketClient

client = MyWebsocketClient()
client.start()
print(client.url, client.products)
try:
    while True:
        print("\nMessageCount =", "%i \n" % client.message_count)
        sleep(1)
except KeyboardInterrupt:
    client.close()

if client.error:
    sys.exit(-1)
else:
    sys.exit(-2)