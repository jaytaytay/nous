
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
df_novelty_5    = pd.read_csv(config.path_novelty_5, header=0)

dict_owners = config.dict_owners

##########################################
#          Build app
##########################################

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index_2.html")

@app.route("/home")
def home():
	return render_template("index_2.html")

@app.route("/soccer")
def soccer():
	return render_template("soccer.html")

@app.route("/soccer/fantasy")
def soccer_fantasy():
	return render_template("soccer/fantasy.html")

@app.route("/soccer/fantasy/novelties")
def novelties():
	nov_1_plot, nov_1_text = novelty1.make_plot(df_single_lines)
	nov_1_script, nov_1_div = components(nov_1_plot)

	nov_2_plot, nov_2_text = novelty2.make_plot(df_novelty_2)
	nov_2_script, nov_2_div = components(nov_2_plot)

	nov_3_plot, nov_3_text = novelty3.make_plot(df_single_lines)
	nov_3_script, nov_3_div = components(nov_3_plot)

	nov_4_plot, nov_4_text = novelty4.make_plot(df_single_lines)
	nov_4_script, nov_4_div = components(nov_4_plot)

	nov_5_plot, nov_5_text = novelty5.make_plot(df_novelty_5, dict_owners)
	nov_5_script, nov_5_div = components(nov_5_plot)

	nov_6_table, nov_6_text = novelty6.novelty6(df_single_lines)

	nov_7_plot, nov_7_table, nov_7_text = novelty7.novelty7(df_pl_past, df_team_info, df_pl_players, dict_owners)
	nov_7_plot_script, nov_7_plot_div = components(nov_7_plot)
	nov_7_table_script, nov_7_table_div = components(nov_7_table)

	return render_template("/soccer/fantasy/novelties_1920.html", \
		nov_1_div=nov_1_div, nov_1_script=nov_1_script, nov_1_text=nov_1_text, \
		nov_2_div=nov_2_div, nov_2_script=nov_2_script, nov_2_text=nov_2_text, \
		nov_3_div=nov_3_div, nov_3_script=nov_3_script, nov_3_text=nov_3_text, \
		nov_4_div=nov_4_div, nov_4_script=nov_4_script, nov_4_text=nov_4_text, \
		nov_5_div=nov_5_div, nov_5_script=nov_5_script, nov_5_text=nov_5_text, \
		nov_6_table=[nov_6_table.to_html(classes='nov_6', header="true")], nov_6_text=nov_6_text, \
		nov_7_plot_div=nov_7_plot_div, nov_7_plot_script=nov_7_plot_script, \
		nov_7_table_div=nov_7_table_div, nov_7_table_script=nov_7_table_script, nov_7_text=nov_7_text)

if __name__ == "__main__":
	app.run(host='0.0.0.0')