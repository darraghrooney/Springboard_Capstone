# Code for turning downloaded HTML play-by-play reports into shot attempt data files
# One class for parsing the HTML and one function for looping over all reports and saving the data

import numpy as np
import pandas as pd
from HTMLParser import HTMLParser as HP

GameKeys = range(0,1230)
Directory_filename = '../data/Directory.csv'
events = ['GOAL', 'SHOT', 'MISS', 'BLOCK']

# Class for parsing HTML

class PlayParse(HP):
	rope = list()
	home_team = None
	away_team = None
	shot_attempts = list()
	latest_attempt = [None for j in  range(0,14)]
	in_attempt = False

	def handle_starttag(self, tag, attrs):
		if tag == 'head':
			self.rope = list()
			self.shot_attempts = list()
			self.latest_attempt = [None for j in  range(0,14)]

		elif (len(self.rope) % 3 == 0 and tag == 'table') or (len(self.rope) % 3 == 1 and tag == 'tr') or (len(self.rope) % 3 == 2 and tag == 'td'):
			self.rope += [1]
		elif (len(self.rope) % 3 == 0 and tag == 'td') or (len(self.rope) % 3 == 1 and tag == 'table') or (len(self.rope) % 3 == 2 and tag == 'tr'):
			self.rope[-1] += 1
		
		if self.in_attempt and len(self.rope) > 3 and self.rope[2] == 1:
			self.in_attempt = False

	def handle_endtag(self, tag):
		if tag == 'td' and self.in_attempt and len(self.rope) == 4 and self.rope[2] == 8:  
			self.shot_attempts.append(self.latest_attempt)
			self.latest_attempt = [None for j in range(0,14)]
			self.in_attempt = False

		if (len(self.rope) % 3 == 0 and tag == 'tr') or (len(self.rope) % 3 == 1 and tag == 'td') or (len(self.rope) % 3 == 2 and tag == 'table'):
			self.rope = self.rope[:-1]


	def handle_data(self,data):
		if self.rope == [1,3,7] and len(data.strip() )>0:
			self.away_team = data.split()[0]
		elif self.rope == [1,3,8] and len(data.strip())>0:
			self.home_team = data.split()[0]
		
		if len(self.rope) > 2 and self.rope[0] in [1,2,3,4] and self.rope[1] > 3:
			if self.rope[2] == 5 and data in events:
				self.latest_attempt[0] = data
				self.in_attempt = True

			if self.in_attempt:
				if self.rope[2] == 6 and len(data.strip()) > 0 and data.split()[0] in [self.home_team, self.away_team]:
					self.latest_attempt[1] = {self.home_team: True, self.away_team: False}[data.split()[0]]
				elif self.rope[2] in [7,8] and len(self.rope) == 9 and self.rope[5] in [1,3,5,7,9,11] and self.rope[6:9] == [1,1,1] and data.isdigit():
					self.latest_attempt[ 2 + int((self.rope[5]-1)/2) + 6*(8-self.rope[2]) ] = data.strip()
					
# Loop over all games, form data frame and save

def PlaySaver():
	for key in GameKeys:

		print "Processing Game " + str(key+1) + "..."
		fn = '../data/PlayReports/PR' + str(key+1).zfill(4) + '.txt'

		PP = PlayParse()
		with open(fn) as file: 
			ft = file.read()
			PP.feed(ft)
			sas = PP.shot_attempts
			sadf = pd.DataFrame(sas, columns = ['Event', 'Home?', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6'])
			sadf.to_csv('../data/PlayDF/DF' + str(key+1).zfill(4) + '.csv', index=False)
