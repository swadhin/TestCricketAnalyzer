#!/usr/bin/python

from igraph import *

import sys
from math import sqrt
from math import ceil

player_dict={}

if len(sys.argv) != 4:
        print "Usage: <Program_name> <IN:input_file of Scores> <IN:Threshold Value of Matches played> <OUT: Group Performance Ranking>"
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

'''
print " Total Vertex Size : "	
print len(g.vs)
print " Total Edge Size : "	
print len(g.es)
'''
#print len(g.vs)
vertices_to_be_deleted = []

for i in range(len(g.vs)):
    #print i
    if g.vs[i]["player_or_match"] == "p":
	if g.vs[i].outdegree() < threshold:           #accessing players here
		vertices_to_be_deleted.append(g.vs[i]);

g.delete_vertices(vertices_to_be_deleted);

g1, g2 = g.bipartite_projection();

#g1 => Match Side One Mode Projection
#g2 => Player Side One Mode Projection

#No Thresholded Deletion in The One Mode Projection Graph
'''
#Thresholded Projection ( say d = 5 )
for edge in g2.get_edgelist():
	#print edge
	edge_indx = g2.get_eid(int(edge[0]),int(edge[1]));
	#print edge_indx
	if int(g2.es[edge_indx]["weight"]) < threshold:
		g2.delete_edges(g2.es[edge_indx]);
'''
#print g2.k_core()

all_cliques = g2.cliques();

print len(all_cliques)

dict={}

def check_same_team(grph,clique):
	for i in clique:
		if grph.vs[i]["tm_id"] == grph.vs[i]["tm_id"] :
			continue
		else:
			return False
	return True


for i in range(len(g2.vs)):
    
    if g2.vs[i].degree()!=0:
      s=0
      for ele in g2.get_adjlist()[i]:
        s=s+int(g2[i,ele])
    
      dict[g2.vs[i]["pl_id"]]=[int(g2.vs[i]["pl_id"]),int(g2.vs[i]["tm_id"]),float(s/float(g2.vs[i].degree()))]

for cliq in all_cliques:
  if len(cliq)>=2:            #considering cliques of size atleast 2
    for i in cliq:
      if check_same_team(g2,cliq) == True:
        dict[g2.vs[i]["pl_id"]][2] += (5*len(cliq))
      else:
        break


list=sorted(dict.items(),key=lambda e: e[1][2])
list.reverse()

#format is player_id:team_id:weighted_score:ranking
for line in content:
  l=line.split(':')
  player_dict[int(l[2].strip())]=l[1].strip()

i=1
fout = open(sys.argv[3],"w")

for lst in list:
  fout.write(str(i) + ":" + str(lst[1][0]).strip(' ') + ':' + str(player_dict[lst[1][0]]).strip(' ') + ':' + str(lst[1][1]).strip(' ') + "\n")
  #print lst[1][0],':',player_dict[lst[1][0]],':',lst[1][1],':',lst[1][2],':',i
  i+=1

fout.close()
	
#color_dict = {"1": "grey", "2": "yellow", "3" : "black", "4": "pink", "5": "red", "6": "blue", "7": "green", "8": "brown", "9" : "orange", "25" : "white"}

#layout = g2.layout("kk")
#plot(g2, layout = layout,vertex_color = [color_dict[pl_mt] for pl_mt in g2.vs["tm_id"]])
