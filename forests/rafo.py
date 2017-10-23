import numpy as np
import pandas as pd
from scipy.sparse import *
from sklearn.ensemble import RandomForestClassifier as RFC
import pickle
import matplotlib.pyplot as plt


train_file = 'data/Training.npz'
cv_file = 'data/CV.npz'

class rf_coll(object):

    ds = [1]
    n_t = [1]
    eval_matrix = pd.DataFrame()

    def __init__(self, ds,n_t):
        self.ds = ds
        self.n_t = n_t
        self.eval_matrix = pd.DataFrame(index = pd.MultiIndex.from_product([self.ds,self.n_t]), columns = pd.MultiIndex.from_product( [['Training', 'CV'], ['Scores', 'Cross entropy']], names = ['split', 'metric']))                
   
    def training(self):

        loader=np.load(train_file)
        X_train = csc_matrix( (loader['training_matrix_data'], loader['training_matrix_indices'], loader['training_matrix_indptr']), shape=loader['training_matrix_shape'])
        y_train=loader['is_for_home']

        for jd in self.ds:
            for jt in self.n_t:
                print('Processing forests with ' + str(jt) + ' trees and depth ' + str(jd))
                myrfc=RFC(n_estimators=jt,criterion="entropy",max_depth=jd )
                myrfc.fit(X_train,y_train)
                fn = 'data/Forest_'+str(jt)+'_'+str(jd)
                with open(fn, 'wb') as output:
                    pickle.dump(myrfc,output)

    def evaluate(self):

        loader=np.load(train_file)
        X_train = csc_matrix( (loader['training_matrix_data'], loader['training_matrix_indices'], loader['training_matrix_indptr']), shape=loader['training_matrix_shape'])
        y_train=loader['is_for_home']
        loader2=np.load(cv_file)
        X_CV = csc_matrix( (loader2['CV_matrix_data'], loader2['CV_matrix_indices'], loader2['CV_matrix_indptr']), shape=loader2['CV_matrix_shape'])
        y_CV=loader2['is_for_home']

        for jd in self.ds:
            for jt in self.n_t:
                fn = 'data/Forest_'+str(jt)+'_'+str(jd)
                with open(fn, 'rb') as input:
                    unpickler = pickle.Unpickler(input)
                    myrfc = unpickler.load()
                    self.eval_matrix.loc[jd,jt].loc[('Training', 'Scores')] = myrfc.score(X_train,y_train)
                    self.eval_matrix.loc[jd,jt].loc[('CV', 'Scores')] = myrfc.score(X_CV,y_CV)
                    log_probs_tr = myrfc.predict_log_proba(X_train)    
                    c0 = log_probs_tr[:,0] < -4
                    c1 = log_probs_tr[:,1] < -4
                    log_probs_tr[c0,0] = -4
                    log_probs_tr[c0,1] = np.log(1-np.exp(-4)) 
                    log_probs_tr[c1,1] = -4
                    log_probs_tr[c1,0] = np.log(1-np.exp(-4)) 

                    log_probs_cv = myrfc.predict_log_proba(X_CV)    
                    c0 = log_probs_cv[:,0] < -4
                    c1 = log_probs_cv[:,1] < -4
                    log_probs_cv[c0,0] = -4
                    log_probs_cv[c0,1] = np.log(1-np.exp(-4)) 
                    log_probs_cv[c1,1] = -4
                    log_probs_cv[c1,0] = np.log(1-np.exp(-4)) 

                    self.eval_matrix.loc[jd,jt].loc[('Training', 'Cross entropy')] = (-log_probs_tr[:,1].T.dot(y_train)-log_probs_tr[:,0].T.dot(~y_train))/float(len(y_train))
                    self.eval_matrix.loc[jd,jt].loc[('CV', 'Cross entropy')] = (-log_probs_cv[:,1].T.dot(y_CV)-log_probs_cv[:,0].T.dot(~y_CV))/float(len(y_CV))