# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 12:14:42 2019

@author: hussl1
"""

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#         Boke hvisualisation MM Fantasy - Lowest Winning Score
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# ==============================================================================
# Chapter 1: Import modules
# ==============================================================================

import pandas as pd
import numpy as np

from bokeh.plotting import figure
from bokeh.models import Range1d, HoverTool, ColumnDataSource, Panel, CrosshairTool, Title


import config



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

    df = df_single_lines[df_single_lines['Result'] == 'W']
    current_lowest_winning_score = []
    for i in range(1,39):
        current_lowest_winning_score.append(df[df['Gameweek'] == i]['Score'].min())
    current_lowest_winning_score = pd.Series(current_lowest_winning_score).cummin().fillna(method='ffill')
    score = current_lowest_winning_score.min()
#    rnd = np.searchsorted(current_lowest_winning_score, current_lowest_winning_score.min()).item() + 1
    rnd = current_lowest_winning_score.idxmin() + 1
    team = df[df['Score']==score]['Team'].iloc[0]
    owner = df[df['Score']==score]['Owner'].iloc[0]

    p = figure(y_range=Range1d(0, 100, bounds="auto"),
               x_range=Range1d(0, 39, bounds="auto"),
               plot_width=1600, plot_height=1000,
               x_axis_label = 'Game Week',
               y_axis_label = 'Points'
               )
    p.add_layout(Title(text="All winning scores shown",
                       text_font_style="italic"), 'above')
    p.add_layout(Title(text="Current Lowest Winning Score is from Gameweek " + str(rnd) + ", when " + team + " (" + owner + ") Scored " + str(int(score)) + " Points",
                       text_font_style="italic"), 'above')
    p.add_layout(Title(text='Novelty 4 - Lowest Winning Score', text_font_size="16pt"), 'above')

    
    p.line(range(1,39), current_lowest_winning_score, line_width=3, color='#e5c100')
    top_score_highlight_ys = [-1]*(rnd-1)
    top_score_highlight_ys.append(score)
    top_score_highlight_ys = top_score_highlight_ys + [-1]*(38-rnd)
    p.circle(range(1,39), top_score_highlight_ys, alpha=1, size=18, color = '#e5c100')

    for owner in set(df['Owner']):
        src = ColumnDataSource(df[df.Owner == owner])
        p.circle('Gameweek', 'Score', source=src, alpha='fill_alpha', size=13, color = 'owner_color', 
                 legend = owner, muted_color='colors', muted_alpha=0.4, name=owner)

        
    src = ColumnDataSource(df)
    hover = HoverTool(names=list(df['Owner'].unique()),
                      tooltips=[('Week', '@Gameweek'),
                                ('Owner', '@Owner, @Team (@Result)'),
                                ('Opposition', '@Opp_Owner, @Opp_Team'),
                                ('Score', '@Score - @Opp_Score'),
                                ])
    p.add_tools(hover)
    
    crosshair = CrosshairTool()
    p.add_tools(crosshair)
    
#    legend = Legend(items=[(fruit, [r]) for (fruit, r) in zip(fruits, rs)], location=(0, 30))
#    p.add_layout(legend, 'right')
    p.legend.location = (0, 660)
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

def novelty4(df_single_lines):
    
    p = make_plot(df_single_lines)
    
    # Make a tab with the layout 
    tab = Panel(child=p, title = 'Novelty 4')
    return tab

