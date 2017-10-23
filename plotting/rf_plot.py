import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

import wrangling.attempt_manager as am

def rf_plot(RFs):

    fig = plt.figure()
    fig.suptitle('Performance of Random Forest Algorithms', fontsize=16, x=0.75, y=1.5)
    ax1 = fig.add_axes([.1,.8,0.55,0.55])
    ax2 = fig.add_axes([.75,.8,0.55,0.55])
    ax3 = fig.add_axes([.1,.1,0.55,0.55])
    ax4 = fig.add_axes([.75,.1,0.55,0.55])
    
    cc = 0
    colors = ['green', 'red', 'blue', 'magenta', 'black']

    for d in RFs.ds:
	    ax1.scatter(RFs.n_t, RFs.eval_matrix.loc[d].loc[:,('Training', 'Scores')], color = colors[cc], label='Trees with depth ' + str(d) )
	    ax3.scatter(RFs.n_t, RFs.eval_matrix.loc[d].loc[:,('CV', 'Scores')], color = colors[cc]  )
	    ax2.scatter(RFs.n_t, RFs.eval_matrix.loc[d].loc[:,('Training', 'Cross entropy')], color = colors[cc]  )
	    ax4.scatter(RFs.n_t, RFs.eval_matrix.loc[d].loc[:,('CV', 'Cross entropy')], color = colors[cc] )
	    cc += 1

    h, l = ax1.get_legend_handles_labels()
    fig.legend(h,l, bbox_to_anchor=(1.75,.9) )
    ax1.set_ylabel('Prediction score, training set', fontsize = 10)
    ax2.set_ylabel('Cross entropy, training set', fontsize = 10)
    ax3.set_ylabel('Prediction score, CV set', fontsize = 10)
    ax4.set_ylabel('Cross entropy, CV set', fontsize = 10)
    fig.text(.5,0,'Number of tress', fontsize = 12)

    plt.show()
