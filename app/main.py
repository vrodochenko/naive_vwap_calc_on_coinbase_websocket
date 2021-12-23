import asyncio

from app.client import CoinbaseClient

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
client = CoinbaseClient()
loop.run_until_complete(client.run())
