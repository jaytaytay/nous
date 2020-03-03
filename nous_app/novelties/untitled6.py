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
def make_plot(df_novelty_5, dict_owners):
    # Blank plot with correct labels

    df_novelty_5 = df_novelty_5.reset_index(level=0, drop=False).reset_index(level=0, drop=False)
    df_novelty_5['team'] = df_novelty_5['owner'].map(dict_owners).apply(lambda x: x['Team'])
    df_novelty_5['owner_colour'] = df_novelty_5['owner'].map(dict_owners).apply(lambda x: x['Colour'])
    
    current_highest_bench_score = []
    for i in range(1,39):
        current_highest_bench_score.append(df_novelty_5[df_novelty_5['gw'] == i]['gw_score'].max())

    score = max(current_highest_bench_score)
#    rnd = np.searchsorted(current_highest_bench_score, pd.Series(current_highest_bench_score).max()).item() + 1
    team = df_novelty_5[df_novelty_5['gw_score']==score]['team'].iloc[0]
    owner = df_novelty_5[df_novelty_5['gw_score']==score]['owner'].iloc[0]

    gold_line = pd.Series(current_highest_bench_score).cummax().fillna(score)
    rnd = gold_line.idxmin()+1

    p = figure(y_range=Range1d(0, 40, bounds="auto"),
               x_range=Range1d(0, 39, bounds="auto"),
               plot_width=1600, plot_height=1000,
               x_axis_label = 'Game Week',
               y_axis_label = 'Points'
               )
    p.add_layout(Title(text="All owners' bench scores shown",
                       text_font_style="italic"), 'above')
    p.add_layout(Title(text="Current Highest Bench Score is from Gameweek " + str(rnd) + ", when " + team + " (" + owner + ") Scored " + str(int(score)) + " Points",
                       text_font_style="italic"), 'above')
    p.add_layout(Title(text="Novelty 5 - Highest Bench Score", text_font_size="16pt"), 'above')

    p.line(range(1,39), gold_line, line_width=3, color='#e5c100')
    top_score_highlight_ys = [-1]*(rnd-1)
    top_score_highlight_ys.append(score)
    top_score_highlight_ys = top_score_highlight_ys + [-1]*(38-rnd)
    p.circle(range(1,39), top_score_highlight_ys, alpha=1, size=18, color = '#e5c100')

    df_novelty_5 = df_novelty_5.drop(['index','level_0'], axis=1)

    for owner in set(df_novelty_5['owner']):
        src = ColumnDataSource(df_novelty_5[df_novelty_5['owner'] == owner])
        p.circle('gw', 'gw_score', source=src, alpha=1, size=11, color = 'owner_colour', 
                 legend = owner, muted_color='owner_colour', muted_alpha=0.4, name=owner)

        
    src = ColumnDataSource(df_novelty_5)
    hover = HoverTool(names=list(df_novelty_5['owner'].unique()),
                      tooltips=[('Week', '@gw'),
                                ('Owner', '@owner, @team'),
                                ('Score', '@gw_score'),
                                ])
    p.add_tools(hover)
    
    crosshair = CrosshairTool()
    p.add_tools(crosshair)
    
    p.legend.location = (0,630)
    p.legend.click_policy = 'mute'
    
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

def novelty5(df_novelty_5, dict_owners):
    
    p = make_plot(df_novelty_5, dict_owners)
    
    # Make a tab with the layout 
    tab = Panel(child=p, title = 'Novelty 5')
    return tab

