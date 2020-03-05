
# -----------------------------------------
#     Import stuff
# -----------------------------------------

from flask import Flask, render_template, request
from bokeh.embed import server_document, components

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
@app.route("/novel") #("/melmac/2019-20/novelty_1")
def novel():
	plot = novelty1.make_plot(df_single_lines)
	script, div = components(plot)
	return render_template("/melmac/2019-20/novelty_1.html", the_div=div, the_script=script)

#    2 Highest 1-Game Player Score (Can be 1 game from a double game-week).
#tab2 = novelty2.novelty2(df_novelty_2)

#    3 Highest Losing Score (excluding double game-weeks).
#tab3 = novelty3.novelty3(df_single_lines)

#    4 Lowest Winning Score. 
#tab4 = novelty4.novelty4(df_single_lines)

#    5 Highest Bench Score in a game-week. Bench players  who are auto-subbed on will not count (Players dropped to the bench to "rig" this will be excluded if the league agree).
#tab5 = novelty5.novelty5(df_novelty_5, dict_owners)

#    6 Most wins against the eventual champion.
#tab6 = novelty6.novelty6(df_single_lines)

#    7 Worst First Round Pick (Player score for the season).
#tab7 = novelty7.novelty7(df_pl_past, df_team_info, df_pl_players, dict_owners)

#    8 Most player points from a waiver request/free agent pick-up the week after (Can count 1 game scores from double game-weeks).    
#tab8 = novelty7.novelty7(df_pl_past, df_team_info, df_pl_players, dict_owners)


if __name__ == "__main__":
    app.run(port=5000, debug=True)