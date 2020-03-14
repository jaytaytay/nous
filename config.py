#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 18:01:10 2019

@author: Liam
"""

import os

path            = os.path.join(os.getcwd(), 'nous_app')

#import sys
chrome_driver = '/usr/local/bin/chromedriver 2'

path_lineups    = os.path.join(path, 'data' ,'fantasy' ,'1920' ,'latest_lineups.csv')

path_results    = os.path.join(path, 'data' ,'fantasy' ,'1920' ,'latest_results.csv')

path_transfers  = os.path.join(path, 'data' ,'fantasy' ,'1920' ,'latest_transfers.csv')

path_novelty_2  = os.path.join(path, 'data' ,'fantasy' ,'1920' ,'novelty_2.csv')
path_novelty_5  = os.path.join(path,'data' ,'fantasy' ,'1920' ,'novelty_5.csv')

dict_owners = {
                'Matt Lowry':       {'team': "Ol' Cider's Lowry",              'first_round_pick': 191,    'colour':'#ffe6d2'},
                'Dylan Urquhart':   {'team': 'Heung like Son' ,                'first_round_pick': 214,    'colour':'#cc66cc'},
                'james west':       {'team': 'best in the west' ,              'first_round_pick': 215,    'colour':'#ffb400'},
                'Peter Allan':      {'team': 'Wizards of Ozil' ,               'first_round_pick': 11,     'colour':'#c73b32'},
                'Liam Fariss':      {'team': 'Corner taken quickly, ORIGIII!' ,'first_round_pick': 12,     'colour':'#32b4ff'},
                'Liam Hussey':      {'team': 'The Feminist Agenda' ,           'first_round_pick': 210,    'colour':'#995f3d'},
                'Tom Barratt':      {'team': "Ain't No Holebas Girl",          'first_round_pick': 192,    'colour':'#0ac832'},
                'Dominic Drewery':  {'team': 'Chopporoos' ,                    'first_round_pick': 338,    'colour':'#1e2832'}
                }

path_pl_past     = os.path.join(path,'data' ,'pl' ,'1920' ,'past.csv')
path_player_info = os.path.join(path,'data' ,'pl' ,'1920' ,'player_info.csv')
path_player_info_json = os.path.join(path, 'data' ,'pl' ,'1920' ,'player_info.json')
path_pl_players  = os.path.join(path,'data' ,'pl' ,'1920' ,'pl_players.csv')
path_pl_fixtures = os.path.join(path,'data' ,'pl' ,'1920' ,'pl_fixtures.csv')
path_pl_teams    = os.path.join(path,'data' ,'pl' ,'1920' ,'pl_teams.csv')
path_pl_future   = os.path.join(path,'data' ,'pl' ,'1920' ,'pl_future.csv')
path_dict_teams  = os.path.join(path,'data' ,'pl' ,'1920' ,'dict_teams.csv')
#
#
##path                = os.getcwd()               #melmac
##sys.path.append(path)
##dirpath                 = os.path.dirname(path)     #FPL
#
##file_player_info        = os.path.join(dirpath, 'data' , 'player_info.csv')
##file_player_info        = 'https://www.dropbox.com/s/4o5cuuqj7i2mrp7/player_info.csv?dl=0'
##output_path             = os.path.join(dirpath, 'data' , '2019/20' , 'player.csv')
##path_gameweeks          = os.path.join(dirpath, 'data' , '2019-20' , 'gameweeks')
#path_master_player_data = 'https://www.dropbox.com/s/do2cnkwh5wnsfw3/1819_master_player_data.csv?dl=1'
##
##base_url            = "https://fantasy.premierleague.com/api/"
##url_bs_static       = "bootstrap-static/"
##path_gw_data_18_19  = os.path.join(dirpath, 'data' , 'historical' , '2018-19' , 'gws' , 'merged_gw.csv')
#path_player_data     = 'https://www.dropbox.com/s/t1l24ug2sqb57f3/1819_players_raw.csv?dl=1'
##path_team_data      = os.path.join(dirpath, 'data' , 'historical' , '2018-19' , 'team_stats.csv')
##path_theme          = os.path.join(dirpath, 'dev' , 'bokeh_dark_theme.yaml')
#path_full_gw_data   = 'https://www.dropbox.com/s/23q6yr45h5rm57k/1819_full_gw_data.csv?dl=1'
#path_full_fixtures  = 'https://www.dropbox.com/s/yrdo47pvlrmieqk/1819_full_fixtures.csv?dl=1'
#
#
#
##path_results         = os.path.join(path, '1819' , 'MM Fantasy EPL 2018.xlsx')
#path_results        = 'https://www.dropbox.com/s/todmhikdcvqyfkh/latest_results.csv?dl=1'           # checked for good 18/19 data
#
#path_results_write          = '/Users/JohnTaylor/Dropbox/Public/kyso/latest_results.csv'
#path_results_pickle_write   = '/Users/JohnTaylor/Dropbox/Public/kyso/latest_results.p'
#path_transfers_write        = '/Users/JohnTaylor/Dropbox/Public/kyso/latest_transfers.csv'
#path_lineups_pickle_write   = '/Users/JohnTaylor/Dropbox/Public/kyso/latest_lineups.p'
#
##path_latest_results_read    = 
#path_lineups_pickle_read    = 'www.dropbox.com/s/a2isktbwghxgcds/latest_lineups.p?dl=0' 
#path_all_lineups_write      = '/Users/JohnTaylor/Dropbox/Public/kyso/latest_lineups.csv'             # checked for good 18/19 data
#path_all_lineups_read       = 'https://www.dropbox.com/s/4vcrgh920hrjrfp/latest_lineups.csv?dl=1'
#path_results_dummy          = 'https://www.dropbox.com/s/b287wvbgdw8hdez/df_results_dummy.csv?dl=1'
#
#path_novelty_2_write        = '/Users/JohnTaylor/Dropbox/Public/kyso/novelty_2.csv'
#path_novelty_2_read         = 'https://www.dropbox.com/s/wftabutt7kx0tma/novelty_2.csv?dl=1'
#
#
#path_novelty_5_write        = '/Users/JohnTaylor/Dropbox/Public/kyso/novelty_5.csv'
#path_novelty_5_read         = 'https://www.dropbox.com/s/n43epsl1dg0qezl/novelty_5.csv?dl=1'
#
#
#                
#path_latest_player_stats_pickle_write = '/Users/JohnTaylor/Dropbox/Public/kyso/latest_player_stats.p'
#
#path_latest_player_gw_stats_pickle_write = '/Users/JohnTaylor/Dropbox/Public/kyso/latest_player_gw_stats.p'
#
#path_pl_past_local         = '/Users/JohnTaylor/Dropbox/Public/kyso/pl_past.csv'
#path_pl_past_public        = 'https://www.dropbox.com/s/fozzavjid9a6ik5/pl_past.csv?dl=1'
#path_pl_future_local       = '/Users/JohnTaylor/Dropbox/Public/kyso/pl_future.csv'
#path_pl_future_public      = 'https://www.dropbox.com/s/if17kudzhvihke9/pl_future.csv?dl=1'
#path_pl_players_local      = '/Users/JohnTaylor/Dropbox/Public/kyso/pl_players.csv'
#path_pl_players_public     = 'https://www.dropbox.com/s/8s0nycnf9otee8i/pl_players.csv?dl=1'
#path_pl_fixtures_local     = '/Users/JohnTaylor/Dropbox/Public/kyso/pl_fixtures.csv'
#path_pl_fixtures_public    = 'https://www.dropbox.com/s/7j6eeorywg90zph/pl_fixtures.csv?dl=1'
#path_pl_teams_local        = '/Users/JohnTaylor/Dropbox/Public/kyso/pl_teams.csv'
#path_pl_teams_public       = 'https://www.dropbox.com/s/3uzenrzop4qgdpd/pl_teams.csv?dl=1'
#path_team_dict_local       = '/Users/JohnTaylor/Dropbox/Public/kyso/dict_teams.csv'
#path_team_dict_public      = 'https://www.dropbox.com/s/ibdi1vtwvmoi13g/dict_team_colour.csv?dl=1'