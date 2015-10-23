# imports
import requests
import pandas as pd 
import numpy as np 
from bs4 import BeautifulSoup
from matplotlib import pyplot
import re

# link set up
team_link_start = 'http://www.basketball-reference.com/teams/'
team_link_end = '/2015.html'

# create dictionary of teams and link values
teams = {'Toronto Raptors':'TOR','Boston Celtics':'BOS',
	'Brooklyn Nets':'BRK','Phildelphia 76ers':'PHI',
	'New York Knicks':'NYK','Cleveland':'CLE',
	'Chicago Bulls':'CHI','Milwaukee Bucks':'MIL',
	'Indiana Pacers':'IND','Detroit Pistons':'DET',
	'Atlanta Hawks':'ATL','Washington Wizards':'WAS',
	'Miami Heat':'MIA','Charlotte Hornets':'CHO',
	'Orlando Magic':'ORL','Portland Trail Blazers':'POR',
	'Oklahoma City Thunder':'OKC','Utah Jazz':'UTA',
	'Denver Nuggests':'DEN','Minnesota Timberwolves':'MIN',
	'Golden State Warriors':'GSW','Los Angeles':'LAC',
	'Phoenix Suns':'PHO','Sacremento Kings':'SAC',
	'Los Angeles Lakers':'LAL','Houston Rockets':'HOU',
	'San Antonio Spurs':'SAS','Memphis Grizzlies':'MEM',
	'Dallas Mavericks':'DAL','New Orleans Pelicans':'NOP'}

# initiate dictionary & list
team_roster = {'Team':None,'No.':None,'Player':None,'Pos':None,'Ht':None,
	'Wt':None, 'Birth_Date':None,'Exp':None,'College':None}
rosters = []
team_stats = {'Team':None,'Player':None,'Age':None,'G':None,'GS':None,
	'MP':None,'FG':None,'FGA':None,'FG_PCT':None,'FG3':None,'FG3A':None,
	'FG3_PCT':None,'FG2':None,'FG2A':None,'FG2_PCT':None,'EFG_PCT':None,
	'FT':None,'FTA':None,'FT_PCT':None,'ORB':None,'DRB':None,'TRB':None,
	'AST':None,'STL':None,'BLK':None,'TOV':None,'PF':None,'PTS':None}
stats = []

# loop through dictionary of teams
for i in teams:

	#initiate player list
	player_list = []

	# request website and turn into beautiful soup object
	r = requests.get(team_link_start + teams[i] + team_link_end)
	b = BeautifulSoup(r.text)

	# create list of player names
	roster_ = b.findAll(name = 'div',attrs={'id':'div_roster'})
	roster_href = roster_[0].findAll('a')
	for j in roster_href:
		match = re.search(r'(?<=.html">).+(?=</a>)',unicode(j).encode('ascii','ignore'))
		if match:
			player_list.append(match.group())

	# scrape roster details for each player on the team
	roster_text = roster_[0].text.encode('ascii','ignore').split('\n')
	for k in player_list:
		place = roster_text.index(k)
		team_roster['Team'] = teams[i]
		team_roster['No'] = roster_text[place - 1]
		team_roster['Player'] = roster_text[place]
		team_roster['Pos'] = roster_text[place + 1]
		team_roster['Ht'] = roster_text[place + 2]
		team_roster['Wt'] = roster_text[place + 3]
		team_roster['Birth_Date'] = roster_text[place + 4]
		team_roster['Exp'] = roster_text[place + 5]
		team_roster['College'] = roster_text[place + 6]
		rosters.append(team_roster.copy())

	# scrape season total stats
	stat_ = b.findAll(name='div',attrs={'id':'div_totals'})
	stat_text = stat_[0].text.encode('ascii','ignore').split('\n')
	for a in player_list:
		place = stat_text.index(a)
		team_stats['Team'] = teams[i]
		team_stats['Player'] = stat_text[place]
		team_stats['Age'] = stat_text[place + 1]
		team_stats['G'] = stat_text[place + 2]
		team_stats['GS'] = stat_text[place + 3]
		team_stats['MP'] = stat_text[place + 4]
		team_stats['FG'] = stat_text[place + 5]
		team_stats['FGA'] = stat_text[place + 6]
		team_stats['FG_PCT'] = stat_text[place + 7]
		team_stats['FG3'] = stat_text[place + 8]
		team_stats['FG3A'] = stat_text[place + 9]
		team_stats['FG3_PCT'] = stat_text[place + 10]
		team_stats['FG2'] = stat_text[place + 11]
		team_stats['FG2A'] = stat_text[place + 12]
		team_stats['FG2_PCT'] = stat_text[place + 13]
		team_stats['EFG_PCT'] = stat_text[place + 14]
		team_stats['FT'] = stat_text[place + 15]
		team_stats['FTA'] = stat_text[place + 16]
		team_stats['FT_PCT'] = stat_text[place + 17]
		team_stats['ORB'] = stat_text[place + 18]
		team_stats['DRB'] = stat_text[place + 19]
		team_stats['TRB'] = stat_text[place + 20]
		team_stats['AST'] = stat_text[place + 21]
		team_stats['STL'] = stat_text[place + 22]
		team_stats['BLK'] = stat_text[place + 23]
		team_stats['TOV'] = stat_text[place + 24]
		team_stats['PF'] = stat_text[place + 25]
		team_stats['PTS'] = stat_text[place + 26]
		stats.append(team_stats.copy())

# turn roster list into DataFrame
cols = ['Team','No','Player','Pos','Ht','Wt','Birth_Date','Exp','College']
roster_df = pd.DataFrame(rosters,columns = cols)

# convert string ht to inches ht
roster_df['ht_ft'] = roster_df['Ht'].str.extract('(\d)')
roster_df['ht_ft'] = roster_df['ht_ft'].convert_objects(convert_numeric=True)
roster_df['ht_in'] = roster_df['Ht'].str.extract('(\d+$)')
roster_df['ht_in'] = roster_df['ht_in'].convert_objects(convert_numeric=True)
roster_df['ht_in'] = roster_df['ht_ft'] * 12 + roster_df['ht_in']
roster_df = roster_df.drop('ht_ft', 1)

# turn stats list into DataFrame
cols2 = ['Team','Player','Age','G','GS',
	'MP','FG','FGA','FG_PCT','FG3','FG3A',
	'FG3_PCT','FG2','FG2A','FG2_PCT','EFG_PCT',
	'FT','FTA','FT_PCT','ORB','DRB','TRB',
	'AST','STL','BLK','TOV','PF','PTS']
stats_df = pd.DataFrame(stats,columns = cols2) 
stats_df['Age'] = stats_df['Age'].convert_objects(convert_numeric=True)

# merge dataframe together
total_df = pd.merge(roster_df,stats_df,on=['Team','Player'],how='left')

# folder saving path
folder_path = 'C:/Users/Michael/projects/bball/nba_rosters_15/'

# write to csv
total_df.to_csv(folder_path + 'b_r_nba_heights_scrape.csv')

