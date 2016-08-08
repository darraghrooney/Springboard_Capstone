# Code for scraping game scores and TOI (time on-ice) from the NHL "event report" pages
# One class parses the reports

import numpy as np
import pandas as pd
from HTMLParser import HTMLParser as HP

GameKeys = range(0,1230)
Directory_filename = '../data/Directory.csv'

# Class to parse game reports	
class EventParse(HP):

	# Uses a rope variable to record where you are in the table tree
	rope = list()
	home_goals = -1
	away_goals = -1
	home_toi = pd.DataFrame(np.zeros([20,2]), columns = ['Player', 'TOI'])
	away_toi = pd.DataFrame(np.zeros([20,2]), columns = ['Player', 'TOI'])

	# Occasionally there's a team penalty which affects the HTML
	team_pen_detect = 0

	def handle_starttag(self, tag, attrs):
		if (len(self.rope) % 3 == 0 and tag == 'table') or (len(self.rope) % 3 == 1 and tag == 'tr') or (len(self.rope) % 3 == 2 and tag == 'td'):
			self.rope += [1]
		elif (len(self.rope) % 3 == 0 and tag == 'td') or (len(self.rope) % 3 == 1 and tag == 'table') or (len(self.rope) % 3 == 2 and tag == 'tr'):
			self.rope[-1] += 1


	def handle_endtag(self, tag):
		if (len(self.rope) % 3 == 0 and tag != 'td') or (len(self.rope) % 3 == 1 and tag != 'table') or (len(self.rope) % 3 == 2 and tag != 'tr'):
			self.rope = self.rope[:-1]


	def handle_data(self,data):
		
		# Record game score
		if self.rope == [1,3,1,1,2,1,1,1,1,1,2,4] and len(data.strip()) > 0:
			self.away_goals = data.strip().split('-')[0]
		elif self.rope == [1,3,1,1,2,1,1,1,2,1,2,4] and len(data.strip()) > 0:
			self.home_goals = data.strip().split('-')[0]

		# Record TOI
		if len(self.rope) == 6 and self.rope[0:4] == [1,8,1,1] and len(data.strip())>0:

			# Home player TOI
			if self.rope[4] in range(3,23):
				if self.rope[5]==3:
					name = data.split(',')
					name.reverse()
					if name[1] == 'CAMMALLERI':			# CAMMALERI went by MICHAEL for four games, and MIKE the rest
						name[0] = 'MIKE'
					self.home_toi.iloc[ self.rope[4]-3,0] = ' '.join(name).strip()
				elif self.rope[5] == 10:	
					toi = data.split(':')
					self.home_toi.iloc[ self.rope[4]-3,1] = int(toi[0])+int(toi[1])/60.

			# Take care of team penalty 
			elif self.rope[4] == 23 and self.rope[5] == 3:
				if data == 'TEAM PENALTY'.strip():
					self.team_pen_detect = 1
				else:
					self.team_pen_detect = 0

			# Away player TOI
			elif self.rope[4] in range(28 + self.team_pen_detect,48 + self.team_pen_detect):
				if self.rope[5]==3:
					name = data.split(',')
					name.reverse()
					if name[1] == 'CAMMALLERI':
						name[0] = 'MIKE'
					self.away_toi.iloc[ self.rope[4]-28 - self.team_pen_detect,0] = ' '.join(name).strip()
				elif self.rope[5] == 10:	
					toi = data.split(':')
					self.away_toi.iloc[ self.rope[4] - 28 - self.team_pen_detect,1] = int(toi[0])+int(toi[1])/60.
			
		
# Class for recording scores for all games	
	
class ScoreBuilder:

	ScoreFrame = pd.DataFrame(np.empty([len(GameKeys), 3]), columns = ['Game', 'Home score', 'Away score'])
	Score_filename = '../data/game_scores.csv'

	def Build(self):
		EP = EventParse()
		for key in GameKeys:

			print "Getting score from Game " + str(key+1) + "..."
			fn = 'EventReports/ER' + str(key+1).zfill(4) + '.txt'
			self.ScoreFrame.iloc[key,0] = key+1

			with open(fn) as file: 
				ft = file.read()
				EP.feed(ft)
				self.ScoreFrame.iloc[key,[1,2]] = [EP.home_goals, EP.away_goals]

	def Save(self):
		self.ScoreFrame.to_csv(self.Score_filename, index=False)

# Class for recording TOI for all players. Only records total TOI for the season
class TOIBuilder:

	TOI_Dir = pd.DataFrame()

	def Build(self):
		self.TOI_Dir = pd.read_csv(Directory_filename)
		if 'TOI' not in self.TOI_Dir.columns:
			self.TOI_Dir['TOI'] = np.zeros([len(self.TOI_Dir),1])
		self.TOI_Dir.rename(self.TOI_Dir['Player'],inplace=True)

		EP = EventParse()
		for key in GameKeys:

			print "Adding TOI from Game " + str(key+1) + "..."

			fn = 'EventReports/ER' + str(key+1).zfill(4) + '.txt'
			with open(fn) as file: 
				ft = file.read()
				EP.feed(ft)

				htoi = EP.home_toi.rename(EP.home_toi['Player'])
				atoi = EP.away_toi.rename(EP.away_toi['Player'])

				self.TOI_Dir.loc[ EP.home_toi['Player'], 'TOI'] += htoi['TOI']
				self.TOI_Dir.loc[ EP.away_toi['Player'], 'TOI'] += atoi['TOI']

	def Save(self):
		self.TOI_Dir.to_csv(Directory_filename, index=False)

# Thie function adds a column to the player directory: positionally adjusted TOI per game_scores
# Basically average TOI for forwards, but 0.75 of average TOI for defensement to account for fewer lines
def Dir_process():
	Directory = pd.read_csv(Directory_filename)
	Directory['TOI'].where( Directory['TOI'] > 0, None, inplace=True)
	if 'paTOI/G' not in Directory.columns:
		p_fac = Directory['Position'].map({'D': 0.75, 'C': 1, 'R': 1, 'L': 1, 'G': 0})
		Directory['paTOI/G'] = p_fac*Directory['TOI']/Directory['Games Dressed']
	Directory.to_csv(Directory_filename, index=False)
