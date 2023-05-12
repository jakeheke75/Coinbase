
# read the data file
with open(FILENAME) as file:
    while line := file.readline():
        parse_message(json.loads(line))