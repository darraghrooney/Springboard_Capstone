# Code to transform game-by-game roster data into a player directory. 
# Two classes: one to scrape salary data for the players, and another to build the directory from the big roster

import numpy as np
import pandas as pd
from HTMLParser import HTMLParser as HP
import requests

# Scrapes player salaries from www.capfriendly.com

class SalaryParse(HP):
	salary = '$0'
 	in_contracts = True
 	in_2015 = False
 	col_count = 0

 	def handle_starttag(self, tag, attrs):
 		if self.in_2015 and tag == 'td':
 			self.col_count += 1
 			if (u'colspan', u'3') in attrs:
 				self.salary = None
 				self.in_2015 = False
	
 	def handle_endtag(self, tag):
		pass
		
 	def handle_data(self,data):
	 	if self.in_contracts and data.startswith('2015-'):
 			self.in_2015 = True
 		elif self.in_2015 and self.col_count == 6:
 			self.salary = data
 			self.in_2015 = False
 			self.in_contracts = False


# Takes the game-by-game roster info and compiles into a player directory. Adds salary information
			
class DirectoryBuilder():

	Directory = pd.DataFrame(columns=['Player', 'Position', 'Games Dressed'])
	BR_filename = '../data/Big_Roster.csv'
	Dir_filename = '../data/Directory.csv'
	Big_Roster = pd.read_csv(BR_filename)

	def Build(self):
		self.Directory =  self.Big_Roster.groupby(['Player', 'Position']).size()
		self.Directory = self.Directory.reset_index() 
		self.Directory.rename( columns = {0: 'Games Dressed'} , inplace= True)
		self.Directory['ID'] = range(1, len(self.Directory)+1)
		self.Directory = self.Directory[ ['ID', 'Player', 'Position', 'Games Dressed'] ]

	def Save(self):
		self.Directory.to_csv(self.Dir_filename, index = False)

	def add_Salaries(self):
		players = self.Directory['Player']
		self.Directory.rename(self.Directory['Player'], inplace=True)
		if 'Salary' in self.Directory.columns:
			players = players[self.Directory['Salary'].isnull()]
		else: 
			self.Directory['Salary'] = None
		
		for p in players:
			url = 'https://www.capfriendly.com/players/' + p.lower().replace(' ','-').replace('.','')
			print "Finding salary for " + p + "..."
			try:
				r = requests.get(url)
				parser = SalaryParse()
				parser.feed(r.text)
				sal = parser.salary
				if not sal == None and sal[0] == '$':
					print 'Salary is ' + sal
		 			sal_num = float(sal.replace('$','').replace(',',''))
		 			self.Directory.loc[p, 'Salary'] = sal_num
		 		else: 
		 			print 'Salary not availabe from CapFriendly'
	 		
			except requests.ConnectionError:
	 			print 'Connection Error. Ignoring.'

