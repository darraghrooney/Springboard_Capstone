# %load convert.py
import numpy as np
from scipy.sparse import *


def convert(set_string):

	if set_string == 'train':
		loader = np.load('../data/Training.npz')
		print 'Converting...'

		col_matr = csc_matrix((loader['training_matrix_data'],loader['training_matrix_indices'],
					loader['training_matrix_indptr']), shape = loader['training_matrix_shape'])
    
		row_matr = col_matr.tocsr()
		print 'Saving...'
		np.savez('../data/Training.npz', training_matrix_data = row_matr.data,  training_matrix_indices = row_matr.indices, 
			training_matrix_indptr = row_matr.indptr,  training_matrix_shape = row_matr.shape,
			is_for_home = loader['is_for_home'], training_ind = loader['training_ind'], attempt_type=loader['attempt_type'],
			non_goalies = loader['non_goalies'], home_OI_sal = loader['home_OI_sal'], away_OI_sal = loader['away_OI_sal'], 
			home_OI_PT = loader['home_OI_PT'], away_OI_PT = loader['away_OI_PT'])
		print 'Done'

	elif set_string == 'cv':
		loader = np.load('../data/CV.npz')
		print 'Converting...'

		col_matr = csc_matrix((loader['CV_matrix_data'],loader['CV_matrix_indices'],
					loader['CV_matrix_indptr']), shape = loader['CV_matrix_shape'])
    
		row_matr = col_matr.tocsr()
		print 'Saving...'
		np.savez('../data/csr_CV.npz', CV_matrix_data = row_matr.data,  CV_matrix_indices = row_matr.indices, 
			CV_matrix_indptr = row_matr.indptr,  CV_matrix_shape = row_matr.shape,
			is_for_home = loader['is_for_home'], attempt_type=loader['attempt_type'],
			non_goalies = loader['non_goalies'], home_OI_sal = loader['home_OI_sal'], away_OI_sal = loader['away_OI_sal'], 
			home_OI_PT = loader['home_OI_PT'], away_OI_PT = loader['away_OI_PT'])
		print 'Done'


	if set_string == 'test':
		loader = np.load('../data/Test.npz')
		print 'Converting...'

		col_matr = csc_matrix((loader['test_matrix_data'],loader['test_matrix_indices'],
					loader['test_matrix_indptr']), shape = loader['test_matrix_shape'])
    
		row_matr = col_matr.tocsr()
		print 'Saving...'
		np.savez('../data/csr_Test.npz', test_matrix_data = row_matr.data,  test_matrix_indices = row_matr.indices, 
			test_matrix_indptr = row_matr.indptr,  test_matrix_shape = row_matr.shape,
			is_for_home = loader['is_for_home'], attempt_type=loader['attempt_type'],
			non_goalies = loader['non_goalies'], home_OI_sal = loader['home_OI_sal'], away_OI_sal = loader['away_OI_sal'], 
			home_OI_PT = loader['home_OI_PT'], away_OI_PT = loader['away_OI_PT'])
		print 'Done'

convert('cv')
convert('test')