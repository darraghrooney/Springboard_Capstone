# Code for summarizing game Corsi data. Creates a table with number of goals, shots, misses, blocks and total shot attempts
# Class for managing summaries
from . import attempt_manager
import pandas as pd

class summary_manager(attempt_manager.attempt_manager):

    summary_fn = 'data/Summary.csv'
    summary = pd.DataFrame()

    def __init__(self):
        super(summary_manager,self).Load()

    # This code is sort of ugly, but it was easier than screwing around with pandas and indexing.
    def Summarize(self):
        offset = 0
        home_g = list()
        away_g = list()
        home_s = list()
        away_s = list()
        home_m = list()
        away_m = list()
        home_b = list()
        away_b = list()

        for key in GameKeys:
            print('Processing Game {}'.format(key+1))
            a_types = self.attempt_type[ offset: (offset + self.game_counts[key]) ]
            is_for_home = [ (k in self.home_indices) for k in range(offset, offset + self.game_counts[key]) ]
            df_big = pd.DataFrame( [a_types, is_for_home], index = ['Attempt type', 'For home team'] ).T
            df_small = df_big.groupby(['Attempt type', 'For home team']).size().unstack(fill_value=0).T
            home_g.append(df_small.loc[True,'G'])
            home_s.append(df_small.loc[True,'S'])
            home_m.append(df_small.loc[True,'M'])
            home_b.append(df_small.loc[True,'B'])
            away_g.append(df_small.loc[False,'G'])
            away_s.append(df_small.loc[False,'S'])
            away_m.append(df_small.loc[False,'M'])
            away_b.append(df_small.loc[False,'B'])
            offset += self.game_counts[key]
            self.summary['Home goals'] = home_g
            self.summary['Home shots'] = home_s
            self.summary['Home misses'] = home_m
            self.summary['Home blocks'] = home_b
            self.summary['Home Corsi'] = self.summary[['Home goals','Home shots','Home misses','Home blocks']].sum(axis=1)
            self.summary['Away goals'] = away_g
            self.summary['Away shots'] = away_s
            self.summary['Away misses'] = away_m
            self.summary['Away blocks'] = away_b
            self.summary['Away Corsi'] = self.summary[['Away goals','Away shots','Away misses','Away blocks']].sum(axis=1)

    def Save(self):
	    self.summary.to_csv(self.summary_fn, index=False)

    def Load(self):
	    self.summary = pd.read_csv(self.summary_fn)

