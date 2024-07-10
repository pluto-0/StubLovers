import requests
import json
import sqlite3
import pandas as pd
from pprint import pprint

# Only gets 1 page right now
def get_players():
    response = requests.get('https://mlb24.theshow.com/apis/items.json')
    if response.status_code != 200:
        print("Error fetching items data from MLB The Show API, existing program")
        exit(-1)
    data = response.json()['items']

    entries = []
    desired_fields = ['name', 'ovr', 'is_hitter', 'is_live_set', 'uuid', 'trend', 'position']
    for item in data:
        entry = []
        for field in desired_fields:
            entry.append(item[field])
        entries.append(tuple(entry))
    return entries

def make_players_table(conn, cur):
    desired_fields = ['name', 'ovr', 'is_hitter', 'is_live_set', 'uuid', 'trend', 'position']
    types = {'name': 'TEXT', 'ovr': 'INT', 'is_hitter': 'INT', 'is_live_set': 'INT', 'uuid': 'TEXT', 'trend': 'TEXT', 'position': 'TEXT'}
    query = """CREATE TABLE IF NOT EXISTS ShowPlayers(id INT PRIMARY KEY, """
    for i, field in enumerate(desired_fields):
        if i != len(desired_fields) - 1:
            query += f'{field} {types[field]}, '
        else:
            query += f'{field} {types[field]});'
    print(query)
    cur.execute(query)
    conn.commit()

if __name__ == '__main__':
    conn = sqlite3.connect('MLB.db')
    cur = conn.cursor()
    make_players_table(conn, cur)

'''
{'age': 25,
 'arm_accuracy': 30,
 'arm_strength': 45,
 'augment_end_date': None,
 'augment_text': None,
 'baked_img': 'https://cards.theshow.com/mlb24/dbad2066681ee9062972ae33e0be6d7d-baked.webp',
 'baserunning_ability': 9,
 'baserunning_aggression': 4,
 'bat_hand': 'R',
 'batting_clutch': 0,
 'bb_per_bf': 31,
 'blocking': 0,
 'born': 'Pennsylvania',
 'bunting_ability': 30,
 'contact_left': 0,
 'contact_right': 0,
 'display_position': 'SP',
 'display_secondary_positions': '',
 'drag_bunting_ability': 10,
 'event': True,
 'fielding_ability': 26,
 'fielding_durability': 70,
 'fielding_rank_image': '',
 'has_augment': False,
 'has_matchup': False,
 'has_rank_change': False,
 'height': '6\'4"',
 'hit_rank_image': '',
 'hits_per_bf': 50,
 'hitting_durability': 0,
 'hr_per_bf': 49,
 'img': 'https://mlb24.theshow.com/rails/active_storage/blobs/redirect/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBCR3d2RFJNPSIsImV4cCI6bnVsbCwicHVyIjoiYmxvYl9pZCJ9fQ==--3057a6b6c1caa62563335afe0e8c5ea49d69bc5e/49bd1fc864af1c5915d8360b7af53001.webp',
 'is_hitter': False,
 'is_live_set': True,
 'is_sellable': True,
 'jersey_number': '49',
 'k_per_bf': 66,
 'name': 'A.J. Alexy',
 'new_rank': 63,
 'ovr': 63,
 'pitch_control': 56,
 'pitch_movement': 99,
 'pitch_velocity': 74,
 'pitches': [{'control': 71,
              'movement': 80,
              'name': '4-Seam Fastball',
              'speed': 94},
             {'control': 55, 'movement': 70, 'name': 'Slider', 'speed': 84},
             {'control': 60,
              'movement': 45,
              'name': 'Circle Change',
              'speed': 88},
             {'control': 40,
              'movement': 99,
              'name': '12-6 Curve',
              'speed': 79}],
 'pitching_clutch': 47,
 'plate_discipline': 0,
 'plate_vision': 0,
 'power_left': 0,
 'power_right': 0,
 'quirks': [],
 'rarity': 'Common',
 'reaction_time': 25,
 'sc_baked_img': None,
 'series': 'Live',
 'series_texture_name': '',
 'series_year': 2017,
 'set_name': 'CORE',
 'speed': 25,
 'stamina': 74,
 'stars': None,
 'team': 'Free Agents',
 'team_short_name': 'FA',
 'throw_hand': 'R',
 'trend': None,
 'type': 'mlb_card',
 'ui_anim_index': 0,
 'uuid': 'dbad2066681ee9062972ae33e0be6d7d',
 'weight': '195 lbs'}
 '''
