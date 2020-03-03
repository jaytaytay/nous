# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 12:14:42 2019

@author: hussl1
"""

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#         Bokeh visualisation MM Fantasy
# Novelty 1: Highest Round Team Score (excluding double game-weeks).
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# ==============================================================================
# Chapter 1: Import modules
# ==============================================================================

import pandas as pd
#import os
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
def make_plot(df_single_lines):
    # Blank plot with correct labels
    
    current_highest_team_score = []
    for i in range(1,39):
        current_highest_team_score.append(df_single_lines[df_single_lines['Gameweek'] == i]['Score'].max())
    current_highest_team_score = pd.Series(current_highest_team_score).fillna(0).cummax()
    
    score = max(current_highest_team_score)
    rnd = np.searchsorted(current_highest_team_score, pd.Series(current_highest_team_score).max()).item() + 1
    team = df_single_lines[df_single_lines['Score']==score]['Team'].iloc[0]
    owner = df_single_lines[df_single_lines['Score']==score]['Owner'].iloc[0]
    
    current_highest_team_score = list(current_highest_team_score) + (38-len(current_highest_team_score)) * [score]

    p = figure(y_range=Range1d(0, 100, bounds="auto"),
               x_range=Range1d(0, 39, bounds="auto"),
               plot_width=1800, plot_height=1200,
               x_axis_label = 'Game Week',
               y_axis_label = 'Points'
               )
    p.add_layout(Title(text="\nAll individual gameweek scores shown",
                       text_font_style="italic"), 'above')
    p.add_layout(Title(text="Current Highest Gameweek Score is from Gameweek " + str(rnd) + ", when " + team + " (" + owner + ") Scored " + str(int(score)) + " Points",
                       text_font_style="italic"), 'above')    
    p.add_layout(Title(text="Novelty 1 - Highest Gameweek Score", text_font_size="16pt"), 'above')
    
    p.line(range(1,39), current_highest_team_score, line_width=3, color='#e5c100')
    top_score_highlight_ys = [-1]*(rnd-1)
    top_score_highlight_ys.append(score)
    top_score_highlight_ys = top_score_highlight_ys + [-1]*(38-rnd)
    p.circle(range(1,39), top_score_highlight_ys, alpha=1, size=18, color = '#e5c100')

    for owner in set(df_single_lines['Owner']):
        src = ColumnDataSource(df_single_lines[df_single_lines['Owner'] == owner])
        p.circle('Gameweek', 'Score', source=src, alpha='fill_alpha', size='size', color = 'owner_color', 
                 legend = owner, muted_color='owner_color', muted_alpha=0.4, name=owner)

    src = ColumnDataSource(df_single_lines)
    hover = HoverTool(names=list(df_single_lines['Owner'].unique()),
                      tooltips=[('Week', '@Gameweek'),
                                ('Owner', '@Owner, @Team (@Result)'),
                                ('Opposition', '@Opp_Owner, @Opp_Team'),
                                ('Score', '@Score - @Opp_Score'),
                                ])
    p.add_tools(hover)
    
    crosshair = CrosshairTool()
    p.add_tools(crosshair)
    
    p.legend.location = (0, 840)
    p.legend.click_policy = 'mute'
    
    p.title.text_font = 'helvetica'
    
    # Styling
    p = style(p)
    
    return p


# -----------------------------------------
#       Main Script
# -----------------------------------------

def novelty1(df_single_lines):
    
    p = make_plot(df_single_lines)
    
    # Make a tab with the layout 
    tab = Panel(child=p, title = 'Novelty 1')
    return tab

