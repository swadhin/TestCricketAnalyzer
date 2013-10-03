#!/usr/bin/python

import sys
import os
#import re

for filename in os.listdir ('./'):
	
	if str(filename).endswith('.txt'):
		#print filename
		fhandle = open( str(filename), 'r')
		content = fhandle.readlines()
		fhandle.close()

		for line in content:
			if str(line).find('<meta name="description" content="Cricket scores for') != -1:
				line_conts = line.strip().split('"')
				#print line_conts
				test_year_conts = str(line_conts[3]).strip().split(' ')
				test_year = test_year_conts[len(test_year_conts) - 1]
				test_fname = "year_" +str(test_year) + ".txt"
				
				print test_year
				fhandle = open(test_fname, 'a')
				fhandle.write(filename +"\n" )
				fhandle.close()
