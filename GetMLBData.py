import requests
import sqlite3
import pandas as pd
from pprint import pprint
from pybaseball import batting_stats_bref

conn = sqlite3.connect('MLB.db')
cur = conn.cursor()
# get all of this season's batting data so far
data = batting_stats_bref(2024)
'''
UNCOMMENT IF YOU NEED TO MAKE MLB TABLE AGAIN:


query = """CREATE TABLE IF NOT EXISTS MLB(id INT PRIMARY KEY, name TEXT, """
column_names = {'#days': 'days', '2B': 'doubles', '3B': 'triples'}
for col in data.columns:
    if col in column_names:
        col_mapped = column_names[col]
    else:
        col_mapped = col

    if data[col].dtype == 'int64':
        query += str(col_mapped.lower() + " INT, ")
    elif data[col].dtype == 'float64':
        query += str(col_mapped.lower() + ' DECIMAL, ')

cur.execute(query[:-2] + ');')
conn.commit()
'''

entries = []
entry_lengths = set()
for i in range(1, data.shape[0] + 1):
    entry = [i]
    for col in data:
        if i in data[col] and col == "Name":
            entry.append(data[col][i])
        elif i in data[col] and (data[col].dtype == 'int64' or data[col].dtype == 'float64'):
            entry.append(data[col][i].item())
    if len(entry) > 1:
        entry_lengths.add(len(entry))
        entries.append(tuple(entry))

if len(entry_lengths) > 1:
    print("Different number of stats for different players, exiting without changing database")
    exit(-1)

query = "INSERT INTO MLB VALUES(" + "?, " * (len(entries[0]) - 1) + "?);"
cur.executemany(query, entries)
conn.commit()
