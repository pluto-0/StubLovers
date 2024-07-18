import pandas as pd
import sqlite3
from pprint import pprint
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split as split
from sklearn.metrics import accuracy_score

conn = sqlite3.connect('MLB.db')
cur = conn.cursor()

query = '''SELECT name, g, pa, ops FROM Hitters;'''
mlb_data = cur.execute(query).fetchall()

query = '''Select name, ovr FROM ShowPlayers WHERE is_hitter = 1;'''
show_data = cur.execute(query).fetchall()

show_df = pd.DataFrame(show_data, columns=['name', 'ovr'])
mlb_df = pd.DataFrame(mlb_data, columns=['name', 'games', 'pa', 'ops'])
mlb_df['name'] = mlb_df['name']
possible_names = set(mlb_df['name'])

df = pd.merge(show_df, mlb_df, how='left', on='name')
df = df[df['games'].notna()]
df = df[df['pa'].notna()]
df = df[df['ops'].notna()]

linear_model = LinearRegression()
X = ['games', 'pa', 'ops']
y = 'ovr'

#train_df, test_df = split(df, test_size=.15, random_state=1)
linear_model.fit(df[X], df[y])
print(linear_model.score(df[X], df[y]))