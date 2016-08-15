import numpy as np
import attempt_manager as am
from scipy.sparse import *

class data_split(object):

	seed = 1911
	fractions = [0.6, 0.2, 0.2]
	length = 0
	train_ind = list()
	CV_ind = list()
	test_ind = list()
 	AM = am.attempt_manager()
	set_filenames = ['Training.npz', 'CV.npz', 'Test.npz']
	
	def Choose(self):
		np.random.seed(self.seed)
		self.AM.Load()
		self.length = self.AM.no_att
		
		self.test_ind = list(  np.random.choice( np.array(range(0,self.length)), self.fractions[2] * self.length, replace = False))
		remainder =  np.array(list(set(range(0,self.length) ) - set(self.test_ind)))
		self.cv_ind = list( np.random.choice( remainder, self.fractions[1] * self.length, replace = False))
		self.train_ind =  list( set( remainder ) - set(self.cv_ind) )
		self.test_ind.sort()
		self.cv_ind.sort()
		self.train_ind.sort()
	
	def CreateTraining(self):
		
		print 'Creating training set'
		attempts = self.AM.att_matrix
		training_matrix = lil_matrix( ( len(self.train_ind), 2*len(self.AM.NGs) ), dtype=bool)
		for k1 in range(0, attempts.shape[1]):
			print 'Processing player {}'.format(k1 + 1)
			pl_att = attempts.getcol(k1)
			for k2 in list(pl_att.indices):
				if k2 in self.train_ind:
					training_matrix[self.train_ind.index(k2), k1] = True

		training_matrix = training_matrix.tocsc()
		print 'Saving...'
		np.savez( '../data/' + self.set_filenames[0], training_matrix_data = training_matrix.data, training_matrix_indices = training_matrix.indices,
			training_matrix_indptr = training_matrix.indptr, training_matrix_shape = training_matrix.shape, training_ind=self.train_ind,
			is_for_home = np.array( [ (k in self.AM.home_indices) for k in self.train_ind  ]), attempt_type = np.array(self.AM.attempt_type)[self.train_ind], non_goalies = self.AM.NGs, 
			home_OI_sal = np.array(self.AM.home_OI_sal)[self.train_ind], away_OI_sal = np.array(self.AM.away_OI_sal)[self.train_ind], 
			home_OI_PT = np.array(self.AM.home_OI_PT)[self.train_ind], away_OI_PT = np.array(self.AM.away_OI_PT)[self.train_ind] )
		print 'Done'
		
	def CreateCV(self):
		
		print 'Creating CV set'
		attempts = self.AM.att_matrix
		CV_matrix = lil_matrix( ( len(self.cv_ind), 2*len(self.AM.NGs) ), dtype=bool)
		for k1 in range(0,attempts.shape[1]):
			print 'Processing player {}'.format(k1 + 1)
			pl_att = attempts.getcol(k1)
			for k2 in list(pl_att.indices):
				if k2 in self.CV_ind:
					CV_matrix[self.CV_ind.index(k2), k1] = True
		CV_matrix = CV_matrix.tocsc()
		print 'Saving...'
		np.savez( '../data/' + self.set_filenames[1], CV_matrix_data = CV_matrix.data, CV_matrix_indices = CV_matrix.indices,
			CV_matrix_indptr = CV_matrix.indptr, CV_matrix_shape = CV_matrix.shape,
			is_for_home = np.array( [ (k in self.AM.home_indices) for k in self.CV_ind  ] ), attempt_type = np.array(self.AM.attempt_type)[self.CV_ind], non_goalies = self.AM.NGs, 
			home_OI_sal = np.array(self.AM.home_OI_sal)[self.CV_ind], away_OI_sal = np.array(self.AM.away_OI_sal)[self.CV_ind], 
			home_OI_PT = np.array(self.AM.home_OI_PT)[self.CV_ind], away_OI_PT = np.array(self.AM.away_OI_PT)[self.CV_ind] )
		print 'Done'
		
	def CreateTest(self):
		
		print 'Creating test set'
		attempts = self.AM.att_matrix
		test_matrix = lil_matrix( ( len(self.test_ind), 2*len(self.AM.NGs) ), dtype=bool)
		for k1 in range(0,attempts.shape[1]):
			print 'Processing player {}'.format(k1 + 1)
			pl_att = attempts.getcol(k1)
			for k2 in list(pl_att.indices):
				if k2 in self.test_ind:
					test_matrix[self.test_ind.index(k2), k1] = True

		print 'Saving...'
		np.savez( '../data/' + self.set_filenames[2], test_matrix_data = test_matrix.data, test_matrix_indices = test_matrix.indices, 
			test_matrix_indptr = test_matrix.indptr, test_matrix_shape = test_matrix.shape,
			is_for_home = np.array( [ (k in self.AM.home_indices) for k in self.test_ind  ]), attempt_type = np.array(self.AM.attempt_type)[self.test_ind], non_goalies = self.AM.NGs, 
			home_OI_sal = np.array(self.AM.home_OI_sal)[self.test_ind], away_OI_sal = np.array(self.AM.away_OI_sal)[self.test_ind], 
			home_OI_PT = np.array(self.AM.home_OI_PT)[self.test_ind], away_OI_PT = np.array(self.AM.away_OI_PT)[self.test_ind] )
		print 'Done'
		
		
DS = data_split()
DS.Choose()
DS.CreateTraining()
