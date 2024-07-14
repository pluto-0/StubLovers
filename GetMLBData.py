import requests
import sqlite3
import pandas as pd
from pprint import pprint
from pybaseball import batting_stats_bref, pitching_stats_bref, pitching_stats

# Only use this if remake of table is needed
def make_hitters_table(conn, cur, data):
    query = """CREATE TABLE IF NOT EXISTS Hitters(id INT PRIMARY KEY, name TEXT, """
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

# Only use if remake of table is needed
def make_pitchers_table(conn, cur, data):
    query = """CREATE TABLE IF NOT EXISTS Pitchers(id INT PRIMARY KEY, name TEXT, """
    column_names = {'#days': 'days', '2B': 'doubles', '3B': 'triples', 'SO9': 'so9', 'GB/FB': 'gbfb', 'SO/W': 'sow'}
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

def fill_hitters_table(conn, cur, data):
    entries = []
    entry_lengths = set()
    for i in range(1, data.shape[0] + 1):
        entry = [i]
        for col in data:
            if i in data[col] and col == "Name":
                entry.append(data[col][i].encode('utf-8'))
            elif i in data[col] and (data[col].dtype == 'int64' or data[col].dtype == 'float64'):
                entry.append(data[col][i].item())
        if len(entry) > 1:
            entry_lengths.add(len(entry))
            entries.append(tuple(entry))

    if len(entry_lengths) > 1:
        print("Different number of stats for different players, exiting without changing database")
        exit(-1)

    query = "INSERT INTO Hitters VALUES(" + "?, " * (len(entries[0]) - 1) + "?);"
    cur.executemany(query, entries)
    conn.commit()

def fill_pitchers_data(conn, cur, data):
    entries = []
    entry_lengths = set()
    id_counter = 1
    for i in range(1, data.shape[0] + 1):
        entry = [id_counter]
        for col in data:
            if i in data[col] and col == 'Name':
                entry.append(data[col][i].encode('utf-8'))
            elif i in data[col] and (data[col].dtype == 'int64' or data[col].dtype == 'float64'):
                entry.append(data[col][i].item())
        if len(entry) > 1:
            entry_lengths.add(len(entry))
            entries.append(tuple(entry))
            id_counter += 1

    if len(entry_lengths) > 1:
        print("Different number of stats for different players, exiting without changing database")
        exit(-1)

    query = "INSERT INTO Pitchers VALUES(" + "?, " * (len(entries[0]) - 1) + "?);"
    cur.executemany(query, entries)
    conn.commit()

if __name__ == '__main__':
    conn = sqlite3.connect('MLB.db')
    cur = conn.cursor()
    hitting_data = batting_stats_bref(2024)
    pitching_data = pitching_stats_bref(2024)
    #make_hitters_table(conn, cur, hitting_data)
    #make_pitchers_table(conn, cur, pitching_data)
    fill_hitters_table(conn, cur, hitting_data)
    fill_pitchers_data(conn, cur, pitching_data)