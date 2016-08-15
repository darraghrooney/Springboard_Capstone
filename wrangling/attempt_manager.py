# This is a class for building and loading shot attempt data for the 2015-2016 season
# The big sparse matrix is a 0-1 matrix recording which players were on the ice for all shot attempts
# Furthe class variables record the type of shot attempts, whether the shot was for the home or away team,
# the average salary of home on-ice and away on-ice, the average playing time of home and away on-ice players,
# the game counts of shot attempts, and the team names.

import numpy as np
import pandas as pd
from scipy.sparse import *

GameKeys = range(0,1230)
Directory_filename = '../data/Directory.csv'

# Dictionary for translating team names to abbreviations

Team_abbrev = {
	'ANAHEIM DUCKS':'ANA',
	'ARIZONA COYOTES':'ARI',
	'BOSTON BRUINS':'BOS',
	'BUFFALO SABRES':'BUF',
	'CALGARY FLAMES':'CGY',
	'CAROLINA HURRICANES':'CAR',
	'CHICAGO BLACKHAWKS':'CHI',
	'COLORADO AVALANCHE':'COL',
	'COLUMBUS BLUE JACKETS':'CBJ',
	'DALLAS STARS':'DAL',
	'DETROIT RED WINGS':'DET',
	'EDMONTON OILERS':'EDM',
	'FLORIDA PANTHERS':'FLA',
	'LOS ANGELES KINGS':'L.A',
	'MINNESOTA WILD':'MIN',
	'MONTREAL CANADIENS':'MTL',
	'NASHVILLE PREDATORS':'NSH',
	'NEW JERSEY DEVILS':'N.J',
	'NEW YORK ISLANDERS':'NYI',
	'NEW YORK RANGERS':'NYR',
	'OTTAWA SENATORS':'OTT',
	'PHILADELPHIA FLYERS':'PIT',
	'PITTSBURGH PENGUINS':'PHI',
	'SAN JOSE SHARKS':'S.J',
	'ST. LOUIS BLUES':'STL',
	'TAMPA BAY LIGHTNING':'T.B',
	'TORONTO MAPLE LEAFS':'TOR',
	'VANCOUVER CANUCKS':'VAN',
	'WASHINGTON CAPITALS':'WSH',
	'WINNIPEG JETS':'WPG'
}

