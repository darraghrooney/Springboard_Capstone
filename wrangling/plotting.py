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
