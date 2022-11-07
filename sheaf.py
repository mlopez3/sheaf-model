import networkx as nx
import numpy as np
import warnings
import copy
import matplotlib.pyplot as plt
import matplotlib as mpl
'''
A Sheaf of Lattices Network Model

Miguel Lopez

'''




'''
 The FuzzySet class is a simple subclass of python's dictionaries with some 
convenient functions. 
'''
class FuzzySet(dict):

    def __init__(self, domain, values):
        dict.__init__(self, zip(domain,values))
        self.domain = domain
        self.values = values
        if(len(values) != len(domain)): warnings.warn('Domain and value lists are of different size.')
        
    def __getitem__(self, key):
        val = dict.__getitem__(self, key)
        return val

    def __setitem__(self, key, val):
        dict.__setitem__(self, key, val)
        
    def __str__(self):
        dict.__str__(self)
        
    def __eq__(self):
        dict.__eq__(self)

        
    # Computes the meet of two fuzzy sets
    def meet(fSet1,fSet2):
        assert(fSet1.keys() == fSet2.keys()) # make sure fuzzy set domains are the same 
        values = []
        for key in fSet1.keys():
            values.append( min(fSet1[key],fSet2[key]) )
        fSet = FuzzySet( fSet1.domain,values)
        return fSet
    
    # Computes the meet of a list of fuzzy sets
    def meet2(fSet_lst):
        values = []
        assert(len(fSet_lst) > 0)
        for key in fSet_lst[0].keys():
            vals = []
            for i in range(len(fSet_lst)):
                vals.append(fSet_lst[i][key])
            values.append(min(vals))
        result = FuzzySet( fSet_lst[0].domain,values)
        return result 
    
    def join(fSet1,fSet2):
        assert(fSet1.keys() == fSet2.keys()) 
        values = []
        for key in fSet1.keys():
            values.append( max(fSet1[key],fSet2[key]) )
        fSet = FuzzySet(fSet1.domain, values)
        return fSet

    def join2(fSet_lst):
        values = []
        assert(len(fSet_lst) > 0)
        for key in fSet_lst[0].keys():
            vals = []
            for i in range(len(fSet_lst)):
                vals.append(fSet_lst[i][key])
            values.append(max(vals))
        result = FuzzySet( fSet_lst[0].domain,values)
        return result 
        
    def weighted_meet(fSet1, fSet2, w1,w2): # could we have a vector of weights for each object?
        assert(fSet1.keys() == fSet2.keys()) # make sure fuzzy set domains are the same 
        values = []
        if w1 == 0 and w2 == 0:
            for key in fSet1.keys():
                values.append( 1 )
        elif w1 == 0:
            for key in fSet1.keys():
                values.append( min(fSet2[key]/w2, 1 ))
        elif w2 == 0:
            for key in fSet1.keys():
                values.append( min(fSet1[key]/w1, 1 ))
        else:
            for key in fSet1.keys():
                values.append( min(fSet1[key]/w1,fSet2[key]/w2, 1 ))
        fSet = FuzzySet( fSet1.domain,values)
        return fSet
    
    def weighted_join(fSet1, fSet2, w1,w2):
        assert(fSet1.keys() == fSet2.keys()) # make sure fuzzy set domains are the same 
        values = []
        if w1 == 0 and w2 == 0:
            for key in fSet1.keys():
                values.append( 1 )
        elif w1 == 0:
            for key in fSet1.keys():
                values.append( max(fSet2[key]/w2, 0 ))
        elif w2 == 0:
            for key in fSet1.keys():
                values.append( max(fSet1[key]/w1, 0 ))
        else:
            for key in fSet1.keys():
                values.append( max(fSet1[key]/w1,fSet2[key]/w2, 0 ))
        fSet = FuzzySet( fSet1.domain,values)
        return fSet
    
    def wgt_list_join(fSet_lst, wgt_lst):
        values = []
        assert(len(fSet_lst) > 0)
        for key in fSet_lst[0].keys():
            vals = []
            for i in range(len(fSet_lst)):
                if wgt_lst[i] == 0: vals.append(1)
                else: vals.append(fSet_lst[i][key])
            values.append(max(vals))
        result = FuzzySet( fSet_lst[0].domain,values)
        return result
    
    def wgt_list_meet(fSet_lst, wgt_lst):
        values = []
        assert(len(fSet_lst) > 0)
        assert(len(fSet_lst) == len(wgt_lst))
        for key in fSet_lst[0].keys():
            vals = []
            for i in range(len(fSet_lst)):
                if wgt_lst[i] == 0: vals.append(1)
                else: vals.append(fSet_lst[i][key])
            values.append(max(vals))
        result = FuzzySet( fSet_lst[0].domain,values)
        return result
