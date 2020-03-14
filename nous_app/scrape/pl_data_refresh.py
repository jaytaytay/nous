#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 17 11:31:05 2019

@author: Liam
"""


# =========================================
#            PL Data Refresh
# =========================================

# -----------------------------------------
#     Import stuff
# -----------------------------------------

import requests
import json

import pandas as pd
from pandas.io.json import json_normalize
import numpy as np
#import matplotlib as plt
import datetime as dt

import sys
import os

import pickle

import config

base_url        = "https://fantasy.premierleague.com/api/"
url_bs_static   = "bootstrap-static/"

# Download all player data: https://fantasy.premierleague.com/drf/bootstrap-static/
def get_players_info():
    r = requests.get(base_url + url_bs_static)
    jsonResponse = r.json()
    with open(config.path_player_info_json, 'w') as outfile:
        json.dump(jsonResponse, outfile)

# read player info from the json file that we downlaoded
def get_all_players_detailed_json():
    with open(config.path_player_info_json) as json_data:
        d = json.load(json_data)
        return d
    
# -----------------------------------------
# Import fresh player data - full season data
# -----------------------------------------
    get_players_info()

    all_data = get_all_players_detailed_json()
    
    player_data = []
    for element in all_data["elements"]:
        player_data.append(json_normalize(element))
    df_player_data = pd.concat(player_data, sort=False).reset_index(drop=True)
    
# -----------------------------------------
# Import fresh team data - full season data
# -----------------------------------------

    df_team_data = json_normalize(all_data['teams'])
    # save?
    
# -----------------------------------------
# Import fresh fixture data - full season data
# -----------------------------------------
    r = requests.get('https://fantasy.premierleague.com/api/fixtures/')
    jsonResponse = r.json()
    df_fixtures = json_normalize(jsonResponse)
#    df_fixtures_stats = df_fixtures['stats'][0]
    
# -----------------------------------------
#       for each player, import their detailed data.
#        this comes in the form of three dictionaries,
#        fixtures: latest data on upcoming games, in this season
#        history: latest data on completed games, in this season
#        history_past: totalised data for past seasons
# -----------------------------------------    

    players = all_data["elements"]
    df_player_stats = json_normalize(players)
    list_all_players = dict()
    
    for row in range(0,len(df_player_stats)):
        player_id = df_player_stats.loc[row, 'id']
        url = 'https://fantasy.premierleague.com/api/element-summary/' + str(player_id) + '/'
        r = requests.get(url)
        jsonResponse = r.json()
        list_player = []
        list_player.append(json_normalize(jsonResponse['fixtures']))
        list_player.append(json_normalize(jsonResponse['history']))
        list_player.append(json_normalize(jsonResponse['history_past']))
        list_all_players.update({player_id: list_player})
        print(row)
        

    
    # build player - match data - single line for each player's game
    df_future = pd.DataFrame()
    df_past = pd.DataFrame()
    for player in list_all_players.keys():
        df_player_future = list_all_players[player][0]
        df_player_future['player_id'] = player
        df_future = pd.concat([df_future, df_player_future], ignore_index=True, sort=False)
        
        df_player_past = list_all_players[player][1]
        df_player_past['player_id'] = player
        df_past = pd.concat([df_past, df_player_past], ignore_index=True, sort=False)
        
    
    # add in player data
    position_map = {1:'GK', 2:'DEF', 3:'MID', 4:'FWD'}
    df_player_stats['position'] = df_player_stats['element_type'] 
    df_player_stats = df_player_stats.replace({"position": position_map})
    
    # add in team name(s)
    team_code_map = df_team_data[['code','name']].set_index('code').to_dict()['name']
    df_player_stats['team_name'] = df_player_stats['team_code']
    df_player_stats = df_player_stats.replace({"team_name": team_code_map})
    
    team_id_map = df_team_data[['id','name']].set_index('id').to_dict()['name']
    df_fixtures['team_h_name'] = df_fixtures['team_h']
    df_fixtures = df_fixtures.replace({"team_h_name": team_id_map})
    df_fixtures['team_a_name'] = df_fixtures['team_a']
    df_fixtures = df_fixtures.replace({"team_a_name": team_id_map})
    
    df_player_meta_data = df_player_stats[['position', 'first_name', 'photo', 'second_name', 'team', 'team_name', 'news', 'news_added', 'id']]
    
    df_past = pd.merge(df_past, df_player_meta_data, left_on='player_id', right_on='id', how='inner', sort=False)
    df_future = pd.merge(df_future, df_player_meta_data, left_on='player_id', right_on='id', how='inner', sort=False)
    
    df_past = pd.merge(df_past, df_fixtures[['id', 'team_h_difficulty', 'team_h_name', 'team_a_difficulty', 'team_a_name']], left_on='fixture', right_on='id', how='inner', sort=False)
    df_future = pd.merge(df_future, df_fixtures[['code', 'team_h_difficulty', 'team_h_score', 'team_h_name', 'team_a_difficulty', 'team_a_score', 'team_a_name']], left_on='code', right_on='code', how='inner', sort=False)

    # reformat datetimes
    df_past['kickoff_time'] = pd.to_datetime(df_past['kickoff_time'], format='%Y-%m-%dT%H:%M:%SZ')
    df_future['kickoff_time'] = pd.to_datetime(df_future['kickoff_time'], format='%Y-%m-%dT%H:%M:%SZ')

    # add in opposition
    df_past['opposition_name'] = np.where(df_past['was_home'] == True, df_past['team_a_name'], df_past['team_h_name'])

    # add in friendly name
    df_past['friendly_name'] = df_past['first_name'] + " " + df_past['second_name']
    df_player_stats['friendly_name'] = df_player_stats['first_name'] + " " + df_player_stats['second_name']


    df_past = df_past.sort_values(by='kickoff_time')

    # export
    df_past.to_csv(config.path_pl_past)
    df_future.to_csv(config.path_pl_future)
    df_player_stats.to_csv(config.path_pl_players)
    df_fixtures.to_csv(config.path_pl_fixtures)
    df_team_data.to_csv(config.path_pl_teams)
    
#    pickle.dump(df_player_stats, open(config.path_latest_player_stats_pickle_write, "wb"))
#    pickle.dump(df_player_stats, open('/Users/JohnTaylor/Dropbox/Public/kyso/latest_player_stats.p', "wb"))
#
#    pickle.dump(list_all_players, open(config.path_latest_player_gw_stats_pickle_write, "wb"))
#    pickle.dump(list_all_players, open('/Users/JohnTaylor/Dropbox/Public/kyso/latest_player_gw_stats.p', "wb"))