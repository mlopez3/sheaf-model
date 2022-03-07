"""
Example where all agents have honest discourse, coming from
some underlying total relation. When less attributes are discussed 
the total relation is restricted to those attributes
"""

import sheaf as sh
import numpy as np
import random as rand

rand.seed(10)
np.random.seed(10)
num_pts = 4
num_edges = 4
all_objects = ['Trump','Biden','Harris','Pence']
all_objects.sort()
all_attribs = ['smart','honest','experienced','charismatic']
all_attribs.sort()

politics = sh.Sheaf()
totalRel = []

for i in range(num_pts):
    rand_num = rand.randint(1,len(all_objects))
    rand_obj = rand.sample(all_objects, rand_num)
    rand_obj.sort()
    totalRel.append( np.around(np.random.rand(len(rand_obj), len(all_attribs)),decimals=3) )
    # initial opinions are based on agents perception of the politicians 'charisma'
    initial_vals = list(totalRel[i][:,0])
    # rand_vals = [x/100 for x in rand.sample(range(0,101), rand_num)]
    node_state = sh.FuzzySet(rand_obj, initial_vals)
    vertToAdd = sh.Vertex(node_state)
    politics.addVertex(i, vertToAdd)
    
         
for i in range(num_edges):
    rand_edge = (1,2)
    while (rand_edge in list(politics.edges)) or (rand_edge[1] < rand_edge[0]):
        rand_edge = tuple(rand.sample(range(num_pts),2))
    rand_num = rand.randint(1,len(all_attribs))
    rand_attrib = rand.sample(all_attribs, rand_num)
    rand_attrib.sort()
    edgeToAdd = sh.Edge(rand_attrib)
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