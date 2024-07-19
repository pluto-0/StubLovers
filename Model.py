import pandas as pd
import sqlite3
from pprint import pprint
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.neural_network import MLPRegressor, MLPClassifier
from sklearn.model_selection import train_test_split as split
from sklearn.metrics import accuracy_score

conn = sqlite3.connect('MLB.db')
cur = conn.cursor()

X = ['g', 'pa', 'ops', 'h', 'doubles', 'triples', 'hr', 'rbi']
y = 'rarity'

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

train_df, test_df = split(df, test_size=.15, random_state=1)
scores = {}

for i in range(1, 11):
    for j in range(1, 11):
        for k in range(1, 11):
            layer_sizes = (i, j, k)
            nn = MLPClassifier(layer_sizes)
            print('training model of size ', layer_sizes)
            nn.fit(train_df[X], train_df[y])
            scores[layer_sizes] = nn.score(test_df[X], test_df[y])
pprint(scores)