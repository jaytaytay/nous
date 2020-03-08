
# -----------------------------------------
#     Import stuff
# -----------------------------------------

from flask import Flask, render_template, request
from bokeh.embed import server_document, components

import pandas as pd

import sys
import os

from nous_app.novelties import novelty1 as novelty1
from nous_app.novelties import novelty2 as novelty2
from nous_app.novelties import novelty3 as novelty3
from nous_app.novelties import novelty4 as novelty4
from nous_app.novelties import novelty5 as novelty5
from nous_app.novelties import novelty6 as novelty6
from nous_app.novelties import novelty7 as novelty7

import config

from bokeh.models.widgets import Tabs
from bokeh.io import curdoc

# -----------------------------------------
#       files
# -----------------------------------------
path                = os.getcwd()
sys.path.append(path)

dirpath             = os.path.dirname(path)

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
#          Build app
##########################################

app = Flask(__name__)

@app.route("/")
def index():
	name = request.args.get("name")
	if name == None:
		name = "Edward"
	return render_template("index.html", name=name)

    # -----------------------------------------
    #       Performance
    # -----------------------------------------

    # -----------------------------------------
    #       Novelties
    # -----------------------------------------

#    1. Highest Round Team Score (excluding double game-weeks).
@app.route("/melmac/2019-20/novelty_1")
def novelty_1():
	plot = novelty1.make_plot(df_single_lines)
	script, div = components(plot)
	return render_template("/melmac/2019-20/novelty_1.html", the_div=div, the_script=script)

#    2 Highest 1-Game Player Score (Can be 1 game from a double game-week).
@app.route("/melmac/2019-20/novelty_2")
def novelty_2():
	plot = novelty2.make_plot(df_novelty_2)
	script, div = components(plot)
	return render_template("/melmac/2019-20/novelty_1.html", the_div=div, the_script=script)

#    3 Highest Losing Score (excluding double game-weeks).
@app.route("/melmac/2019-20/novelty_3")
def novelty_3():
	plot = novelty3.make_plot(df_single_lines)
	script, div = components(plot)
	return render_template("/melmac/2019-20/novelty_1.html", the_div=div, the_script=script)

#    4 Lowest Winning Score. 
@app.route("/melmac/2019-20/novelty_4")
def novelty_4():
	plot = novelty4.make_plot(df_single_lines)
	script, div = components(plot)
	return render_template("/melmac/2019-20/novelty_1.html", the_div=div, the_script=script)

#    5 Highest Bench Score in a game-week. Bench players  who are auto-subbed on will not count (Players dropped to the bench to "rig" this will be excluded if the league agree).
@app.route("/melmac/2019-20/novelty_5")
def novelty_5():
	plot = novelty5.make_plot(df_novelty_5, dict_owners)
	script, div = components(plot)
	return render_template("/melmac/2019-20/novelty_1.html", the_div=div, the_script=script)

#    6 Most wins against the eventual champion.
@app.route("/melmac/2019-20/novelty_6")
def novelty_6():
	plot = novelty6.novelty6(df_single_lines)
	script, div = components(plot)
	return render_template("/melmac/2019-20/novelty_1.html", the_div=div, the_script=script)

#    7 Worst First Round Pick (Player score for the season).
@app.route("/melmac/2019-20/novelty_7")
def novelty_7():
	plot = novelty7.novelty7(df_pl_past, df_team_info, df_pl_players, dict_owners)
	script, div = components(plot)
	return render_template("/melmac/2019-20/novelty_1.html", the_div=div, the_script=script)
	
#    8 Most player points from a waiver request/free agent pick-up the week after (Can count 1 game scores from double game-weeks).    
#tab8 = novelty7.novelty7(df_pl_past, df_team_info, df_pl_players, dict_owners)


if __name__ == "__main__":
	app.run(host='0.0.0.0')