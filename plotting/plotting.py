import os
import numpy as np
import scipy.stats as sps 
import pandas as pd

from sklearn.linear_model import LinearRegression, LogisticRegression

import matplotlib.pyplot as plt

import wrangling.attempt_manager as am


def sal_PT_plot():

	AM = am.attempt_manager()
	AM.Load()
	h_sal = pd.Series(AM.home_OI_sal)
	a_sal = pd.Series(AM.away_OI_sal)
	h_PT = pd.Series(AM.home_OI_PT)
	a_PT = pd.Series(AM.away_OI_PT)

	fig = plt.figure()
	fig.suptitle('Salaries and playing time for opposing on-ice players', fontsize=16, x=0.75, y = 0.8)

	ax1 = fig.add_axes([.1,.1,0.6,0.6])

	ax1.scatter(h_sal,a_sal, alpha=0.05)
	ax1.set_xlabel('Avg. home salary',fontsize=12)
	ax1.set_ylabel('Avg. away salary', fontsize=12)

	ax2 = fig.add_axes([.85,.1,0.6,0.6])
	ax2.scatter(h_PT,a_PT, alpha=0.05)
	ax2.set_xlabel('Avg. home PT',fontsize=12)
	ax2.set_ylabel('Avg. away PT', fontsize=12)
	plt.show()

def OI_diff_plot():
	AM = am.attempt_manager()
	AM.Load()
	away_indices = list(set(range(0,len(AM.attempt_type))) - set(AM.home_indices))
	away_indices.sort()
	sal_diff = pd.DataFrame()
	sal_diff_home = list(pd.Series(AM.home_OI_sal)[AM.home_indices]- \
                     pd.Series(AM.away_OI_sal)[AM.home_indices])
	sal_diff_away = list(pd.Series(AM.home_OI_sal)[away_indices] - \
                     pd.Series(AM.away_OI_sal)[away_indices])
	PT_diff_home = pd.Series(AM.home_OI_PT)[AM.home_indices] - \
                     pd.Series(AM.away_OI_PT)[AM.home_indices]
	PT_diff_away = pd.Series(AM.home_OI_PT)[away_indices] - \
                     pd.Series(AM.away_OI_PT)[away_indices]

	fig = plt.figure()
	fig.suptitle('Home-Away On-Ice Player Differentials', fontsize=16, x=0.75, y=.8)
	ax1 = fig.add_axes([.1,.1,0.6,0.6])
	ax2 = fig.add_axes([.85,.1,0.6,0.6])
	
	ax1.boxplot([sal_diff_home,sal_diff_away])
	ax2.boxplot([PT_diff_home,PT_diff_away])

	ax1.set_ylabel('Avg. salary difference', fontsize=12)
	ax2.set_ylabel('Avg. PT difference', fontsize=12)
	ax1.set_xticklabels(['Home','Away'], fontsize=12 )
	ax2.set_xticklabels(['Home','Away'], fontsize=12 )
	plt.show()