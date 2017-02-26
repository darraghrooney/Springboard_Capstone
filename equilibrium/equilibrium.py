import numpy as np
import pandas as pd
from scipy.sparse import *

train_fn = '../data/csr_Training.npz'

class ForceMatrix(object):
    
    force_matrix = np.matrix([])
    pp_ratios = pd.Series([1., 1.], index = ['Up one', 'Up two/three'])
    ha_ratio = 1
    fm_fn = '../data/Forces.npz'
    
    def HA_Ratio(self):
        print 'Calculating HA ratio'
        loader = np.load(train_fn)
        is_for_home = loader['is_for_home']
        self.ha_ratio = sum(is_for_home)/float(sum( ~is_for_home ))

    def PP_Ratios(self):
        print 'Calculating PP ratios'
        loader = np.load(train_fn)
        train_matrix = csr_matrix( (loader['training_matrix_data'], loader['training_matrix_indices'], 
                                    loader['training_matrix_indptr']), shape = loader['training_matrix_shape'])
        is_for_home = loader['is_for_home']
        self.force_matrix = np.zeros( [train_matrix.shape[1]+1, train_matrix.shape[1]])
        pp_att = [0,0]
        sh_att = [0,0]
        
        for j in range(0, len(is_for_home)):
            attempt = train_matrix.getrow(j)
            hp = sum(attempt.indices < train_matrix.shape[1]/2)
            ap = attempt.indices.shape[0] - hp
            if hp == ap:
                pass
            elif is_for_home[j]:
                if hp == ap + 1:
                    pp_att[0] += 1
                elif hp == ap - 1:
                    sh_att[0] += 1
                elif hp >= ap + 2:
                    pp_att[1] += 1
                else:
                    sh_att[1] += 1
            else:
                if hp == ap - 1:
                    pp_att[0] += 1
                elif hp == ap + 1:
                    sh_att[0] += 1
                elif hp <= ap - 2:
                    pp_att[1] += 1
                else:
                    sh_att[1] += 1
        for j in [0,1]:
            self.pp_ratios[j] = pp_att[j] / float(sh_att[j])
        
    def CreateForces(self):
        
        loader = np.load(train_fn)
        train_matrix = csr_matrix( (loader['training_matrix_data'], loader['training_matrix_indices'], 
                                    loader['training_matrix_indptr']), shape = loader['training_matrix_shape'])
        is_for_home = loader['is_for_home']
        no_pl = train_matrix.shape[1]/2
        self.force_matrix = np.zeros( [no_pl+1, no_pl])
        self.force_matrix[no_pl, : ] = np.ones([1, no_pl])
        
        for j in range(0, len(is_for_home)):
            print 'Processing attempt {}'.format(j)
            attempt = train_matrix.getrow(j)
            hp = attempt.indices[attempt.indices < no_pl ]
            ap = attempt.indices[attempt.indices >= no_pl ]
            hp_no = len(hp)
            ap_no = len(ap)
            exp_ratio = self.ha_ratio

            if hp_no == ap_no:
                pass
            elif hp_no == ap_no+1:
                exp_ratio *= self.pp_ratios[0]
            elif hp_no >= ap_no+2:
                exp_ratio *= self.pp_ratios[1]
            elif hp_no == ap_no-1:
                exp_ratio /= self.pp_ratios[0]
            elif hp_no <= ap_no-2:
                exp_ratio /= self.pp_ratios[1]
            h_points = 2*exp_ratio / float(1+exp_ratio)      
            a_points = 2 - h_points
            
            for k1 in hp:
                for k2 in ap:
                    if is_for_home[j]:
                        self.force_matrix[k1, k2 - no_pl ] += h_points
                    else:
                        self.force_matrix[k2 - no_pl, k1 ] += a_points

        for j in range(0, self.force_matrix.shape[1]):
            for i in range(0,self.force_matrix.shape[0]-1):
                if i == j:
                    pass
                self.force_matrix[i,j] *= self.force_matrix[i,j]
                self.force_matrix[j,j] -= self.force_matrix[i,j]

        
    def Save(self):
        np.savez(self.fm_fn, force_matrix=self.force_matrix, ha_ratio = self.ha_ratio, pp_ratios = self.pp_ratios)
                

class Equilibrium(object):

    fm_fn = '../data/Forces.npz'
    train_fn = '../data/csr_Training.npz'
    cv_fn = '../data/csr_CV.npz'
    test_fn = '../data/csr_Test.npz'

    eq_fn = '../data/Equilibrium.csv'
    force_matrix = np.load(fm_fn)['force_matrix']
    force_matrix[355,355] = 1
    equilibrium_r = np.zeros( [force_matrix.shape[1], 1] )
    adjust_CF = np.zeros( [force_matrix.shape[1], 1] )
    
    def FindEq(self):
        b = np.zeros([self.force_matrix.shape[0], 1])
        b[ self.force_matrix.shape[0] - 1, 0 ] = self.force_matrix.shape[1]
        b[355] = 1
        self.equilibrium_r = np.linalg.lstsq(self.force_matrix, b)[0]
        
    def AdjustCF(self):
        self.adjust_CF = self.equilibrium_r / (self.equilibrium_r + 1)
        
    def Save(self):
        df = pd.DataFrame( np.append(self.equilibrium_r, self.adjust_CF, axis = 1 ), 
            columns = ['Equilibrium ratio', 'Adjusted CF'], index = np.load(self.train_fn)['non_goalies'])
        df.to_csv(self.eq_fn)

    def Load(self):
        df = pd.read_csv(self.eq_fn)
        self.equilibrium_r = np.array(df['Equilibrium ratio'])
        self.adjust_CF = np.array(df['Adjusted CF'])

    def CreateFeatures(self, split):

        sp_fn = ''
        prefix = split

        if split == 'training':
            sp_fn = self.train_fn
        elif split == 'cv':
            sp_fn = self.cv_fn
            prefix = 'CV'
        else:
            sp_fn = self.test_fn

        loader = np.load( sp_fn )
        att_matrix = csr_matrix((loader[prefix + '_matrix_data'],loader[prefix + '_matrix_indices'],
            loader[prefix + '_matrix_indptr']), shape = loader[prefix + '_matrix_shape'])

        home_feature = list()
        away_feature = list()
        
        for j in range(0, att_matrix.shape[0]):
            if (j-1)%10000 == 0:
                print 'Processing attempt {}'.format(j-1)
            att = att_matrix.getrow(j)
            sum_home_r = 0
            sum_away_r = 0
            
            for i in att.indices:
                if i < self.equilibrium_r.shape[0]:
                    sum_home_r += self.equilibrium_r[i]
                else:
                    sum_away_r += self.equilibrium_r[i - self.equilibrium_r.shape[0]]
            home_feature.append(sum_home_r)
            away_feature.append(sum_away_r)
            
        features = pd.DataFrame(np.array([home_feature, away_feature]).T, 
                                     columns = ['Sum of home r', 'Sum of away r'])
        features.to_csv('../data/Eq_Feat_' + prefix + '.csv', index = False)

EQ = Equilibrium()
EQ.Load()
EQ.CreateFeatures('training')
EQ.CreateFeatures('cv')
EQ.CreateFeatures('test')