#!/usr/bin/python

import sys
from math import sqrt
from math import ceil

if len(sys.argv) != 2:
        print "Usage: <Program_name> <IN:input_file : File containing Results of Matches >"
        exit(0)

input_file              = sys.argv[1]


#input map in wkt format reading
in_handle               = open(input_file,'r')
content                 = in_handle.readlines()
in_handle.close()

team_success_score = {}

success_score = []

for line in content:
	line_vals = line.strip().split(':');
	
	team_id1 = line_vals[2].replace(' ','');
	team_id2 = line_vals[5].replace(' ','');
	
	team1_result = int(line_vals[3].replace(' ',''))
	team2_result = int(line_vals[6].replace(' ',''))

	val = team1_result - team2_result;

	success_score_team1 = []
	success_score_team2 = []
	
	if team_id1 in team_success_score:
		success_score_team1 = team_success_score[team_id1];
		success_score_team1[0] += 1;
	
		if val == 1:
			success_score_team1[1] += 1;
		elif val == 0:
			success_score_team1[2] += 1;
		else:
			success_score_team1[3] += 1;

		team_success_score[team_id1] = success_score_team1;
	else:
		success_score_team1 = [ 1, 0, 0, 0];
	
		if val == 1:
			success_score_team1[1] += 1;
		elif val == 0:
			success_score_team1[2] += 1;
		else:
			success_score_team1[3] += 1;
                
		team_success_score[team_id1] = success_score_team1;

	if team_id2 in team_success_score:
		success_score_team2 = team_success_score[team_id2];
		success_score_team2[0] += 1;

		if val == -1:
			success_score_team2[1] += 1;
		elif val == 0:
			success_score_team2[2] += 1;
		else:
			success_score_team2[3] += 1;
		
		team_success_score[team_id2] = success_score_team2;
	else:
		success_score_team2 = [ 1, 0, 0, 0];
	
		if val == -1:
			success_score_team2[1] += 1;
		elif val == 0:
			success_score_team2[2] += 1;
		else:
			success_score_team2[3] += 1;
                team_success_score[team_id2] = success_score_team2;


#print team_success_score

team_success_rate = {}

for key in team_success_score:
	score_arr = team_success_score[key]
	#rate = (float(score_arr[1])*1 + float(score_arr[2])*0.5)/float(score_arr[0])
	rate = (float(score_arr[1])*2 + float(score_arr[2])*1)/float(score_arr[0])
	team_success_rate[key] = rate

#print team_success_rate	

count = 1
for key, value in sorted(team_success_rate.iteritems(), key=lambda (k,v): (v,k), reverse=True):
    print "%s:%s:%s" % (count,key, value)
    count += 1

'''
clique_result_dict = {'1': 2011654, '25': 10069, '3': 1126935, '2': 3999011, '5': 219179, '4': 1674008, '7': 577446, '6': 1505418, '9': 20803, '8': 568248};

#for key in clique_result_dict:
#	clique_result_dict[key] = float(float(clique_result_dict[key]) / float(team_success_score[key][0]));

print "\n-------------------------------------------------------\n"
for key, value in sorted(clique_result_dict.iteritems(), key=lambda (k,v): (v,k)):
    print "%s: %s" % (key, value)

clique_result_dict1 = {'1': 38504543, '25': 37989, '3': 10600203, '2': 73953639, '5': 1286536, '4': 41207166, '7': 2871737, '6': 19180036, '9': 154547, '8': 2658978};
print "\n-------------------------------------------------------\n"
for key, value in sorted(clique_result_dict1.iteritems(), key=lambda (k,v): (v,k)):
    print "%s: %s" % (key, value)

clique_result_dict2 = {'1': 1094547, '25': 4255, '3': 860394, '2': 2161285, '5': 120812, '4': 959185, '7': 317153, '6': 893320, '9': 17665, '8': 407688};
print "\n-------------------------------------------------------\n"
for key, value in sorted(clique_result_dict2.iteritems(), key=lambda (k,v): (v,k)):
    print "%s: %s" % (key, value)
'''
