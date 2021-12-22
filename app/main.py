import sys
from time import sleep

from app.client import CoinbaseClient

client = CoinbaseClient()
client.open()
print(client.url, client.products)
try:
    while True:
        sleep(1)
except KeyboardInterrupt:
    client.close()

if client.error:
    sys.exit(-1)
else:
    sys.exit(-2)
