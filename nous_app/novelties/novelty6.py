#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 22:16:54 2019

@author: liam
"""

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#         Bokeh visualisation MM Fantasy - Novelty #6: 
#    6 Most wins against the eventual champion.
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# ==============================================================================
# Chapter 1: Import modules
# ==============================================================================

import pandas as pd
import numpy as np

from bokeh.plotting import figure
from bokeh.models import Range1d, HoverTool, ColumnDataSource, Panel, CrosshairTool, Title

import emoji

from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource, LabelSet
from bokeh.layouts import column
from bokeh.models import Panel, DataTable, TableColumn, Title
#import config

# Styling for plot
def style(p):
    # Title 
    p.title.align = 'center'
    p.title.text_font_size = '20pt'
    p.title.text_font = 'serif'

    # Axis titles
    p.xaxis.axis_label_text_font_size = '14pt'
    p.xaxis.axis_label_text_font_style = 'bold'
    p.yaxis.axis_label_text_font_size = '14pt'
    p.yaxis.axis_label_text_font_style = 'bold'

    # Tick labels
    p.xaxis.major_label_text_font_size = '12pt'
    p.yaxis.major_label_text_font_size = '12pt'

    return p

# Function to make the plot
def make_plot(df_table):
    
    df_table = df_table.reset_index(drop=False)
   
    cds_table = ColumnDataSource(df_table)
    
    list_cols = [TableColumn(field = "index", title = "", width=300)]
    for owner in df_table.columns[1:]:
        list_cols.append(TableColumn(field = owner, title = owner))

    data_table = DataTable(source = cds_table, columns=list_cols, editable = False, fit_columns=True, index_position=None)
    
    nov_6_text = "Current league-leader is " # + str(ladder_leader_team) + " (" + str(ladder_leader_owner) + "). " \
                 # + team + " (" + owner + ") has beaten them " + str(int(score)) + " times"

    return data_table, nov_6_text

def make_table(df):
    
    df_grouped = df.groupby(by=['owner','opp_owner','result']).count().astype(int)
    df_table = pd.DataFrame()
    for owner in set(df.owner):
        for opp in set(df.owner):
            try:
                df_table.loc[owner,opp] = int(df_grouped.loc[owner,opp,'W'].max())
            except:
                df_table.loc[owner,opp] = int(0)
        
    df_table['Total Wins'] = df_table.sum(axis=1).astype(int).astype(str)

    nov_6_text = "Current league-leader is " # + str(ladder_leader_team) + " (" + str(ladder_leader_owner) + "). " \
                 # + team + " (" + owner + ") has beaten them " + str(int(score)) + " times"

    # for owner in set(df.owner):
    #     most_wins = df_table[owner].max()
    #     df_table.loc['Novelty winner(s) would be:', owner] = ', '.join(list(df_table[df_table[owner]==most_wins].index))

    for owner in set(df.owner):    
        df_table[owner] = df_table[owner].astype(int).astype(str)

    return df_table, nov_6_text
# -----------------------------------------
#       Main Script
# -----------------------------------------

def novelty6(df_single_lines):

    df_table, nov_6_text = make_table(df_single_lines)
    
    # table, nov_6_text = make_plot(df_table)
    
    # Make a tab with the layout 
#    tab = Panel(child=table, title = 'Novelty 6')
    return df_table.astype(str), nov_6_text

