import pandas as pd
import sqlite3
from pprint import pprint
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split as split
from sklearn.metrics import accuracy_score

conn = sqlite3.connect('MLB.db')
cur = conn.cursor()

X = ['g', 'pa', 'ops', 'h', 'doubles', 'triples', 'hr', 'rbi']
y = 'ovr'

cols_from_hitters = ['name', 'g', 'pa', 'ops', 'h', 'doubles', 'triples', 'hr', 'rbi']

query = f"SELECT " + ''.join([x + ', ' for x in cols_from_hitters])[:-2] + " FROM Hitters;"
hitter_data = cur.execute(query).fetchall()

cols_from_show = ['name', 'ovr', 'rarity']
query = f"SELECT " + ''.join([x + ', ' for x in cols_from_show])[:-2] + " FROM ShowPlayers;"
show_data = cur.execute(query).fetchall()

show_df = pd.DataFrame(show_data, columns=cols_from_show)
hitter_df = pd.DataFrame(hitter_data, columns=cols_from_hitters)
#possible_names = set(hitter_df['name'])

df = pd.merge(show_df, hitter_df, how='left', on='name')
for element in X + [y]:
    df = df[df[element].notna()]

linear_model = LinearRegression()

#train_df, test_df = split(df, test_size=.15, random_state=1)
linear_model.fit(df[X], df[y])
print(linear_model.score(df[X], df[y]))