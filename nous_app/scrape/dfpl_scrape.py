#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 21:06:22 2018

@author: liam
https://www.analyticsvidhya.com/blog/2015/10/beginner-guide-web-scraping-beautiful-soup-python/
"""
# import libraries
import pandas as pd
import numpy as np
import os

#import urllib.request
#from bs4 import BeautifulSoup
from selenium import webdriver
import time
from timeit import default_timer as timer
import pickle
from io import StringIO
#import sys

import config
import config2

path = os.getcwd()

# specify the url
def scrape_fixtures():
    
    # scrape
    ## NOTE TO FUTURE LIAM
    ## This is working well. Scraping all fixtures and links to individual matchups.
    ## look to extend this to collect lineups (and store these in the liast_seasons[round] dataframes?)
    ## could investigate scheduling this to only scrape this round? or not to scrape old rounds? or rounds to far in future?
    
    driver = webdriver.Chrome(confgi.chrome_driver)
    df_results = pd.DataFrame(columns=['home_team','home_owner','away_team','away_owner','score','href'])
    function_start = timer()
    for i in range(1, 30):
        urlpage = 'https://draftfantasyfootball.co.uk/league/started/HmeqQ3SqxHMSBnA5y/team/J996wRPcDekXEbooB/gameweek/' + str(i)
        driver.get(urlpage)
#        time.sleep(10) # Let the user actually see something!
        locator = '//*[@id="wrapper"]/div[2]/div/div[1]/div/div[4]/table'

        start = timer()
        end = timer()
        duration = end - start  # time in seconds
        
        list_home_teams= []
        list_home_owners= []
        list_away_teams= []
        list_away_owners= []
        list_scores = []
        list_hrefs = []
        df = pd.DataFrame()
        
        while duration < 30:
            try:
                for row in range(0,8):
                    if row%2 == 0:
                        list_home_teams.append(driver.find_element_by_xpath(locator).find_elements_by_tag_name('div')[row].get_attribute('innerHTML'))
                        list_hrefs.append(driver.find_element_by_xpath(locator).find_elements_by_tag_name('a')[int(row/2)].get_attribute('href'))
                        list_home_owners.append(driver.find_element_by_xpath(locator).find_elements_by_tag_name('strong')[row].get_attribute('innerHTML'))    
                        list_scores.append(driver.find_element_by_xpath(locator).find_elements_by_class_name('text-center')[int(row)].get_attribute('innerHTML'))
                    else:
                        list_away_teams.append(driver.find_element_by_xpath(locator).find_elements_by_tag_name('div')[row].get_attribute('innerHTML'))
                        list_away_owners.append(driver.find_element_by_xpath(locator).find_elements_by_tag_name('strong')[row].get_attribute('innerHTML'))    
                
                df = pd.DataFrame(list(zip(list_home_teams, list_home_owners, list_away_teams, list_away_owners, list_scores, list_hrefs)), \
                                  columns=['home_team','home_owner','away_team','away_owner','score','href'])
                df['gw'] = i
                    
                df_results = pd.concat([df_results, df])
                    
                end = timer()
                duration = end - start  # time in seconds
                print('Round ' + str(i) + ' fixtures successfully scraped in ' + str(round(duration, 2)) + ' seconds')
                break
            except:
                time.sleep(0.1)
            end = timer()
            duration = end - start
            
        if len(df) < 1:
            print("Fixture scrape failed on round " + str(i))
            driver.quit()
            exit()
        
    end = timer()
    duration = end - function_start  # time in seconds
    print('All fixtures successfully scraped in ' + str(round(duration, 2)) + ' seconds')

    driver.quit()    
    
    df_results.reset_index(inplace=True,drop=True)
    
    # Reformat
        # Split owners and teams
    def string_split(old_string):
        comma   = old_string.rfind(",")
        team    = old_string[:comma]
        owner   = old_string[comma+1:]
        return team, owner
    
    def split_score(old_score):
        dash   = old_score.rfind("-")
        home   = old_score[:dash-1]
        away   = old_score[dash+1:]
        return home, away
    
    for row in range(0,len(df_results)):
        df_results.loc[row,'home_score'], df_results.loc[row,'away_score'] = split_score(df_results.loc[row,'score'])    
    
    dict_owners = {
                'Matt Lowry':       {'team': "Ol' Cider's Lowry",             'first_round_pick': 253,    'Colour':'#ffe6d2'},
                'Dylan Urquhart':   {'team': 'Heung like Son',                'first_round_pick': 270,    'Colour':'#cc66cc'},
                'james west':       {'team': 'best in the west',              'first_round_pick': 273,    'Colour':'#ffb400'},
                'Peter Allan':      {'team': 'Wizards of Ozil',               'first_round_pick': 23,     'Colour':'#c73b32'},
                'Liam Fariss':      {'team': 'Corner taken quickly, ORIGIII!','first_round_pick': 22,     'Colour':'#32b4ff'},
                'Liam Hussey':      {'team': 'The Feminist Agenda',           'first_round_pick': 280,    'Colour':'#995f3d'},
                'Tom Barratt':      {'team': "Ain't No Holebas Girl",         'first_round_pick': 251,    'Colour':'#0ac832'},
                'Dominic Drewery':  {'team': 'Chopporoos',                    'first_round_pick': 372,    'Colour':'#1e2832'}
                }
    
    df_single_lines = pd.DataFrame(columns=['team', 'opp_team', 'owner', 'opp_owner', 'score', 'opp_score', 'gw', 'result', 'url', 'home'])
    
    j=0
    for i in range(0, len(df_results)):
        df_single_lines.loc[j] = [np.nan for n in range(df_single_lines.shape[1])]
        df_single_lines.loc[j, 'team']      = df_results.loc[i, 'home_team'].strip()
        df_single_lines.loc[j, 'opp_team']  = df_results.loc[i, 'away_team'].strip()
        df_single_lines.loc[j, 'owner']     = df_results.loc[i, 'home_owner'].strip()
        df_single_lines.loc[j, 'opp_owner'] = df_results.loc[i, 'away_owner'].strip()
        df_single_lines.loc[j, 'score']     = df_results.loc[i, 'home_score'].strip()
        df_single_lines.loc[j, 'opp_score'] = df_results.loc[i, 'away_score'].strip()
        df_single_lines.loc[j, 'gw']  = df_results.loc[i, 'gw']
        df_single_lines.loc[j, 'href']       = df_results.loc[i, 'href']
        df_single_lines.loc[j, 'home']      = True
      
        if df_single_lines.loc[j, 'score'] > df_single_lines.loc[j, 'opp_score']:
            df_single_lines.loc[j, 'result'] = 'W'
        elif df_single_lines.loc[j, 'score'] < df_single_lines.loc[j, 'opp_score']:
            df_single_lines.loc[j, 'result'] = 'L'
        else:
            df_single_lines.loc[j, 'result'] = 'D'
        
        j+=1
        
        df_single_lines.loc[j] = [np.nan for n in range(df_single_lines.shape[1])]
        df_single_lines.loc[j, 'team']      = df_results.loc[i, 'away_team'].strip()
        df_single_lines.loc[j, 'opp_team']  = df_results.loc[i, 'home_team'].strip()
        df_single_lines.loc[j, 'owner']     = df_results.loc[i, 'away_owner'].strip()
        df_single_lines.loc[j, 'opp_owner'] = df_results.loc[i, 'home_owner'].strip()
        df_single_lines.loc[j, 'score']     = df_results.loc[i, 'away_score'].strip()
        df_single_lines.loc[j, 'opp_score'] = df_results.loc[i, 'home_score'].strip()
        df_single_lines.loc[j, 'gw']  = df_results.loc[i, 'gw']
        df_single_lines.loc[j, 'href']       = df_results.loc[i, 'href']
        df_single_lines.loc[j, 'home']      = False
        
        if df_single_lines.loc[j, 'score'] > df_single_lines.loc[j, 'opp_score']:
            df_single_lines.loc[j, 'result'] = 'W'
        elif df_single_lines.loc[j, 'score'] < df_single_lines.loc[j, 'opp_score']:
            df_single_lines.loc[j, 'result'] = 'L'
        else:
            df_single_lines.loc[j, 'result'] = 'D'

        j+=1
        
    colormap = {'L': 'red', 'W': 'green', 'D': 'blue'}
    colors = [colormap[x] for x in df_single_lines['result']]
    df_single_lines['colors'] = colors
    df_single_lines['fill_alpha'] = 1
    df_single_lines['size'] = 11
    df_single_lines['line_width'] = 2

    df_owners = pd.DataFrame.from_dict(dict_owners).T
    dict_colors = df_owners['Colour'].to_dict()
    
#     # owners have leading whitespace...
# #    df_single_lines['owner'] = df_single_lines['owner'].str.strip()
    df_single_lines['score'] = pd.to_numeric(df_single_lines['score'])
    df_single_lines['opp_score'] = pd.to_numeric(df_single_lines['opp_score'])
    # df_single_lines['gw'] = pd.to_numeric(df_single_lines['gw'])

#sort to order legend as W-L-D
    df_single_lines = df_single_lines.sort_values('result', ascending = False)
        
    df_single_lines['owner_color'] = df_single_lines['owner'].map(dict_colors)

    # Export
    df_single_lines.to_csv(config.path_results)
#    pickle.dump(df_results, open(config.path_results_pickle_write, "wb"))


def scrape_transfers():
    
    # need to log in to get transfers...
    driver = webdriver.Chrome('/usr/local/bin/chromedriver')    
    urlpage = 'https://draftfantasyfootball.co.uk/sign-in'
    driver.get(urlpage)
    time.sleep(5)

    user = config2.draft_username
    password = config2.draft_password
    
    user_id = 'at-field-email'
    password_id = 'at-field-password'
    login_button = '//*[@id="at-btn"]'
    login_button = 'at-btn'
    
    driver.find_elements_by_id(user_id)[0].send_keys(user)
    time.sleep(0.5)
    driver.find_elements_by_id(password_id)[0].send_keys(password)
    time.sleep(0.7)
    driver.find_elements_by_id(login_button)[0].click()
    time.sleep(5) 
    # now we are logged in, scrape transfers       
    urlpage = 'https://draftfantasyfootball.co.uk/transfers/J996wRPcDekXEbooB'
    driver.get(urlpage)
    time.sleep(10)
    
    #need to click on History to select transfer history
    history_button = '//*[@id="wrapper"]/div[2]/div[2]/div[1]/ul/li[3]'
    driver.find_elements_by_xpath(history_button)[0].click()
    time.sleep(2)
    
    
    #need to click on View All
    viewall_button = '//*[@id="viewMore"]'
    driver.find_elements_by_xpath(viewall_button)[0].click()
    time.sleep(2)

    locator = '//*[@id="wrapper"]/div[2]/div[2]/div[2]/div/div/table'
    transfer_table = driver.find_element_by_xpath(locator).get_attribute('outerHTML')
    df_transfers = pd.read_html(transfer_table)
    df_transfers = df_transfers[0]

    driver.quit()

    df_transfers.to_csv(config.path_transfers)

    
def scrape_teams():
    
    function_start = timer()
    start = timer()
    end = timer()
    duration = end - start  # time in seconds

    df_results = pd.read_csv(config.path_results)
    
    list_season = []

    driver = webdriver.Chrome(config.chrome_driver)
    data_view_button = '//*[@id="wrapper"]/div[2]/div/div[3]/div/ul/li[2]' 
    for row in range(0, len(df_results)):
        round_check = False  # initialise
        start = timer()
        end = timer()
        duration = end - start  # time in seconds
        
        list_lineup = []

        driver.get(df_results.loc[row, 'href'])
        while duration < 30:
            try:
                driver.find_elements_by_xpath(data_view_button)[0].click()
                end = timer()
                duration = end - start  # time in seconds
                print('Button clicked successfully in ' + str(round(duration, 2)) + ' seconds')
                break
            except:
                time.sleep(0.1)
                end = timer()
                duration = end - start  # time in seconds
                
#        home_table_xpath = '//*[@id="wrapper"]/div[2]/div/div[4]/div[1]/div/div/div/div'
        home_table_xpath = '//*[@id="wrapper"]/div[2]/div/div[4]/div[1]/div/div/div[1]'        
    
        while duration < 60:
            try:
                if df_results.loc[row, 'home']:
                    home_lineup = StringIO(driver.find_elements_by_xpath(home_table_xpath)[0].text)
                    df = pd.read_csv(home_lineup, sep="\n")
                    df = df.drop([0,1,2,58,59,60,61], axis=0).reset_index(drop=True)
                    df_home = pd.DataFrame(columns = ['position',
                                                       'player',
                                                       'team',
                                                       'gw_score',
                                                       'season_score'])
                    df_home['position']     = df[df.index%5==0].reset_index(drop=True)['Lineup']
                    df_home['player']       = df[df.index%5==1].reset_index(drop=True)['Lineup']
                    df_home['team']         = df[df.index%5==2].reset_index(drop=True)['Lineup']
                    df_home['gw_score']     = df[df.index%5==3].reset_index(drop=True)['Lineup']
                    df_home['season_score'] = df[df.index%5==4].reset_index(drop=True)['Lineup']
                    df_home['bench']        = False
                    df_home.loc[11:,'bench']= True
    
                    list_lineup.append(df_home)
                    
                    list_data = [df_results.loc[row,'owner'],
                                 df_results.loc[row,'team'],
                                 df_results.loc[row,'gw']]
                    list_lineup.append(list_data)
    
                    list_season.append(list_lineup)
                    list_lineup = []
                else:
                    away_table_xpath = '//*[@id="wrapper"]/div[2]/div/div[4]/div[2]/div/div/div[1]'
                    away_lineup = StringIO(driver.find_elements_by_xpath(away_table_xpath)[0].text)
                    df = pd.read_csv(away_lineup, sep="\n")
                    df = df.drop([0,1,2,58,59,60,61], axis=0).reset_index(drop=True)
                    df_away = pd.DataFrame(columns = ['position',
                                                       'player',
                                                       'team',
                                                       'gw_score',
                                                       'season_score'])
                    df_away['position']     = df[df.index%5==0].reset_index(drop=True)['Lineup']
                    df_away['player']       = df[df.index%5==1].reset_index(drop=True)['Lineup']
                    df_away['team']         = df[df.index%5==2].reset_index(drop=True)['Lineup']
                    df_away['gw_score']     = df[df.index%5==3].reset_index(drop=True)['Lineup']
                    df_away['season_score'] = df[df.index%5==4].reset_index(drop=True)['Lineup']
                    df_away['bench']        = False
                    df_away.loc[11:,'bench']= True
    
                    list_lineup.append(df_away)
                    
                    list_data = [df_results.loc[row,'owner'],
                                 df_results.loc[row,'team'],
                                 df_results.loc[row,'gw']]
                    list_lineup.append(list_data)
                    
                    list_season.append(list_lineup)
                    
                round_check = True
                break
            
            except:
                time.sleep(0.1)
                end = timer()
                duration = end - start
                
            
        if not round_check:
            print('FAILURE! Scrape probably timed out...')
            exit

        end = timer()
        duration = end - start  # time in seconds
        total_duration = end - function_start
        print('Match ' + str(row+1) + ' lineups successfully scraped in ' + str(round(duration, 2)) + ' seconds\n    ' + \
               str(round((row+1)*100/(len(df_results)+1),1)) + '% complete. Total time: ' + str(round(total_duration,2)) + ' seconds\n    ' + \
               str(round((total_duration/((row+1)/(len(df_results)+1)))-total_duration,0)) + ' seconds to go')

    end = timer()
    duration = end - function_start  # time in seconds
    print('All lineups successfully scraped in ' + str(round(duration, 2)) + ' seconds')

    driver.quit()
    
    # make a dataframe for each owner, with 2 cols: player and gw owned, listing each player that was in their team for each gw.
    for i in range(0,len(list_season)):
        df_lineup = list_season[i][0]
        list_data = list_season[i][1]
        
        df_lineup['owner']   = list_data[0]
        df_lineup['team']    = list_data[1]
        df_lineup['gw']      = list_data[2]
        
        if i == 0:
            df_all_players = df_lineup
        else:
            df_all_players = pd.concat([df_all_players,df_lineup], ignore_index=True)    

    df_all_players.to_csv(config.path_lineups)
#    pickle.dump(list_season, open(config.path_lineups_pickle_write, "wb"))
#    df_lineups = pickle.load(open(path_lineups_pickle, 'rb'))

 
def novelty_5_structure():
    
    df_all_players = pd.read_csv(config.path_lineups)
    df_all_players['gw_score'] = pd.to_numeric(df_all_players['gw_score'])

    df_all_players = df_all_players[df_all_players['bench'] == True]

    df_benches = df_all_players.groupby(['gw', 'owner'])['gw_score'].sum()
    
    df_benches.to_csv(config.path_novelty_5)
#    df_benches.to_csv('/Users/JohnTaylor/Dropbox/Public/kyso/novelty_5.csv')
    
    #----------------------------------------------
    # comments
    #----------------------------------------------
def novelty_2_structure():
    # Need to match website's player names with the database's player names/IDs. use fuzzy string to build a dictionary for each of the 
    # players scraped from the website, then map back to database
    
    from fuzzywuzzy import fuzz
    
    df_lineups      = pd.read_csv(config.path_lineups)
    df_pl_players   = pd.read_csv(config.path_pl_players, encoding='latin1')
    df_pl_past      = pd.read_csv(config.path_pl_past)  # df_gw_data

    dict_owners = config.dict_owners
    
    def fuzzy_string_match(df_uniques, string, season_score):
        
#        df_gw_data['ratio']            = df_gw_data['friendly_name'].apply(lambda x: fuzz.ratio(x.lower(), string.lower()))
        df_uniques['partial_ratio']    = df_uniques['friendly_name'].apply(lambda x: fuzz.partial_ratio(x.lower(),string.lower()))
#        df_gw_data['token_sort_ratio'] = df_gw_data['friendly_name'].apply(lambda x: fuzz.token_sort_ratio(x.lower(),string.lower()))
#        df_gw_data['token_set_ratio']  = df_gw_data['friendly_name'].apply(lambda x: fuzz.token_set_ratio(x.lower(),string.lower()))
#        df_gw_data['fuzzy_sum'] = df_gw_data['ratio'] + df_gw_data['partial_ratio'] + df_gw_data['token_sort_ratio'] + df_gw_data['token_set_ratio']
        print('.')
        df = df_uniques[df_uniques['total_points']==season_score]
        return df.sort_values('partial_ratio', ascending=False).reset_index(drop=True).loc[0,'id']

    df_uniques = df_pl_players[['id', 'friendly_name', 'total_points']].drop_duplicates()
    df_to_be_matched = pd.DataFrame(df_lineups[['player', 'season_score']].drop_duplicates()).reset_index(drop=True)
    
    # fuzzy text match was returning incorrect matches, thertefore included season score filter. 
    for i in range(0, len(df_to_be_matched)):
        df_to_be_matched.loc[i, 'player_id'] = fuzzy_string_match(df_uniques, df_to_be_matched.loc[i, 'player'], df_to_be_matched.loc[i, 'season_score'])
    
    df_to_be_matched = df_to_be_matched.set_index('player')
    df_to_be_matched = df_to_be_matched.drop('season_score', axis=1)
    dict_dfpl_players = df_to_be_matched['player_id'].to_dict()
    df_lineups['player_id'] = df_lineups['player'].map(dict_dfpl_players)
    
    # go through all 8 dfs, listing each players ROUND scores for the corresponging GWs
    df_rnd_gw_player = df_pl_past[['round', 'player_id', 'total_points', 'fixture', 'friendly_name']]
    df_lineups = pd.merge(df_lineups, df_rnd_gw_player, how='inner', left_on=['gw','player_id'], right_on=['round','player_id'])    
    
#    list_plot = []
#    for i in range(1, df_lineups.gw.max()+1):
#        list_plot.append(df_lineups[df_lineups['gw']==i].sort_values('total_points', ascending=False).reset_index(drop=True).iloc[0])
#    df_plot = pd.DataFrame(list_plot)
#    
    row = 0
    df_plot = pd.DataFrame()
    for owner in list(set(df_lineups['owner'])):
        df = df_lineups[df_lineups['owner']==owner]
        for gw in range(1, int(df_lineups['gw'].max()+1)):
            series = df[df['gw']==gw].sort_values(by='gw_score', ascending=False).iloc[0]
            df_plot.loc[row,'score']    = series['gw_score']
            df_plot.loc[row,'player']   = series['friendly_name']
            df_plot.loc[row,'gw']       = gw
            df_plot.loc[row,'owner']    = series['owner']
            df_plot.loc[row,'team']     = series['team']
            row +=1
    
    df_owners = pd.DataFrame.from_dict(dict_owners).T
    dict_team_colors = df_owners['Colour'].to_dict()
    df_plot['owner_color'] = df_plot['owner'].map(dict_team_colors)

    df_plot.to_csv(config.path_novelty_2)
#    df_plot.to_csv('/Users/JohnTaylor/Dropbox/Public/kyso/novelty_2.csv')


