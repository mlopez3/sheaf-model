# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 10:21:59 2022

@author: migue
"""

import sheaf as sh
import numpy as np


all_objects = ['Galaxy','Iphone','Pixel']
all_objects.sort()
all_attribs = ['battery','camera','popularity']
all_attribs.sort()

phones = sh.Sheaf(residuum = 'prod')
totalRel = []

totalRel.append( np.array([[0.7, 0.8, 0.6],
                           [0.7, 0.9, 0.9],
                           [0.9, 0.7, 0.4]]))
initial_op1 = [0.5,0.5,0.5]
node_state1 = sh.FuzzySet(all_objects,initial_op1)
vertToAdd1 = sh.Vertex(node_state1)
phones.addVertex(0,vertToAdd1)

totalRel.append( np.array([[0.7, 0.4, 0.2],
                           [0.7, 0.6, 1],
                           [0.7, 0.3, 0.1]]))
initial_op2 = [0.2,0.9,0.1]
node_state2 = sh.FuzzySet(all_objects,initial_op2)
vertToAdd2 = sh.Vertex(node_state2)
phones.addVertex(1,vertToAdd2)

totalRel.append( np.array([[0.5, 0.7, 0.4],
                           [0.3, 0.7, 0.9],
                           [0.3, 0.7, 0.2]]))
initial_op3 = [0.3,0.8,0.4]
node_state3 = sh.FuzzySet(all_objects,initial_op3)
vertToAdd3 = sh.Vertex(node_state3)
phones.addVertex(2,vertToAdd3)

edgeToAdd = sh.Edge(all_attribs)
phones.addEdge(0,1,edgeToAdd)
phones.addEdge(0,2,edgeToAdd)
phones.addEdge(1,2,edgeToAdd)

phones.addRelation(0,(0,1),totalRel[0])
phones.addRelation(1,(0,1),totalRel[1])
phones.addRelation(0,(0,2),totalRel[0])
phones.addRelation(2,(0,2),totalRel[2])
phones.addRelation(1,(1,2),totalRel[1])
phones.addRelation(2,(1,2),totalRel[2])