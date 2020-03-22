# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 12:57:06 2020

Download data from https://snap.stanford.edu/data/sx-stackoverflow.html

@author: daipe
"""
import networkx as nx
from collections import defaultdict
import collections
import time
import datetime
#from pipelines.graphs import getGraph


def loadData(edge_file, thr):
        
    edge_list = []
    edges = defaultdict(list)
    edges_nx = []
    
    with open (edge_file, 'r') as e_file:
        edge_list = e_file.readlines()
    
    
    cnt = 0
    cnt_max = 0
    edgeWeights = collections.defaultdict(lambda: collections.Counter())
    
    
    for edge in edge_list:
		if cnt % int(thr/10) == 0:
				print(' - Processed {}'.format(cnt))

		if cnt > thr:
				break

		try:
				from_, to_ = edge.split('\t')
				from_, to_ = int(from_), int(to_[:-1])
		except:
				#print(edge.split(' '))
				from_,to_,_ = edge.split(' ')
				from_, to_ = int(from_), int(to_)
			
		if from_ > cnt_max:
				cnt_max = from_
		if to_ > cnt_max:
				cnt_max = to_
		edges[from_].append(to_)
		edgeWeights[from_][to_] += 1.0
		edges_nx.append((from_, to_))
		cnt += 1
			
    print('max_value is {}, Total number of edges is {}'.format(cnt_max, len(edge_list)))
		
    return edges_nx

# In[]

infile ="sx-stackoverflow-a2q.txt"
thr = 9990000 # 17823525
edges_nx = loadData(infile, thr)

G=nx.Graph()
#G.add_nodes_from([2,3])
G.add_edges_from(edges_nx)

print('=> Staring PageRank')
print(datetime.datetime.now())

tic = time.time()
pr = nx.pagerank(G, alpha=0.9)

print('=> PageRank take time %s with amount of data %s' % (time.time() - tic, thr))

a = sorted(pr.items(), key=lambda x: x[1])

print(a[-10:])