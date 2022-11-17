#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verification of the weighted sheaf laplcian.
"""
import sheaf as sh
import numpy as np
import random as rand
import networkx as nx

rand.seed(10)
np.random.seed(10)
all_objects = ['A','B']
all_objects.sort()
all_attribs = ['a','b']
all_attribs.sort()

verify = sh.Sheaf()

rels = []

# Add vetrices
# For agent 0
initial_op_0 = [0.9,0.1] # define agent 0's initial opinion vector
initial_state_0 = sh.FuzzySet(all_objects,initial_op_0)# Associate objects to numbers
rels.append(np.array([ [ 0.9, 0.3],   #
                       [ 0.8, 0.1]])
            )                    
vertToAdd_0 = sh.Vertex(initial_state_0) # create vertex object 
verify.addVertex(0,vertToAdd_0)  # add vertex to sheaf

# For agent 1
initial_op_1 = [0.9,0.9] # define agent 0's initial opinion vector
initial_state_1 = sh.FuzzySet(all_objects,initial_op_1)# Associate objects to numbers
rels.append(np.array([ [ 0.9, 0.3],   
                       [ 0.8, 0.1]])
            )                    
vertToAdd_0 = sh.Vertex(initial_state_1) # create vertex object 
verify.addVertex(1,vertToAdd_0)  # add vertex to sheaf

# Add an edge
edgeToAdd = sh.Edge(all_attribs, weights = [1,1,0.5,0.5])
verify.addEdge(0,1,edgeToAdd)

verify.addRelation(0,(0,1),rels[0])
verify.addRelation(1,(0,1),rels[1])

#verify.drawIntensity('A')



