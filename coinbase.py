import json
import websockets.client
from websockets.exceptions import ConnectionClosedError
import logging
import asyncio
import time

# define local switches/variables for program behaviour
# potentially can be passed as executable arguments
# uri of ws to be called
ws_uri = 'wss://ws-feed.exchange.coinbase.com'
# save ws stream in output text file bool
SAVEFILE = False
# set the debug level of the web service
logger_level = logging.ERROR
# print the ws response to stdout
PRINTWS = False

logger = logging.getLogger('websockets')
logger.setLevel(logger_level)
logger.addHandler(logging.StreamHandler())

# parse the snapshot message
def parse_snapshot(ws_data):
    exit

# parse the ws message and understand what to do
def parse_message(ws_data):
    if ws_data['type'] == 'snapshot':
        parse_snapshot(ws_data) 

# for debugging purpose
def print_ws_response(response):
    print(response)

# test single ws connection
""" async def coinbase():
    async with websockets.client.connect(ws_uri) as wbs:
        await wbs.send(
            json.dumps({
                "type": "subscribe",
                "product_ids": ["BTC-USD"],
                "channels": ["level2",
                             "matches",
                             "heartbeat]
            })
        )
        response = await wbs.recv()
        data = json.loads(response)
        print(data)
asyncio.get_event_loop().run_until_complete(coinbase()) """

# test infinite loop to get data from exchange
async def coinbase():
    wbs = await websockets.client.connect(ws_uri)
    await wbs.send(
        json.dumps({
            "type": "subscribe",
            "product_ids": ["BTC-USD"],
            "channels": ["level2",
                        "matches",
                        "heartbeat"]
        })
    )

    # ws output stored not as a single line file but formatted as a list of
    # strings with one ws response per each line terminated with CR/LF
    # in this way the file can be read line by line and processed to simulate
    # real time ws input
    if SAVEFILE:
        timestamp = time.strftime("%Y%m%d%H%M%S")
        filename = 'coinbase' + '_' + timestamp + '.txt'
        outfile = open(filename, 'w', encoding="utf-8")

    # infinite processing loop for reading ws data
    while True:
        try:
            response = await wbs.recv()
            # parse the ws response
            ws_data = json.loads(response)
            parse_message(ws_data)
            if SAVEFILE:
                outfile.write(response)
                outfile.write('\n')
            if PRINTWS:
                print_ws_response(response)
        except ConnectionClosedError:
            # reconnect in case of connection closed
            continue
        except KeyboardInterrupt:
            # close the ws connection amd close the output file
            wbs.close()
            if SAVEFILE:
                outfile.close()

asyncio.get_event_loop().run_until_complete(coinbase())