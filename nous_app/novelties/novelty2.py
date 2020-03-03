# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 12:14:42 2019

@author: hussl1
"""

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#         Bokeh visualisation MM Fantasy
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# ==============================================================================
# Chapter 1: Import modules
# ==============================================================================

import pandas as pd
import numpy as np

from bokeh.plotting import figure
from bokeh.models import Range1d, HoverTool, ColumnDataSource, Panel, CrosshairTool, Title


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
def make_plot(df_plot):
    
    current_highest_player_score = []

    for i in range(1,39):
        current_highest_player_score.append(df_plot[df_plot['gw'] == i]['score'].max())
    
    current_highest_player_score = pd.Series(current_highest_player_score).fillna(0).cummax()
    
    series = df_plot.sort_values(by='score', ascending=False).iloc[0]
    score = int(series['score'])
    rnd = int(series['gw'])
    team = series['team']
    owner = series['owner']
    player = series['player']

    current_highest_player_score = list(current_highest_player_score) + (38-len(current_highest_player_score)) * [score]

    p = figure(y_range=Range1d(0, 30, bounds="auto"),
               x_range=Range1d(0, 39, bounds="auto"),
               plot_width=1600, plot_height=1000,
               x_axis_label = 'Game Week',
               y_axis_label = 'Points'
               )
    p.add_layout(Title(text="Each owner's highest scoring player for each gameweek shown",
                       text_font_style="italic"), 'above')
    p.add_layout(Title(text="Current Highest Matchday Score is from Gameweek " + str(rnd) + ", when " + player + " Scored " + str(int(score)) + " Points for " + team + " (" + owner + ")",
                       text_font_style="italic"), 'above')
    p.add_layout(Title(text="Novelty 2 - Highest Player Score", text_font_size="16pt"), 'above')

    # gold line and circles
    p.line(range(1,39), current_highest_player_score, line_width=3, color='#e5c100')
    top_score_highlight_ys = [-1]*(rnd-1)
    top_score_highlight_ys.append(score)
    top_score_highlight_ys = top_score_highlight_ys + [-1]*(38-rnd)
    
    p.circle(range(1,39), top_score_highlight_ys, alpha=1, size=18, color = '#e5c100')
#    p.vbar(x=range(1,39), width=0.5, bottom=0, top=top_score_highlight_ys, color="firebrick")

#    for owner in set(df_plot['owner']):
#    src = ColumnDataSource(df_plot)
#    p.vbar(x='gw', source=src, width=0.5, bottom=0, top='total_points', color="owner_color",
#           legend=owner, muted_color='owner_color', muted_alpha=0.4, name=owner)

    for owner in set(df_plot['owner']):
        src = ColumnDataSource(df_plot[df_plot.owner == owner])
#         p.line? full alpha, but appear pn hover?
#        p.line('gw', 'score', source=src, alpha=0,
#                legend = owner, hover_alpha=0.5, hover_line_color='owner_color', line_width=2)

        p.circle('gw', 'score', source=src, alpha=1, size=13, color = 'owner_color', 
                 legend = owner, muted_color='owner_color', muted_alpha=0.4, name=owner)

    src = ColumnDataSource(df_plot)
    hover = HoverTool(names=list(df_plot['owner'].unique()),
                      tooltips=[('Week', '@gw'),
                                ('Owner', '@owner, @team'),
                                ('Player', '@player'),
                                ('Score', '@score'),
                                ])
    p.add_tools(hover)
    
    crosshair = CrosshairTool()
    p.add_tools(crosshair)

    p.legend.location = (0, 640)
#    p.legend.click_policy = 'mute'
    
    p.title.text_font = 'helvetica'
    
    # Styling
    p = style(p)
    
    return p


#p = make_plot()

#show(p)
#output_file("Fantasy.html")

# -----------------------------------------
#       Main Script
# -----------------------------------------

def novelty2(df_plot):
    
    p = make_plot(df_plot)
            
    # Make a tab with the layout 
    tab = Panel(child=p, title = 'Novelty 2')
    return tab

