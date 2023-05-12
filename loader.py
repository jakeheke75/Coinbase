import json
FILENAME = 'coinbase.txt'

# parse the snapshot message
def parse_snapshot(ws_data):
    print(ws_data)

# parse the ws message and understand what to do
def parse_message(ws_data):
    if ws_data['type'] == 'snapshot':
        parse_snapshot(ws_data)

# read the data file
with open(FILENAME) as file:
    while line := file.readline():
        parse_message(json.loads(line))