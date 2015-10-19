# imports
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import random

# request espn's college bball website and convert to beautiful soup item
r = requests.get('http://espn.go.com/mens-college-basketball/teams')
b = BeautifulSoup(r.text)

# create empty lists and find all links
team_names =[]
id_nums = []
roster_link_ends = []
links = b.findAll(attrs={'class':'bi'})

# append lists with data from links
for i in links:
	team_names.append(str(i.text))
	id_nums.append(re.search(r'(?<=/_/id/)\d+',i['href']).group())
	roster_link_ends.append(re.search(r'(?<=/_/id/).+',i['href']).group())

# check that team_names equals length of id_nums
assert(len(team_names) == len(id_nums))

# create a dictionary containing all of the team names and ids
team_id_dict = {}
for i in range(len(team_names)):
	team_id_dict[team_names[i]] = (id_nums[i],roster_link_ends[i])

# initiate lists and set up base link
l_team_name = []
l_player_name = []
l_player_height = []
l_team_conference = []
roster_base_link = 'http://espn.go.com/mens-college-basketball/team/roster/_/id/'

# loop through team ids, run request & transfer into BeautifulSoup object
# locate player names and heights via "re" module
# append lists with data
for key in team_id_dict:
	roster_link = roster_base_link + team_id_dict[key][1]
	r = requests.get(roster_link)
	b = BeautifulSoup(r.text)
	team_data = b.findAll(attrs={'class':'mod-content'})
	team_data = unicode(team_data[0])
	team_data = team_data.encode('ascii','ignore')
	team_data = re.findall(r'(?<=">)([^<]+)[^\d]+(\d-\d+)',team_data)
	# collect conference data
	conf = b.find(name='div',attrs={'class':'sub-title'})
	conf = conf.text.encode('ascii','ignore')
	for i in team_data:
		l_team_name.append(key)
		l_player_name.append(i[0])
		l_player_height.append(i[1])
		l_team_conference.append(conf)

# load data to DataFrame
df = pd.DataFrame({'player_name':l_player_name,'player_height':l_player_height,'team_name':l_team_name,'team_conference':l_team_conference})

# convert string height to inches height
df['player_height_ft'] = df['player_height'].str.extract('(\d)')
df['player_height_ft'] = df['player_height_ft'].convert_objects(convert_numeric=True)
df['player_height_in'] = df['player_height'].str.extract('(\d+$)')
df['player_height_in'] = df['player_height_in'].convert_objects(convert_numeric=True)
df['player_height_in'] = df['player_height_ft'] * 12 + df['player_height_in']
df = df.drop('player_height_ft', 1)

# folder saving path
folder_path = 'C:/Users/Michael/projects/bball/college_heights/'

# write to csv
df.to_csv(folder_path + 'espn_college_bball_heights_scrape.csv')
