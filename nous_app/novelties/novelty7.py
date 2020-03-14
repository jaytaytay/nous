#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  4 09:44:24 2019

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
import emoji

from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource, LabelSet
from bokeh.layouts import column
from bokeh.models import Panel, DataTable, TableColumn, Title


def make_dataset(df_pl_past, df_team_info, df_pl_players, dict_owners):

    x_list_rounds = []
    y_list_total_points = []
    round_points = []
    label_list = []
    colour1_list = []
    round_opponent = []
    y_range_max = 30
    player_id = []
    
    df_owners = pd.DataFrame.from_dict(dict_owners).T
    dict_picks = df_owners['first_round_pick'].to_dict()
    dict_picks = {v: k for k, v in dict_picks.items()}
    
    dict_team_names = df_owners['team'].to_dict()
#    dict_team_names = {v: k for k, v in dict_team_names.items()}
    
    for player in list(dict_picks.keys()):
        df = df_pl_past[df_pl_past['player_id']==player]
        player_id.append(player)
#        y_list_total_points.append(0)  # for zero-th round
        y_list_total_points.append([0] + list(df['total_points'].cumsum()))
        round_points.append(list(df['total_points']))     
        round_opponent.append(df['opposition_name'])
        label_list.append(df['friendly_name'].iloc[0])
        owner = df_owners[df_owners['first_round_pick']==player].reset_index(drop=False)['index'].item()
        colour1_list.append(df_owners.loc[owner, 'colour'])
        x_list_rounds.append(list(range(0,39)))
        y_range_max = max(y_range_max, df['total_points'].cumsum().max())
    
    dict_source = dict(
                    xs=x_list_rounds,
                    cums=y_list_total_points,
                    labels=label_list,
                    colour1=colour1_list,
                    round_points=round_points
                    )

    list_table_points = []
    for i in range(0,len(y_list_total_points)):
        list_table_points.append(max(y_list_total_points[i]))

    df = pd.DataFrame({
                        'player':label_list,
                        'total_points':list_table_points,
                        'player_id':player_id
                        }
                    )
    
    df = df.sort_values(by='total_points', ascending=False)
    df['owner'] = df['player_id'].map(dict_picks)
    df['team'] = df['owner'].map(dict_team_names)
    df['rank'] = df['total_points'].rank(method='min', ascending=False)
    team_name = df[df['rank'] == 8]['team'].item() + ' ' + emoji.emojize(':money-mouth_face:')
    df.loc[df[df['rank'] == 8].index, 'team'] = team_name
    
    df_labels = df[['player','total_points']].rename(columns={'total_points':'ys'}).sort_values(by='ys',ascending=False).reset_index(drop=True)
    df_labels['xs'] = 8*[len(y_list_total_points[0])-1]
    for i in range(1,len(df_labels)):
        delta = df_labels.loc[i-1, 'ys'] - df_labels.loc[i, 'ys']
        if delta < 2:
            df_labels.loc[i, 'ys'] = df_labels.loc[i-1, 'ys'] - 2
            
    return dict_source, y_range_max, df, df_labels

def style(p):
    # Title 
    p.title.align = 'center'
    p.title.text_font_size = '20pt'
    p.title.text_font = 'helvetica'

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
def make_plot(dict_source, y_range_max, df, df_labels):

    series = df.sort_values(by='total_points', ascending=True).iloc[0]
    
    player  = series['player']
    team    = series['team']
    owner   = series['owner']
    score   = series['total_points']
    
    p = figure(aspect_ratio=1.5, sizing_mode="scale_both",
              x_axis_label = 'Rounds', x_range =(0,38),
              y_axis_label = 'Total Points', y_range=(0, y_range_max + 10))
    
    nov_7_text = "Current Lowest Scoring First Round Draft Pick is " + str(player) + ", drafted by " + team + " (" + owner + ") with " + str(int(score)) + " Points"
    
    src = ColumnDataSource(dict_source)    
    p.multi_line(xs='xs', ys='cums',
             line_width=2, line_color='colour1', line_alpha=0.4,
             hover_line_color='colour1', hover_line_alpha=1,
             source=src)
    
    p.add_tools(HoverTool(show_arrow=False, 
                          line_policy='next', 
                          tooltips=[
                                    ('player','@labels')
                                    ]
                          )
                )
    
    df_source = pd.DataFrame.from_dict(dict_source)
    
    for i in range(0,8):
        src = ColumnDataSource(dict(
                                    xs=df_source.loc[i,'xs'],
                                    cums=df_source.loc[i,'cums'] +(39-len(df_source.loc[i,'cums']))* [-1],
                                    labels=[df_source.loc[i,'labels']]*len(df_source.loc[i,'xs'])
                                    )
                                )
        p.circle('xs', 'cums', source=src, alpha=1, size=4, color = df_source.loc[i,'colour1'])
    
    labels = LabelSet(
                    x='xs',
                    y='ys',
                    text='player',
                    level='glyph',
                    x_offset=0.7, 
                    y_offset=0, 
                    source=ColumnDataSource(df_labels), 
                    render_mode='canvas',
                    text_font_size='10pt')

    p.add_layout(labels)
    
    # Styling
    p = style(p)
    
    return p, nov_7_text

def make_table(df_table):
    
    cds_table = ColumnDataSource(df_table)
    
    columns = [TableColumn(field = "rank", title = "Rank", width=50),
               TableColumn(field = "player", title = "Player", width=300),
               TableColumn(field = "total_points", title = "Total Points", width=100),
               TableColumn(field = "owner", title = "Owner", width=200),
               TableColumn(field = "team", title = "Team", width=300),
               ]
    
    data_table = DataTable(source = cds_table, columns = columns, editable = False, fit_columns=True, index_position=None)

    return data_table
# -----------------------------------------
#       Main Script
# -----------------------------------------

def novelty7(df_pl_past, df_team_info, df_pl_players, dict_owners):
    
    dict_source, y_range_max, df_table, df_labels = make_dataset(df_pl_past, df_team_info, df_pl_players, dict_owners)
    p, nov_7_text= make_plot(dict_source, y_range_max, df_table, df_labels)
    table = make_table(df_table)
    
    # Create a row layout
   # layout = column(p, table)
    
    # Make a tab with the layout 
    #tab = Panel(child=layout, title = 'Novelty 7')
    return p, table, nov_7_text
