#!/usr/bin/python

import urllib2
import sys, traceback
import os
import codecs
import time

#from BeautifulSoup import BeautifulSoup
from bs4 import BeautifulSoup


def crawl_cricinfo():
	
	player_page_count = 0
	player_page =0
	
	team_no_name = { '1' : 'England' , '2' : 'Australia', '3' : 'SouthAfrica', '4' : 'WestIndies', '5' : 'NewZealand', '6' : 'India', '7' : 'Pakistan', '8' : 'SriLanka', '9' : 'Zimbabwe', '25' : 'Bangladesh' };
	fname = 0

	for key in team_no_name:
		player_page_count += 1

		#Go to Each Player Profile
		try:
			#http://www.espncricinfo.com/ci/content/player/caps.html?country=6;class=1
			print "Downloading .........."
			temp_player_page = urllib2.urlopen("http://www.espncricinfo.com/ci/content/player/caps.html?country=" + key + ";class=1")
			fname = "./outDir/teams/" + team_no_name[key] + ".html"
			print fname
			player_page = temp_player_page.read()
			fhandle = open(fname, 'w')
			print "Writing ...."
			fhandle.write(player_page)
			fhandle.close()
			os.system("dos2unix " + fname)
			#introduce delay	
			time.sleep(0.0001)
		except urllib2.URLError,error:
			print "While Retrieving Player Page No. " + str(key) + ", got URL Error."
		except httplib.BadStatusLine:
    			print "Could not fetch %s due to BAD STATUS" % url

		soup_player = BeautifulSoup(player_page)

		for tag in soup_player.find_all("li", class_= "ciPlayername"):
			url_part = str(tag).strip().split('"')[5]
			url = "http://www.espncricinfo.com" + url_part
			pl_id = url.strip().split("/")[-1]

			#Getting Each Player Info for Test for each country
			try:
                        	temp_player_page = urllib2.urlopen(url)
				dir_path_name = "./cap_dir/players/" + team_no_name[key]

				try: 
    					os.makedirs(dir_path_name)
				except OSError:
    					if not os.path.isdir(dir_path_name):
                        			raise
				fname = dir_path_name + "/" + pl_id
                        	player_page = temp_player_page.read()
                        	fhandle = open(fname, 'w')
                        	fhandle.write(player_page)
                        	fhandle.close()
                        	os.system("dos2unix " + fname)
                        	#introduce delay        
                        	time.sleep(0.0001)
                	except urllib2.URLError,error:
                        	print "While Retrieving Player Page No. " + str(key) + ", got URL Error."
                	except httplib.BadStatusLine:
                        	print "Could not fetch %s due to BAD STATUS" % url


			departments = [ 'batting', 'bowling', 'fielding' ];

			for elem in departments:
				inning_cnt = 1
				
				while  inning_cnt < 3:

					fname = str(elem)
					#http://stats.espncricinfo.com/ci/engine/player/35320.html?class=1;template=results;type=batting;view=innings
					#Go to Each Player Profile
					try:
						temp_player_page = 0

						if inning_cnt == 1:
							inning_cnt += 1
							url_rec = "http://stats.espncricinfo.com/ci/engine/player/" + pl_id + "?class=1;template=results;type=" + str(elem)
							temp_player_page = urllib2.urlopen(url_rec)
							fname = fname + "_record.txt"
						else:
							inning_cnt += 1
							url_inn = "http://stats.espncricinfo.com/ci/engine/player/" + pl_id + "?class=1;template=results;type=" + str(elem) + ";view=innings"
							print url_inn
							temp_player_page = urllib2.urlopen(url_inn)
							fname = fname + "_innings.txt"
					
						player_page = temp_player_page.read()
						#introduce delay	
						time.sleep(0.0001)

					except urllib2.URLError,error:
						print "While Retrieving Page " + str(pl_id) + ", got URL Error."
						player_page = 0
						continue

					except httplib.BadStatusLine:
    						print "Could not fetch %s due to BAD STATUS" % url
						player_page = 0
						continue

					if player_page != 0 :
						dir_path_name = "./cap_dir/player_database/" + team_no_name[key] + "/" + str(pl_id).strip().split('.')[0]
						print dir_path_name
						try: 
    							os.makedirs(dir_path_name)
						except OSError:
    							if not os.path.isdir(dir_path_name):
                        					raise

                        			fhandle = open( dir_path_name + "/" + fname, 'w')
                        			fhandle.write(player_page)
                        			fhandle.close()
                        			os.system("dos2unix " + dir_path_name + "/" + fname)
						player_page = 0


def main():
	crawl_cricinfo();

if __name__ == "__main__":
    main()
