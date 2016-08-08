# Two classes for scraping NHL rosters for the 2015-2016 season
# The first class parses the HTML from the on-line game-by-game rosters
# The second class builds the roster table and saves


import numpy as np
import pandas as pd
from HTMLParser import HTMLParser as HP
import requests

# There were 1230 games in the season

GameKeys = range(0,1230)

# Class to parse the HTML. Most of the code is pretty tedious

class RosterParse(HP):

	n = 0
	in_head = False
	in_home = False
	in_away = False
	roster_row = 0
	head_col = 0
	GameKey = 0
	players = pd.DataFrame(np.empty([40,5]), index=range(0,40), columns=['GameKey', 'Team', 'Player', 'Position', 'Jersey'],
		dtype = type(0))

	def __init__(self,GameKey):
		HP.__init__(self)		
		self.GameKey = GameKey
		self.players['GameKey'] = GameKey

	def handle_starttag(self, tag, attrs):
		if tag == 'table':
			self.n += 1
			if self.n == 9:
				self.in_head = True
			elif self.n == 11:
				self.in_home = True
			elif self.n == 12:
				self.in_away = True
		
		if tag == 'td' and self.in_head:
			self.head_col += 1
		if tag == 'tr' and (self.in_home or self.in_away): 
			self.roster_row += 1

	def handle_endtag(self, tag):
		if tag == 'table':
			self.roster_row = 0
			self.head_col = 0
			if self.n == 9:
				self.in_head = False
			elif self.n == 11:
				self.in_home = False
			elif self.n == 12:
				self.in_away = False
			
	def handle_data(self,data):
		if self.in_head:
			if self.head_col == 1 and len(data) > 2:
				self.players.loc[0:20,'Team'] = data.strip()

			elif self.head_col == 2 and len(data) > 2:
				self.players.loc[20:40,'Team'] = data.strip()

		if (self.in_home or self.in_away) and self.roster_row > 1 and len(data) > 0 and not data.isspace():
			rost_ind = self.in_away*20 + (self.roster_row - 2)
			if data.isdigit():
				self.players.loc[ rost_ind, 'Jersey' ] = int(data) 
			elif len(data) == 1:
				self.players.loc[ rost_ind, 'Position' ] = data
			else:
				if data.find('(') > 0:
					data = data.rsplit(' ', 1)[0].strip()
				self.players.loc[ rost_ind, 'Player' ] = data 


# This classes uses the RosterParse class to build a giant roster table 

class RosterBuilder(object):
	Rosters = pd.DataFrame(columns=['GameKey', 'Team', 'Player', 'Position', 'Jersey'], dtype=type(0))
	BR_filename = 'Big_Roster.csv'
	
	def Build(self):
		for key in GameKeys:
		 	print "Processing game " + str(key+1) + " of " + str(max(GameKeys)+1)
			roster_url = 'http://www.nhl.com/scores/htmlreports/20152016/RO02' + str(key+1).zfill(4) + '.HTM'	
			ro_req = requests.get(roster_url)
			parser = RosterParse(key)
			ro_code = ro_req.text
			parser.feed(ro_code)
			new_ro = parser.players
			self.Rosters = self.Rosters.append(new_ro)

		self.Rosters.reset_index(inplace=True, drop=True)
		self.Rosters['GameKey'] = self.Rosters['GameKey'].apply(int)
		self.Rosters['Jersey'] = self.Rosters['Jersey'].apply(int)

	def Clean(self):
		self.Rosters['Player'].where( self.Rosters['Player'] != 'MICHAEL CAMMALLERI', 'MIKE CAMMALLERI', inplace=True)
	
	def Save(self):
		self.Rosters.to_csv(self.BR_filename)

