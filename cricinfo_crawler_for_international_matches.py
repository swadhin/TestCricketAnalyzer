#!/usr/bin/python

import urllib2
import httplib
import sys, traceback
import os
import codecs
import time
import re

#from BeautifulSoup import BeautifulSoup
from bs4 import BeautifulSoup


def crawl_cricinfo():
	
	player_page_count = 0
	player_page =0
	
	team_no_name = { '1' : 'England' , '2' : 'Australia', '3' : 'SouthAfrica', '4' : 'WestIndies', '5' : 'NewZealand', '6' : 'India', '7' : 'Pakistan', '8' : 'SriLanka', '9' : 'Zimbabwe', '25' : 'Bangladesh' };
	fname = 0
	match_dict ={}
	player_match_bipartite_file = open("./cap_dir/team_player_id_to_match_id.txt",'w');

	for key in team_no_name:
		player_page_count += 1

#		http://stats.espncricinfo.com/ci/engine/player/35320.html?class=1;template=results;type=allround;view=match
		#Go to Each Player Profile
		try:
			#http://www.espncricinfo.com/ci/content/player/caps.html?country=6;class=1
			print "Downloading .........."
			temp_player_page = urllib2.urlopen("http://www.espncricinfo.com/ci/content/player/caps.html?country=" + key + ";class=1")
			fname = "./cap_dir/teams/" + team_no_name[key] + ".html"
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
		player_match_page = 0
		id_player = 0

		for tag in soup_player.find_all("li", class_= "ciPlayername"):
			url_part = str(tag).strip().split('"')[5]
			pl_id = url_part.strip().split("/")[-1]
			match_url = "http://stats.espncricinfo.com/ci/engine/player/" + str(pl_id) +"?class=1;template=results;type=allround;view=match"
			id_player = str(pl_id).strip().split('.')[0]

			#Getting Each Player Info for Test for each country
			try:
                        	temp_player_page = urllib2.urlopen(match_url)
				dir_path_name = "./cap_dir/players_matches_info/" + team_no_name[key]

				try: 
    					os.makedirs(dir_path_name)
				except OSError:
    					if not os.path.isdir(dir_path_name):
                        			raise

				fname = dir_path_name + "/" + pl_id
                        	player_match_page = temp_player_page.read()
                        	fhandle = open(fname, 'w')
                        	fhandle.write(player_match_page)
                        	fhandle.close()
                        	os.system("dos2unix " + fname)
                        	#introduce delay        
                        	time.sleep(0.0001)

                	except urllib2.URLError,error:
                        	print "While Retrieving Match Info of Player Page No. " + str(pl_id) + ", got URL Error."
                	except httplib.BadStatusLine:
                        	print "Could not fetch %s due to BAD STATUS" % match_url

			soup_player_match = BeautifulSoup(player_match_page)

			#Getting Matches from each Player All matches File
			for elem in soup_player_match.find_all("a", { "title" : "view the scorecard for this row" }):
				#print elem
				#<a href="/ci/engine/match/62429.html" title="view the scorecard for this row">Test # 34</a>
				url_part = str(elem).strip().split('"')[1]
				url_mtch = "http://www.espncricinfo.com" + str(url_part)
				match_id = str(url_mtch.strip().split("/")[-1]).strip().split('.')[0]
				print url_mtch
				print match_id
				match_page = 0

				file_str = str(key) + ":" + str(id_player) + ":" + str(match_id) + "\n"
				player_match_bipartite_file.write(file_str)

				if str(match_id) not in match_dict:
					match_dict[str(match_id)] = 1

					try:
                                		temp_player_page = urllib2.urlopen(url_mtch)
                                		dir_path_name = "./cap_dir/matches"
														
                                		try:
                                        		os.makedirs(dir_path_name)
                                		except OSError:
                                        		if not os.path.isdir(dir_path_name):
                                                		raise

                                		fname = dir_path_name + "/" + match_id + ".txt"
                                		match_page = temp_player_page.read()
                                		fhandle = open(fname, 'w')
                                		fhandle.write(match_page)
                                		fhandle.close()
                                		os.system("dos2unix " + fname)
                                		#introduce delay        
                                		time.sleep(0.0001)
                        		except urllib2.URLError,error:
                                		print "While Retrieving Match Page No. " + str(match_id) + ", got URL Error."
                        		except httplib.BadStatusLine:
                                		print "Could not fetch %s due to BAD STATUS" % url_mtch
	player_match_bipartite_file.close()
	
def main():
	crawl_cricinfo();

if __name__ == "__main__":
    main()