'''
The FuzzyRelation class stores an object-attribute relationship matrix
along with the lists of objects and attributes. We also store a dictionary
pairs whose keys are obj-attrib pairs and values are the corresponding matrix
(row,col) index, however this code does not currently take advantage of these pairs
'''
class FuzzyRelation():
    def __init__(self, obj, attrib, valueMatrix):
        self.objects = obj 
        self.attribs = attrib
        M = len(obj)
        N = len(attrib)
        pairs = dict()
        for i in range(0,M):
            for j in range(0,N):
                pairs.update({(obj[i],attrib[j]) : (i,j)})
        self.pairs = pairs
        assert ( (len(valueMatrix[:,0]) == M)
        and (len(valueMatrix[0,:]) == N))
        self.valueMatrix = valueMatrix
        
    def __getitem__(self,key):
        index = self.pairs[key]
        value = self.valueMatrix[index[0],index[1]]
        return value
    
    def __str__(self):
        return (np.array2string(self.valueMatrix)+ '\n' +
        'rows: ' + ', '.join(self.objects) + '\n' +
        'cols: ' + ', '.join(self.attribs)  ) 



'''
The following three classes are used to store the information on the sheaf.
The Vertex class stores the fuzzy set and the domain of objects.
The Edge class stores the set of attributes dicussed by two vertices
The Relation class stores the obj-attrib relation associated to a vertex
and edge pair. May want to remain these classes since they dont actually
contain vertex/edge info
'''
class Vertex:
    def __init__(self, fSet):
        self.fSet = fSet
        self.objects = fSet.domain
        return
    
    def update(self, fSet):
        self.fSet = fSet
        return
    
class Edge:
     def __init__(self, attributes, weights = [1,1,1,1]):
         # Ordering is as follows (v = vert1, w = vert2, v < w as indices):
         # vv
         # ww
         # vw
         # wv
         self.attribs = attributes
         self.weights = weights
 
# this information storage is redundant, will fix later
class Relation:
     def __init__(self, vertIndex, edgeIndices, fuzzyRel):
        self.vertIndex = vertIndex
        self.edgeIndices = edgeIndices
        self.fuzzyRel = fuzzyRel
        
     def __str__(self):
        str1 = 'Relation of node ' + str(self.vertIndex) + ' with edge ' + str(self.edgeIndices) + '\n'
        str2 = str(self.fuzzyRel)
        return(str1 + str2)
        
         

'''
 The sheaf class is a subclass of the networkx graph class. The vertex and edge
 information is stored with the super class' attributes while we additionally
 store the relations for each vertex-edge pair. The method Laplacian updates the 
 states (fuzzy sets) of all of the vertices via the diffusion operation. 
 '''