class attempt_manager(object):

	attempt_filename = 'data/Attempts.npz'
	no_att = 0
	att_matrix = lil_matrix([1,1], dtype=bool)
	game_counts = list()
	home_indices = list()
	attempt_type = list()
	home_teams = list()
	away_teams = list()
	home_OI_sal = list()
	away_OI_sal = list()
	home_OI_PT = list()
	away_OI_PT = list()
	NGs = list()			# list of players (excluding goalies)

	att_dict = {'GOAL': 'G', 'MISS': 'M', 'SHOT': 'S', 'BLOCK': 'B'}

	# Before constructing matrix, count total shot attempts
	
	def Count(self):

		for key in GameKeys:
			print 'Counting attempts in Game {}'.format(key+1)
			game_file = '../data/PlayDF/DF{}.csv'.format( str(key+1).zfill(4) ) 
			game_att = pd.read_csv(game_file)
			self.no_att += len(game_att)

		print 'Total number of shot attempts: {}'.format(self.no_att)

	# Method for building the data from individual play-by-play reports
	def Build(self):

		BR_filename = '../data/Big_Roster.csv'
		print 'Initializing matrix...'

		Dir = pd.read_csv(Directory_filename)
		Dir = Dir[Dir.Position != 'G']
		self.NGs = list(Dir.Player)
		sal_dict = {Dir.Player[k]:Dir.Salary[k] for k in Dir.index}
		PT_dict = {Dir.Player[k]:Dir['paTOI/G'][k] for k in Dir.index}

		self.att_matrix = lil_matrix( (self.no_att, 2*len(Dir)), dtype=bool)

		for key in GameKeys:

			print 'Processing Game {}'.format(key+1)
			game_file = '../data/DF{}.csv'.format( str(key+1).zfill(4) ) 

			big_ro = pd.read_csv(BR_filename)
			short_ro = big_ro[ big_ro.GameKey == key]
			short_ro = short_ro[ ['Player', 'Team', 'Jersey'] ]
			del big_ro
			short_ro['Team'] = short_ro['Team'].map(Team_abbrev)
			self.home_teams.append( short_ro.Team[key*40 + 20] )
			self.away_teams.append( short_ro.Team[key*40 + 0] )

			game_att = pd.read_csv(game_file)
			game_att = game_att.fillna(-1)
			home_dict = { short_ro.Jersey[k]: short_ro.Player[k] for k in range(key*40+20, key*40+40) }
			home_dict[-1] =  'NO-ONE'
			away_dict = { short_ro.Jersey[k]: short_ro.Player[k] for k in range(key*40, key*40+20) }
			away_dict[-1] =  'NO-ONE'
			
			offset = sum(self.game_counts)
			for j in range(0, len(game_att)):
				h_sal = list()
				a_sal = list()
				h_PT = list()
				a_PT = list()
				for k in range(0,6):
					h_play = home_dict[ game_att.ix[j, 'H{}'.format(k+1)] ]
					a_play = away_dict[ game_att.ix[j, 'A{}'.format(k+1)] ]
					if h_play in self.NGs: 	
						self.att_matrix[ j + offset, self.NGs.index(h_play) ] = True
						h_sal.append( sal_dict[h_play])
						h_PT.append( PT_dict[h_play])
					if a_play in self.NGs:
						self.att_matrix[ j + offset, len(Dir) + self.NGs.index( a_play ) ] = True
						a_sal.append( sal_dict[a_play])
						a_PT.append( PT_dict[a_play])

				self.home_OI_sal.append( 0 if len(h_sal) == 0 else np.mean(h_sal))
				self.away_OI_sal.append( 0 if len(a_sal) == 0 else np.mean(a_sal))
				self.home_OI_PT.append( 0 if len(h_PT) == 0 else np.mean(h_PT))
				self.away_OI_PT.append( 0 if len(a_PT) == 0 else np.mean(a_PT) )

			self.game_counts.append(len(game_att))
			hsa = game_att['Home?']
			hsa_ind = hsa[hsa].index.get_values()
			self.home_indices.extend( [ (offset + j) for j in hsa_ind ])
			
			self.attempt_type.extend( [self.att_dict[att] for att in game_att['Event'] ] )

		self.att_matrix = self.att_matrix.tocsc()

	def Save(self):
		print 'Saving data...'
		np.savez(self.attempt_filename, attempt_matrix_data = self.att_matrix.data, attempt_matrix_indices = self.att_matrix.indices,
			attempt_matrix_indptr = self.att_matrix.indptr, attempt_matrix_shape = self.att_matrix.shape, 
			game_counts = self.game_counts, home_indices = self.home_indices, 
			attempt_type = self.attempt_type, home_teams = self.home_teams, away_teams = self.away_teams, non_goalies = self.NGs,
			home_OI_sal = self.home_OI_sal, away_OI_sal = self.away_OI_sal, home_OI_PT = self.home_OI_PT, away_OI_PT = self.away_OI_PT)
		print '...done'

	def Load(self):
		loader = np.load(self.attempt_filename)
		self.game_counts =  list(loader['game_counts'])
		self.home_indices =  list(loader['home_indices'])
		self.attempt_type =  list(loader['attempt_type'])
		self.home_teams =  list(loader['home_teams'])
		self.away_teams =  list(loader['away_teams'])
		self.NGs =  list(loader['non_goalies'])
		self.home_OI_sal =  list(loader['home_OI_sal'])
		self.away_OI_sal =  list(loader['away_OI_sal'])
		self.home_OI_PT =  list(loader['home_OI_PT'])
		self.away_OI_PT =  list(loader['away_OI_PT'])
		self.att_matrix = csc_matrix( (loader['attempt_matrix_data'], loader['attempt_matrix_indices'], loader['attempt_matrix_indptr']), 
			shape = loader['attempt_matrix_shape'])
		self.no_att = len(self.attempt_type)
		


	# Computes a player's CF% for a season. Option exists to compute only home or away Corsi
	def compute_Corsi(self, player, qualifier = None):
		if player not in self.NGs:
			print 'Player not found'
			return

		NG_ind = self.NGs.index(player)
		home_att = self.att_matrix.getcol(NG_ind).indices
		away_att = self.att_matrix.getcol(len(self.NGs) + NG_ind).indices
		
		if qualifier == 'home' and float(len(home_att)) > 0:
			return len( set(home_att) & set(self.home_indices)) / float(len(home_att))
		elif qualifier == 'away' and float(len(away_att)) > 0:
			return 1 - len( set(away_att) & set(self.home_indices)) / float(len(away_att))
		elif float(len(away_att) + len(home_att)) > 0:
			numerator = len( set(home_att) & set(self.home_indices)) + len(away_att) - len( set(away_att) & set(self.home_indices)) 
			return numerator / float( len(home_att) + len(away_att) )
		else:
			return None

