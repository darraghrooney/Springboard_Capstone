import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from scipy.sparse import csc_matrix

train_file = 'data/SmallTraining.npz'
cv_file = 'data/SmallCV.npz'


class Small_Logistic(LogisticRegression):

    loader_train = np.load(train_file)
    loader_cv = np.load(cv_file)
    X_train = loader_train['features']
    y_train = loader_train['indicator']
    X_cv = loader_cv['features']
    y_cv = loader_cv['indicator']

    def __init__(self, features = 'all', C = 1, solver = 'liblinear'):
        super(Small_Logistic, self).__init__(C = C, solver=solver)
        if features == 'Corsis':
            self.X_train = self.X_train[:,[0,1]]
            self.X_cv = self.X_cv[:,[0,1]]
        elif features == 'plus_PT':
            self.X_train = self.X_train[:,[0,1,4,5]]
            self.X_cv = self.X_cv[:,[0,1,4,5]]


    def normalize(self):
        for j in range(0, self.X_train.shape[1] ):
            self.X_train[:,j]=(self.X_train[:,j]-self.X_train[:,j].mean())/self.X_train[:,j].std()
            self.X_cv[:,j]=(self.X_cv[:,j]-self.X_cv[:,j].mean())/self.X_cv[:,j].std()

    def fit(self):
        super(Small_Logistic, self).fit(self.X_train, self.y_train)

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


class SL_sweeper(object):

    Cs = [1]
    eval_matrix = pd.DataFrame()
    features = ['Corsis', 'plus_PT', 'all']

    def __init__(self, C):
        self.Cs = C
        self.eval_matrix = pd.DataFrame(index = self.Cs, 
            columns = pd.MultiIndex.from_product( [self.features, ['Training', 'CV'], ['Scores', 'Cross entropy']], names = ['features', 'split', 'metric']))
       
    def training(self):

        for feat in self.features:
            for C in self.Cs:
    
                SLR = Small_Logistic(C = C, solver='newton-cg', features = feat)
                SLR.normalize()
                SLR.fit()
                self.eval_matrix.loc[C, (feat, 'Training', 'Scores')] = SLR.train_score()
                self.eval_matrix.loc[C, (feat, 'CV', 'Scores')] = SLR.cv_score()
                self.eval_matrix.loc[C, (feat, 'Training', 'Cross entropy')] = SLR.train_ce()
                self.eval_matrix.loc[C, (feat, 'CV', 'Cross entropy')] = SLR.cv_ce()
