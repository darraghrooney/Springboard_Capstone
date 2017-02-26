import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

import wrangling.attempt_manager as am

C = [ pow(10, c/2.) for c in range(-10,10)]

def train_plot(SLS):

	fig = plt.figure()
	fig.suptitle('Performance of Algorithms on the Training Data', fontsize=16, x=0.75, y=1.5)
	ax3 = fig.add_axes([.1,.1,0.6,0.6])
	ax4 = fig.add_axes([.85,.1,0.6,0.6])
	ax1 = fig.add_axes([.1,.8,0.6,0.6])
	ax2 = fig.add_axes([.85,.8,0.6,0.6])
	ax1.scatter(np.log(C), SLS.eval_matrix[ 'Corsis', 'Training', 'Scores'], color='red', label='Corsi only' )
	ax1.scatter(np.log(C), SLS.eval_matrix[ 'plus_PT', 'Training', 'Scores'], color='green', label='Corsi + PT' )
	ax1.scatter(np.log(C), SLS.eval_matrix[ 'all', 'Training', 'Scores'], color='blue' , label= 'Corsi + PT + salary')
	ax2.scatter(np.log(C), SLS.eval_matrix[ 'Corsis', 'Training', 'Cross entropy'], color='red' )
	ax2.scatter(np.log(C), SLS.eval_matrix[ 'plus_PT', 'Training', 'Cross entropy'], color='green' )
	ax2.scatter(np.log(C), SLS.eval_matrix[ 'all', 'Training', 'Cross entropy'], color='blue' )
	ax3.scatter(np.log(C), SLS.eval_matrix[ 'Corsis', 'Training', 'Scores'], color='red' )
	ax3.scatter(np.log(C), SLS.eval_matrix[ 'plus_PT', 'Training', 'Scores'], color='green' )
	ax3.scatter(np.log(C), SLS.eval_matrix[ 'all', 'Training', 'Scores'], color='blue' )
	ax3.set_ylim([.6135,.6155])
	ax4.scatter(np.log(C), SLS.eval_matrix[ 'Corsis', 'Training', 'Cross entropy'], color='red' )
	ax4.scatter(np.log(C), SLS.eval_matrix[ 'plus_PT', 'Training', 'Cross entropy'], color='green' )
	ax4.scatter(np.log(C), SLS.eval_matrix[ 'all', 'Training', 'Cross entropy'], color='blue' )
	ax4.set_ylim([.651,.654])
	h, l = ax1.get_legend_handles_labels()
	fig.legend(h,l, bbox_to_anchor=(2,1) )
	ax1.set_ylabel('Prediction score', fontsize = 12)
	ax3.set_ylabel('Prediction score', fontsize = 12)
	ax2.set_ylabel('Prediction score', fontsize = 12)
	ax4.set_ylabel('Cross-entropy', fontsize = 12)
	fig.text(.5,0,'Negative log of regularization strength', fontsize = 12)

	plt.show()

def cv_plot(SLS):

	fig = plt.figure()
	fig.suptitle('Performance of Algorithms on the Cross-Validation Data', fontsize=16, x=0.75, y=1.5)
	ax3 = fig.add_axes([.1,.1,0.6,0.6])
	ax4 = fig.add_axes([.85,.1,0.6,0.6])
	ax1 = fig.add_axes([.1,.8,0.6,0.6])
	ax2 = fig.add_axes([.85,.8,0.6,0.6])
	ax1.scatter(np.log(C), SLS.eval_matrix[ 'Corsis', 'CV', 'Scores'], color='red', label='Corsi only' )
	ax1.scatter(np.log(C), SLS.eval_matrix[ 'plus_PT', 'CV', 'Scores'], color='green', label='Corsi + PT' )
	ax1.scatter(np.log(C), SLS.eval_matrix[ 'all', 'CV', 'Scores'], color='blue' , label= 'Corsi + PT + salary')
	ax2.scatter(np.log(C), SLS.eval_matrix[ 'Corsis', 'CV', 'Cross entropy'], color='red' )
	ax2.scatter(np.log(C), SLS.eval_matrix[ 'plus_PT', 'CV', 'Cross entropy'], color='green' )
	ax2.scatter(np.log(C), SLS.eval_matrix[ 'all', 'CV', 'Cross entropy'], color='blue' )
	ax3.scatter(np.log(C), SLS.eval_matrix[ 'Corsis', 'CV', 'Scores'], color='red' )
	ax3.scatter(np.log(C), SLS.eval_matrix[ 'plus_PT', 'CV', 'Scores'], color='green' )
	ax3.scatter(np.log(C), SLS.eval_matrix[ 'all', 'CV', 'Scores'], color='blue' )
	ax3.set_ylim([.624,.628])
	ax4.scatter(np.log(C), SLS.eval_matrix[ 'Corsis', 'CV', 'Cross entropy'], color='red' )
	ax4.scatter(np.log(C), SLS.eval_matrix[ 'plus_PT', 'CV', 'Cross entropy'], color='green' )
	ax4.scatter(np.log(C), SLS.eval_matrix[ 'all', 'CV', 'Cross entropy'], color='blue' )
	ax4.set_ylim([.64,.643])
	h, l = ax1.get_legend_handles_labels()
	fig.legend(h,l, bbox_to_anchor=(2,1) )
	ax1.set_ylabel('Prediction score', fontsize = 12)
	ax3.set_ylabel('Prediction score', fontsize = 12)
	ax2.set_ylabel('Prediction score', fontsize = 12)
	ax4.set_ylabel('Cross-entropy', fontsize = 12)
	fig.text(.5,0,'Negative log of regularization strength', fontsize = 12)

	plt.show()
