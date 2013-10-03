#!/usr/bin/python

from igraph import *

import sys
from math import sqrt
from math import ceil

if len(sys.argv) != 3:
        print "Usage: <Program_name> <IN:input_file> <IN:Threshold Value>"
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

print " Total Vertex Size : "	
print len(g.vs)
print " Total Edge Size : "	
print len(g.es)

#print g.get_edgelist();
print " Graph Weighted (?) : "
print g.is_weighted();
print " Graph Bipartite (?) : "
print g.is_bipartite();

g1, g2 = g.bipartite_projection();

#g1 => Match Side One Mode Projection
#g2 => Player Side One Mode Projection

#print g1.vs["type"]
#print g2.vs["type"]

#print g2.k_core();

#Total Bipartite Graph
#layout = g.layout("kk")
#color_dict = {"m": "blue", "p": "pink"}
#plot(g, layout = layout, vertex_color = [color_dict[pl_mt] for pl_mt in g.vs["player_or_match"]])		

#Thresholded Projection ( say d = 5 )
for edge in g2.get_edgelist():
	#print edge
	edge_indx = g2.get_eid(int(edge[0]),int(edge[1]));
	#print edge_indx
	if int(g2.es[edge_indx]["weight"]) < threshold:
		g2.delete_edges(g2.es[edge_indx]);

#print g2.k_core()


all_cliques = g2.cliques();
team_wise_clique_score = {"1" : 0, "2" : 0, "3" : 0, "4" : 0, "5" : 0, "6" : 0, "7" : 0, "8" : 0, "9" : 0, "25" : 0};

for cliq in all_cliques:
	#tot_weight = 0
	#lamda_adv = 0

	for i in range(len(cliq)-1):
		edge_inx = g2.get_eid(int(cliq[i]),int(cliq[i+1]));

		if g2.vs[int(cliq[i])]["tm_id"] == g2.vs[int(cliq[i])]["tm_id"] :
			team_wise_clique_score[g2.vs[int(cliq[i])]["tm_id"]] += g2.es[edge_inx]["weight"];
			team_wise_clique_score[g2.vs[int(cliq[i])]["tm_id"]] += 5;
	
print team_wise_clique_score
	
#color_dict = {"1": "grey", "2": "yellow", "3" : "black", "4": "pink", "5": "red", "6": "blue", "7": "green", "8": "brown", "9" : "orange", "25" : "white"}

#layout = g2.layout("kk")
#plot(g2, layout = layout,vertex_color = [color_dict[pl_mt] for pl_mt in g2.vs["tm_id"]])
