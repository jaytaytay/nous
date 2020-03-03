#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  4 12:32:17 2019

@author: Liam
"""

# -----------------------------------------
#    To run; navigate to /Users/liam/Dropbox/Nous/FPL/dev
#    execute; bokeh serve --show bokeh_player_test.py
# -----------------------------------------

# -----------------------------------------
#     Import stuff
# -----------------------------------------
import pandas as pd

import sys
import os

import novelties.novelty1 as novelty1
import novelties.novelty2 as novelty2
import novelties.novelty3 as novelty3
import novelties.novelty4 as novelty4
import novelties.novelty5 as novelty5
import novelties.novelty6 as novelty6
import novelties.novelty7 as novelty7

import config

from bokeh.models.widgets import Tabs
from bokeh.io import curdoc

# -----------------------------------------
#       files
# -----------------------------------------
path                = os.getcwd()               #/Users/liam/Dropbox/Nous/nous
sys.path.append(path)

dirpath             = os.path.dirname(path)     #FPL

encoding = 'latin1'

# PL
df_pl_players   = pd.read_csv(config.path_pl_players, encoding=encoding)
df_pl_past      = pd.read_csv(config.path_pl_past)  # df_gw_data

df_fixtures     = pd.read_csv(config.path_pl_fixtures)
df_team_info    = pd.read_csv(config.path_dict_teams, index_col='code')

# Fantasy
df_lineups      = pd.read_csv(config.path_lineups)
df_single_lines = pd.read_csv(config.path_results)


df_novelty_2    = pd.read_csv(config.path_novelty_2) 
df_novelty_5    = pd.read_csv(config.path_novelty_5, header=None)
df_novelty_5.columns = ['gw','owner','gw_score']

dict_owners = config.dict_owners

##########################################
#          Build tabs
##########################################

    # -----------------------------------------
    #       Performance
    # -----------------------------------------

    # -----------------------------------------
    #       Novelties
    # -----------------------------------------
    
#    1. Highest Round Team Score (excluding double game-weeks).
tab1 = novelty1.novelty1(df_single_lines)

#    2 Highest 1-Game Player Score (Can be 1 game from a double game-week).
tab2 = novelty2.novelty2(df_novelty_2)

#    3 Highest Losing Score (excluding double game-weeks).
tab3 = novelty3.novelty3(df_single_lines)

#    4 Lowest Winning Score. 
tab4 = novelty4.novelty4(df_single_lines)

#    5 Highest Bench Score in a game-week. Bench players  who are auto-subbed on will not count (Players dropped to the bench to "rig" this will be excluded if the league agree).
tab5 = novelty5.novelty5(df_novelty_5, dict_owners)

#    6 Most wins against the eventual champion.
tab6 = novelty6.novelty6(df_single_lines)

#    7 Worst First Round Pick (Player score for the season).
tab7 = novelty7.novelty7(df_pl_past, df_team_info, df_pl_players, dict_owners)

#    8 Most player points from a waiver request/free agent pick-up the week after (Can count 1 game scores from double game-weeks).    
tab8 = novelty7.novelty7(df_pl_past, df_team_info, df_pl_players, dict_owners)


# -----------------------------------------
#       Stich tabs into app
# -----------------------------------------
tabs = Tabs(tabs=[tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8])
#tabs = Tabs(tabs=[tab1, tab2])

#theme = Theme(filename=path_theme)

#curdoc().theme=theme

# Put the tabs in the current document for display
curdoc().add_root(tabs)
