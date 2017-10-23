import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

import wrangling.attempt_manager as am

def comp_plot(BLS):

	C = BLS.Cs

	fig = plt.figure()
	fig.suptitle('Performance of Big Logistic Regression', fontsize=16, x=0.75, y=1.5)
	ax1 = fig.add_axes([.1,.8,0.6,0.6])
	ax2 = fig.add_axes([.85,.8,0.6,0.6])
	ax1.scatter(np.log(C), BLS.eval_matrix[ 'Training', 'Scores'], color='red', label='Training' )
	ax1.scatter(np.log(C), BLS.eval_matrix[ 'CV', 'Scores'], color='green', label='Cross-validation' )
	ax2.scatter(np.log(C), BLS.eval_matrix[ 'Training', 'Cross entropy'], color='red', label='Training' )
	ax2.scatter(np.log(C), BLS.eval_matrix[ 'CV', 'Cross entropy'], color='green', label='Cross-validation' )
	h, l = ax1.get_legend_handles_labels()
	fig.legend(h,l, bbox_to_anchor=(2,.7) )
	ax1.set_ylabel('Prediction score', fontsize = 12)
	ax2.set_ylabel('Cross-entropy', fontsize = 12)
	fig.text(.5,0.7,'Negative log of regularization strength', fontsize = 12)
	plt.show()