import numpy as np
import pandas as pd
from scipy.sparse import *

class FeatureAssemble(object):

	prefix = 'training'
	big_fn = '../data/Training.npz'
	small_fn = '../data/SmallTraining.npz'
	Corsis_fn = '../data/TrainCorsis.csv'
	
	Corsi = pd.DataFrame()
	features = np.zeros([1,1])
	feature_names = ['Sum of home log-likelihood(CF%)', 'Sum of away log-likelihood(CF%)', 'Mean home salary', 'Mean away salary',
		'Mean home paTOI/G', 'Mean away paTOI/G' 	]
	indicator = np.zeros([1,1])

	def __init__(self, which_set = 'train'):
		if which_set == 'cv':
			self.prefix = 'CV'
			self.big_fn = '../data/CV.npz'
			self.small_fn = '../data/SmallCV.npz'
			self.Corsis_fn = '../data/CVCorsis.csv'
		elif which_set == 'test':
			self.prefix = 'test'
			self.big_fn = '../data/Test.npz'
			self.small_fn = '../data/SmallTest.npz'
			self.Corsis_fn = '../data/TestCorsis.csv'

	def get_SAs(self,home_att, away_att, is_for_home):
		home_for = 0
		away_not = 0

		for index in home_att.indices:
			if is_for_home[index]:
				home_for += 1
		for index in away_att.indices:
			if is_for_home[index]:
				away_not += 1

		home_not = home_att.nnz - home_for
		away_for = away_att.nnz - away_not
		return home_for, home_not, away_for, away_not

	def Corsis(self):

		loader = np.load(self.big_fn)
		NGs = loader['non_goalies']
		no_players = len(NGs)
		att_matrix = csc_matrix( (loader[self.prefix + '_matrix_data'], loader[self.prefix + '_matrix_indices'], 
			loader[self.prefix + '_matrix_indptr']), shape=loader[self.prefix + '_matrix_shape'])
		HomeCorsi = list()
		AwayCorsi = list()
		BothCorsi = list()
		Fudges = list()
		fudge = 0.1
		for p in range(0, len(NGs)):
			print 'Calculating Corsi for {}'.format( NGs[p] )
			home_att = att_matrix.getcol(p)
			away_att = att_matrix.getcol(p+no_players)
			home_for, home_not, away_for, away_not = self.get_SAs(home_att, away_att, loader['is_for_home'])
			if min(home_for, home_not) == 0:
				home_for = max(home_for, fudge)
				home_not = max(home_not, fudge)
				if min(away_for, away_not) == 0:
					away_for = max(away_for, fudge)
					away_not = max(away_not, fudge)
					Fudges.append('Both')
				else:
					Fudges.append('Home')				
			elif min(away_for, away_not) == 0:
				Fudges.append('Away')
				away_for = max(away_for, fudge)
				away_not = max(away_not, fudge)
			else:
				Fudges.append('None')
			HomeCorsi.append( home_for / float(home_for + home_not) )
			AwayCorsi.append( away_for / float(away_for + away_not) )
			BothCorsi.append( (home_for + away_for) / float(home_for + home_not + away_for + away_not) )
			
		self.Corsi['Player'] = NGs
		self.Corsi['Home CF%'] = HomeCorsi
		self.Corsi['Away CF%'] = AwayCorsi
		self.Corsi['Total CF%'] = BothCorsi
		self.Corsi['Fudges'] = Fudges
		self.Corsi.to_csv(self.Corsis_fn, index=False)


	def Assemble(self):

		loader = np.load(self.big_fn)
		self.Corsi = pd.read_csv(self.Corsis_fn)

		NGs = loader['non_goalies']
		no_players = len(NGs)
		att_matrix = csc_matrix( (loader[self.prefix + '_matrix_data'], loader[self.prefix + '_matrix_indices'], 
			loader[self.prefix + '_matrix_indptr']), shape=loader[self.prefix + '_matrix_shape'])

		home_llC = np.zeros(att_matrix.shape[0])
		away_llC = np.zeros(att_matrix.shape[0])

		for p in range(0, len(NGs)):
			print 'Adding data for {} to features'.format( NGs[p] )
			home_att = att_matrix.getcol(p)
			away_att = att_matrix.getcol(p+no_players)
			for index in home_att.indices:
				prob = self.Corsi.loc[p,'Home CF%']
				home_llC[index] += np.log( prob/float(1-prob))

			for index in away_att.indices:
				prob = self.Corsi.loc[p,'Away CF%']
				away_llC[index] += np.log( prob/float(1-prob))
		
		self.features = np.array( [home_llC, away_llC, loader['home_OI_sal'], loader['away_OI_sal'], 
			loader['home_OI_PT'], loader['away_OI_PT'] ] ).T
		self.indicator = loader['is_for_home']
		np.savez( self.small_fn, features = self.features, feature_names = self.feature_names, indicator = self.indicator)

