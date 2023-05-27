import json
from sortedcontainers import SortedDict

FILENAME = 'coinbase.txt'

# parse the snapshot message
def parse_snapshot(ws_data):
    for ask in ws_data['asks']:
        print(ask[0])
    for bid in ws_data['bids']:
        print(bid[0])

# parse the ws message and understand what to do
def parse_coinbase(ws_data):
    if ws_data['type'] == 'snapshot':
        parse_snapshot(ws_data)

# read the data file
with open(FILENAME) as file:
    while line := file.readline():
        parse_coinbase(json.loads(line))