class Sheaf(nx.Graph):
    
    
    def __init__(self, residuum = 'luka'):
        nx.Graph.__init__(self);
        self.relations = dict() 
        self.res = residuum
        return

    
    # function used in computing Laplacian
    def residuum(self, a, b):
        if self.res == 'luka':
            return min(np.around(1.0-a+b,decimals=3),1)
        elif self.res == 'godel':
            if (a <= b): return 1
            else: return b
        elif self.res== 'prod':
            if (a <= b) or (a == 0): return 1
            else: return b/a
        
        
    # vertices are named by their integer index 
    # an object of class Vertex is input in the second argument
    def addVertex(self, vertIndex, vertToAdd):
        self.add_node(vertIndex,vertex = vertToAdd)
        return
    
    # creates and edge between vertIndex1 and vertIndex2 
    # an object of class Edge is input for the third argument 
    # adds 0 matrix for vertex-edge pairs
    def addEdge(self, vertIndex1, vertIndex2, edgeToAdd):
        # whenever an edge is added we force the indices to be in increasing order
        if (vertIndex1 < vertIndex2): 
            v1 = vertIndex1; v2 = vertIndex2
        else: v2 = vertIndex1; v1 = vertIndex2
        self.add_edge(v1, v2, edge = edgeToAdd)   
        # adding 0-relations
        attribs = edgeToAdd.attribs
        obj1 = self.nodes[v1]['vertex'].objects
        z1 = np.zeros( (len(obj1), len(attribs)) )
        self.relations[v1, (v1,v2)] = Relation(v1, (v1,v2), 
                                               FuzzyRelation(obj1, attribs, z1))
        obj2 = self.nodes[v2]['vertex'].objects
        z2 = np.zeros( (len(obj2), len(attribs)) )
        self.relations[v2, (v1,v2)] = Relation(v2, (v1,v2), 
                                               FuzzyRelation(obj2, attribs, z2))
        return
    
    # stores relation matrix along with vertex vertIndex and edge edgeIndices
    def addRelation(self,vertIndex, edgeIndices, valueMatrix):
        obj = self.nodes[vertIndex]['vertex'].objects
        attribs = self.edges[edgeIndices[0], edgeIndices[1] ]['edge'].attribs
        self.relations[vertIndex, edgeIndices] = Relation(vertIndex, edgeIndices, 
                                                          FuzzyRelation(obj, attribs, valueMatrix))
        return
        
    def updateVertex(self,vertIndex,fSet):
        self.nodes[vertIndex]['vertex'].fSet = fSet
    
    def getVertex(self, vertIndex):
        return self.nodes[vertIndex]['vertex']
    
    def getEdge(self,edgeIndices):
        return self.edges[edgeIndices[0], edgeIndices[1] ]['edge']
    
    def Laplacian(self):
        new_states = []
        for node in list(self.nodes):
            updates = []
            for nghbr in self.neighbors(node):
                if node > nghbr:
                    edgeIndices = (nghbr, node)
                else: edgeIndices = (node, nghbr)
                attrib_fSet1 = self.deriv_up(node, edgeIndices)
                attrib_fSet2 = self.deriv_up(nghbr, edgeIndices)
                meet = FuzzySet.meet(attrib_fSet1, attrib_fSet2) #meet
                update = self.deriv_down(node, edgeIndices, meet)
                updates.append(update)
            new_state = FuzzySet.join2(updates) # join
            new_states.append([node,new_state])
        return new_states
        

    def deriv_up(self, vertIndex, edgeIndices):
        vert = self.getVertex(vertIndex)
        edge = self.getEdge(edgeIndices)
        rel = self.relations[vertIndex, edgeIndices]
        values = []
        for attrib in edge.attribs:
            minimum = 1
            for obj in vert.objects:
                a = vert.fSet[obj]
                b = rel.fuzzyRel[obj, attrib]
                result = self.residuum(a,b)
                if result < minimum:
                    minimum = result                   
            values.append(minimum)
        fSet = FuzzySet(edge.attribs,values)
        return fSet
    
    def deriv_down(self, vertIndex, edgeIndices, fSet):
        vert = self.getVertex(vertIndex)
        edge = self.getEdge(edgeIndices)
        rel = self.relations[vertIndex, edgeIndices]
        values = []
        for obj in vert.objects:
            minimum = 1
            for attrib in edge.attribs:
                a = fSet[attrib]
                b = rel.fuzzyRel[obj,attrib]
                result = self.residuum(a, b)
                if result < minimum:
                    minimum = result                    
            values.append(minimum)
        x = FuzzySet(vert.objects,values)
        return x
    
    '''
    Weighted Laplcian 
    '''
    def weighted_Laplacian(self):
        new_states = []
        for node in list(self.nodes):
            updates = []
            wgt_lst = []
            for nghbr in self.neighbors(node):
                if node > nghbr:
                    edgeIndices = (nghbr, node)
                    edge = self.getEdge(edgeIndices)
                    wgt_lst.append[ edge.weights[1] ] # weight ww
                    w1 = edge.weights[3] # weight for wv
                    w2 = edge.weights[2] # weight for vw
                else: 
                    edgeIndices = (node, nghbr)
                    edge = self.getEdge(edgeIndices)
                    wgt_lst.append[ edge.weights[0] ] # weight vv
                    w1 = edge.weights[2] # weight for vw
                    w2 = edge.weights[3] # weight for wv
                # Can the deriv ops be weighted so that they still give an adjunction?
                attrib_fSet1 = self.deriv_up(node, edgeIndices)
                attrib_fSet2 = self.deriv_up(nghbr, edgeIndices)
                meet = FuzzySet.weighted_meet(attrib_fSet1, attrib_fSet2, w1, w2) #meet
                update = self.deriv_down(node, edgeIndices, meet)
                updates.append(update)
            new_state = FuzzySet.wgt_list_join(updates, wgt_lst) # join
            new_states.append([node,new_state])
        return new_states


    def stateReadout(self):
       for node in list(self.nodes):
           print('Node ' + str(node) + ': ' + self.nodes[node]['vertex'].fSet.__repr__())
           for nghbr in self.neighbors(node):
               if node > nghbr:
                   edgeIndices = (nghbr, node)
               else: edgeIndices = (node, nghbr)
               print( str(self.relations[node,edgeIndices]))
           print('')
           # Number of node states displayed can be changed below
           if node > 5: print('Other node states repressed...'); break
       

    
    def update(self, num_iter = 1):
        for i in range(num_iter):
            new_states = self.Laplacian()    
            for state in new_states:
                # meet/join with identity 
                state[1] = FuzzySet.join(state[1], self.getVertex(state[0]).fSet) #join
                self.updateVertex(state[0], state[1])            
        return 
    
    def printFutureStates(self, num_iter = 1):
        for node in list(self.nodes):
            print('Node ' + str(node) + ' after 0 iterations: ' + self.getVertex(node).fSet.__repr__())
        new_sheaf = copy.deepcopy(self)
        print()
        for i in range(1,num_iter):
            new_sheaf.update()
            for node in list(self.nodes):
                print('Node ' + str(node) + ' after ' + str(i) + ' iterations: ' + new_sheaf.getVertex(node).fSet.__repr__())
            print()
            

    def isSection(self):
        new_sheaf = copy.deepcopy(self)
        new_sheaf.update()
        isSection = True
        for node in list(self.nodes):
            if self.getVertex(node).fSet != new_sheaf.getVertex(node).fSet:
                isSection = False
        return isSection
    
    def plotEvolution(self, num_iter, obj):
        # obj = string of object
        new_sheaf = copy.deepcopy(self)       
        time = np.arange(num_iter)
        all_node_states = {}
        for node in list(self.nodes):
            if obj not in self.getVertex(node).fSet:
                continue
            else: 
                node_states = [ self.getVertex(node).fSet[obj] ]
                all_node_states[node] = node_states
        for i in range(1,num_iter):
            new_sheaf.update()          
            for node in all_node_states:
                all_node_states[node].append(new_sheaf.getVertex(node).fSet[obj])    
        
        if len(all_node_states) == 0:
            print('No nodes with object: ',obj)
            return
        else:
            plt.figure(figsize=(10, 8))
            for node in all_node_states:
                plt.plot(time,all_node_states[node], label = 'Node ' + str(node))
            plt.xlabel('Time Step')
            plt.ylabel('Favor')
            plt.title('Opinions about ' + obj)
            plt.legend()
            