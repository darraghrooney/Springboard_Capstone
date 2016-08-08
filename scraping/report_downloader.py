# Code for downloading play-by-play reports and event reports. This was done so that the scraping
# could be done off-line.

import requests
import os

GameKeys = range(0,1230)
Play_dir = '../data/PlayReports'
Ev_dir = '../data/EventReports'

if not os.path.exists(Play_dir): 
	os.makedirs(Play_dir)

if not os.path.exists(Ev_dir): 
	os.makedirs(Ev_dir)

for key in GameKeys:
	print 'Downloading Play Report for Game ' + str(key+1)
	url = 'http://www.nhl.com/scores/htmlreports/20152016/PL02' + str(key+1).zfill(4) + '.HTM'
	playfn = Play_dir + '/PR' + str(key+1).zfill(4) + '.txt'
	r = requests.get(url)
	rt = r.text
	playfile = open(playfn, 'w')
	playfile.write(rt)
	playfile.close()

	print 'Downloading Event Report for Game ' + str(key+1)
	url = 'http://www.nhl.com/scores/htmlreports/20152016/ES02' + str(key+1).zfill(4) + '.HTM'
	eventfn = Ev_dir + '/ER' + str(key+1).zfill(4) + '.txt'
	r = requests.get(url)
	rt = r.text
	eventfile = open(playfn, 'w')
	eventfile.write(rt)
	eventfile.close()

