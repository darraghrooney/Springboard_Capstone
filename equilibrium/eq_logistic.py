import numpy as np
import pandas as pd
from scipy.sparse import *
from sklearn.ensemble import RandomForestClassifier


train_file = 'data/Training.npz'
cv_file = 'data/CV.npz'

class rafo(RandomForestClassifier):

    X_train = np.array(pd.read_csv('data/Eq_Feat_training.csv'))
    X_cv = np.array(pd.read_csv('data/Eq_Feat_CV.csv'))
    y_train = np.load('data/Training.npz')['is_for_home']
    y_cv = np.load('data/CV.npz')['is_for_home']

    def __init__(self, C = 1, solver = 'newton-cg'):
        super(eq_logistic, self).__init__(C = C, solver=solver)

    def fit(self):
        super(eq_logistic, self).fit(self.X_train, self.y_train)

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

class EL_sweeper(object):

    Cs = [1]
    eval_matrix = pd.DataFrame()

    def __init__(self, C):
        self.Cs = C
        self.eval_matrix = pd.DataFrame(index = self.Cs, columns = pd.MultiIndex.from_product( [['Training', 'CV'], ['Scores', 'Cross entropy']], names = ['split', 'metric']))
   
    def training(self):

        for C in self.Cs:
            ELR = eq_logistic(C = C, solver='newton-cg')
            ELR.fit()
            self.eval_matrix.loc[C, ('Training', 'Scores')] = ELR.train_score()
            self.eval_matrix.loc[C, ('CV', 'Scores')] = ELR.cv_score()
            self.eval_matrix.loc[C, ('Training', 'Cross entropy')] = ELR.train_ce()
            self.eval_matrix.loc[C, ('CV', 'Cross entropy')] = ELR.cv_ce()    