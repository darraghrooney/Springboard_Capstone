import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from scipy.sparse import csc_matrix

train_file = 'data/Training.npz'
cv_file = 'data/CV.npz'


class Big_Logistic(LogisticRegression):

    loader_train = np.load(train_file)
    loader_cv = np.load(cv_file)
    X_train = csc_matrix( (loader_train['training_matrix_data'], loader_train['training_matrix_indices'], 
        loader_train['training_matrix_indptr']), shape = loader_train['training_matrix_shape'] )
    y_train = loader_train['is_for_home']
    X_cv = csc_matrix( (loader_cv['CV_matrix_data'], loader_cv['CV_matrix_indices'], 
        loader_cv['CV_matrix_indptr']), shape = loader_cv['CV_matrix_shape'] )
    y_cv = loader_cv['is_for_home']

    def __init__(self, C = 1, solver = 'sag'):
        super(Big_Logistic, self).__init__(C = C, solver = solver)

    def fit(self):
        super(Big_Logistic, self).fit(self.X_train, self.y_train)

    def train_score(self):
        return self.score(self.X_train,self.y_train)

    def train_ce(self):
        log_probs = self.predict_log_proba(self.X_train)    
        return (-log_probs[:,1].T.dot(self.y_train)-log_probs[:,0].T.dot(~self.y_train))/float(len(self.y_train))

    def cv_score(self):
        return self.score(self.X_cv,self.y_cv)

    def cv_ce(self):
        log_probs = self.predict_log_proba(self.X_cv)    
        return (-log_probs[:,1].T.dot(self.y_cv)-log_probs[:,0].T.dot(~self.y_cv))/float(len(self.y_cv))


class BL_sweeper(object):

    Cs = [1]
    eval_matrix = pd.DataFrame()

    def __init__(self, C):
        self.Cs = C
        self.eval_matrix = pd.DataFrame(index = self.Cs, 
            columns = pd.MultiIndex.from_product( [['Training', 'CV'], ['Scores', 'Cross entropy']], names = ['split', 'metric']))
       
    def training(self):

        for C in self.Cs:

            BLR = Big_Logistic(C = C)
            BLR.fit()
            self.eval_matrix.loc[C, ('Training', 'Scores')] = BLR.train_score()
            self.eval_matrix.loc[C, ('CV', 'Scores')] = BLR.cv_score()
            self.eval_matrix.loc[C, ('Training', 'Cross entropy')] = BLR.train_ce()
            self.eval_matrix.loc[C, ('CV', 'Cross entropy')] = BLR.cv_ce()
