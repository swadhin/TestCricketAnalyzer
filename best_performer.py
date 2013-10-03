#!/usr/bin/python

from igraph import *
import operator
import sys
from math import sqrt
from math import ceil

player_dict={}

if len(sys.argv) != 4:
        print "Usage: <Program_name> <IN:input_file of Relative Performance Score> <IN:Threshold Value : Min Number of Matches Played> <OUT: Output Ranking File>"
        exit(0)

input_file              = sys.argv[1]


#input map in wkt format reading
in_handle               = open(input_file,'r')
content                 = in_handle.readlines()
in_handle.close()

threshold = int(sys.argv[2])

#out_handle              = open(output_file,'w')

g = Graph();
g.vs["player_or_match"] = [];
g.vs["type"] = [];
g.vs["pl_id"] = [];
g.vs["mt_id"] = [];
g.vs["tm_id"] = [];
g.es["weight"] = [];

for line in content:
        line_parts = line.strip().split(':')
	player_id = 0;
	team_name = 0;
	edge_weight = 0;
	match_id = 0;
	player_name = 0;
	#print line_parts
	
	#print len(line_parts)
	for elem in range(len(line_parts)):
		texx = line_parts[int(elem)];
		texx = texx.replace(' ','');
		
		if elem == 0:
			match_id = texx; #match id
		elif elem == 1:
			player_name = texx
		elif elem == 2:
			player_id = texx; #player_id
		elif elem == 4:
			team_name = texx; #team_name
		elif elem == 9:
			edge_weight = texx; #edge weight
	
	if player_id not in g.vs["pl_id"]:
		g.add_vertices(1);
		g.vs[len(g.vs)-1]["pl_id"] = player_id;
		g.vs[len(g.vs)-1]["player_or_match"] = "p";
		g.vs[len(g.vs)-1]["type"] = True;
		g.vs[len(g.vs)-1]["tm_id"] = team_name;
		g.vs[len(g.vs)-1]["mt_id"] = -1;
	
	if match_id not in g.vs["mt_id"]:
		g.add_vertices(1);
		g.vs[len(g.vs)-1]["mt_id"] = match_id;
		g.vs[len(g.vs)-1]["player_or_match"] = "m";
		g.vs[len(g.vs)-1]["type"] = False;
		g.vs[len(g.vs)-1]["pl_id"] = -1;
		g.vs[len(g.vs)-1]["tm_id"] = -1;
	
	
	player_indx = (g.vs.find(pl_id = player_id)).index
	#print player_indx
	match_indx = (g.vs.find(mt_id = match_id)).index
	#print match_indx
	
	g.add_edge(player_indx,match_indx)
	g.es[len(g.es) - 1]["weight"] = edge_weight; 

#print "Total Vertex Size : ",len(g.vs)
#print "Total Edge Size : ",len(g.es)

#bipartite built here access the weights of these vertices of the players
#dictionary list

#format is player_id:team_id:weighted_score:ranking

dict={}

for i in range(len(g.vs["pl_id"])):
  if g.vs[i]["mt_id"]==-1 and g.vs[i].outdegree()>=threshold:		#accessing players here
    s=0
    for ele in g.get_adjlist()[i]:
      s=s+int(g[i,ele])
    #dict[g.vs[i]["pl_id"]]=[int(g.vs[i]["pl_id"]),int(g.vs[i]["tm_id"]),float(s/float(g.vs[i].outdegree()))]
    dict[g.vs[i]["pl_id"]]=[int(g.vs[i]["pl_id"]),int(g.vs[i]["tm_id"]),float(s/float(g.vs[i].outdegree()))+float(float(g.vs[i].outdegree())/float(threshold))]

list=sorted(dict.items(),key=lambda e: e[1][2])
list.reverse()

for line in content:
  l=line.split(':')
  player_dict[int(l[2].strip())]=l[1].strip()
  

i=1

fout = open(sys.argv[3],"w")

for lst in list:
  fout.write( str(i) + ":" + str(lst[1][0]).strip(' ') + ':' + str(player_dict[lst[1][0]]).strip(' ') + ':' + str(lst[1][1]).strip(' ') + "\n" )
  #print lst[1][0],':',player_dict[lst[1][0]],':',lst[1][1],':',lst[1][2],':',i
  i+=1

fout.close()

#print player_dict
