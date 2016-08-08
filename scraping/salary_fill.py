# Cap Friendly did not have salary for a handful of players, so they had empty spaces in the directory.
# This code fills in by hand the missing numbers. Most of these numbers are the following year's salary 
# (the present year's salary not being available because of some "sliding" phenomenon in the CBA).

import pandas as pd

sal_dic = 	{
		'ALEX KHOKHLACHEV': 775000.0,
		'BRETT LERNOUT': 660000.0,
		'BUD HOLLOWAY': 575000.0,
		'DANNY DEKEYSER': 2250000.0,
		'EVGENY MEDVEDEV': 3000000.0,
		'JASON LABARBERA': 600000.0,
		'KASPERI KAPANEN':  925000.0,
		'KEVIN FIALA': 925000.0,
		'MARC-ANDRE FLEURY': 5750000.0,
		'MATTHEW O\'CONNOR': 925000.0,
		'MAX TALBOT': 1000000.0,
		'MIKKO RANTANEN': 925000.0,
		'NATHAN SCHOENFELD': 525000.0,
		'NIC PETAN': 692500.0,
		'NICK PAUL': 667500.0,
		'NIKOLAY GOLDOBIN': 925000.0,
		'NIKOLAY KULEMIN': 4250000.0,
		'OLIVER KYLINGTON': 742500.0,
		'OLLI MAATTA': 832500.0,
		'PAVEL ZACHA': 925000.0,
		'PHIL VARONE': 600000.0,
		'SERGEY KALININ': 925000.0,
		'SONNY MILANO': 925000.0,
		'TEUVO TERAVAINEN': 925000.0,
		'TREVOR VAN RIEMSDYK': 925000.0
	}

DIR_filename = '../data/Directory.csv'
Directory = pd.read_csv(DIR_filename)
Directory.rename(Directory[ 'Player'], inplace=True)

for k in sal_dic.keys():
	Directory.loc[k, 'Salary'] = sal_dic[k]

Directory.to_csv(DIR_filename, index=False)