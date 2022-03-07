# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 10:21:59 2022

@author: migue
"""

import sheaf as sh
import numpy as np
import random as rand

rand.seed(9)
np.random.seed(9)
num_pts = 6
num_edges = 8
all_objects = ['Trump','Biden','Harris','Pence']
all_objects.sort()
all_attribs = ['smart','honest','experienced','charismatic']
all_attribs.sort()

politics = sh.Sheaf()
totalRel = []

for i in range(num_pts):
    totalRel.append( np.around(np.random.rand(len(all_objects), len(all_attribs)),decimals=3) )
    # initial opinions are based on agents perception of the politicians 'charisma'
    initial_vals = list(totalRel[i][:,0])
    noisy_vals = initial_vals + np.random.rand(1,len(initial_vals))/100 # multiply summand by zero to remove noise
    node_state = sh.FuzzySet(all_objects, noisy_vals.flatten())
    vertToAdd = sh.Vertex(node_state)
    politics.addVertex(i, vertToAdd)
    
         
for i in range(num_edges):
    rand_edge = (1,2)
    while (rand_edge in list(politics.edges)) or (rand_edge[1] < rand_edge[0]):
        rand_edge = tuple(rand.sample(range(num_pts),2))
    edgeToAdd = sh.Edge(all_attribs)
    politics.addEdge(rand_edge[0], rand_edge[1], edgeToAdd)
    
for pair in list(politics.relations):
    objects = politics.relations[pair].fuzzyRel.objects
    attribs = politics.relations[pair].fuzzyRel.attribs
    indices = [ all_attribs.index(string) for string in attribs]
    indices.sort()
    cols = [totalRel[ pair[0] ][:,i] for i in indices]
    valMatrix = np.stack(cols, axis = -1)
    politics.addRelation(pair[0], pair[1], valMatrix)

# labels = {0:'0',1:'1',2:'2',3:'3'}