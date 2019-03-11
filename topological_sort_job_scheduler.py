#-*- coding: utf-8 -*-
from collections import defaultdict

#Kahn’s algorithm for Topological Sorting

class DAG:
    def __init__(self, DAG_config = None): 
        self.graph = defaultdict(list) #Create hashmap for saving Adjacencty list

        if 'num_nodes' not in DAG_config.keys():
            raise InvalidDAGError('Number of nodes undefined')

        self.V = DAG_config['num_nodes'] #No. of vertices

        if 'edges' not in DAG_config.keys():
            raise InvalidDAGError('Edges undefined')

        # creating dictionary containing adjacency List, aka hashmap
        for edge in DAG_config['edges']:
            self.graph[edge['from']].append(edge['to'])

    def topologicalSort(self): 
        # Create a vector to store indegrees of all 
        # vertices. Initialize all indegrees as 0. 
        in_degree = [0]*(self.V) 
          
        # Traverse adjacency lists to fill indegrees of 
           # vertices.  This step takes O(V+E) time 
        for i in self.graph: 
            for j in self.graph[i]: 
                in_degree[j] += 1
  
        # Create an queue and enqueue all vertices with 
        # indegree 0 
        queue = [] 
        for i in range(self.V): 
            if in_degree[i] == 0: 
                queue.append(i) 
  
        #Initialize count of visited vertices 
        cnt = 0
  
        # Create a vector to store result (A topological 
        # ordering of the vertices) 
        top_order = [] 
  
        # One by one dequeue vertices from queue and enqueue 
        # adjacents if indegree of adjacent becomes 0 
        while queue: 
  
            # Extract front of queue (or perform dequeue) 
            # and add it to topological order 
            u = queue.pop(0) 
            top_order.append(u) 
  
            # Iterate through all neighbouring nodes 
            # of dequeued node u and decrease their in-degree 
            # by 1 
            for i in self.graph[u]: 
                in_degree[i] -= 1
                # If in-degree becomes zero, add it to queue 
                if in_degree[i] == 0: 
                    queue.append(i) 
  
            cnt += 1
  
        # Check if there was a cycle
        if cnt != self.V: 
            raise CyclicGraphError('Error in DAG Config, cannot perform topological sort')
        else: 
            print top_order 

class DAGError(Exception):
    pass

class InvalidDAGError(DAGError):
    def __init__(self, msg):
        print "Exception occured while building DAG : " + msg

class CyclicGraphError(DAGError):
    def __init__(self, msg):
        print "There exists a cycle in the Graph"

DAG_config = {
"num_nodes": 6,         # number of tasks/jobs
"edges":                # dependencies
    [
        {
            "from": 5,
            "to": 2,
            "data": {   # data 
                    }
        }, 
        {
            "from": 5,
            "to": 0,
            "data": {   # data 
                    }
        },
        {
            "from": 4,
            "to": 0,
            "data": {   # data 
                    }
        },
        {
            "from": 4,
            "to": 1,
            "data": {   # data 
                    }
        }, 
        {
            "from": 2,
            "to": 3,
            "data": {   # data 
                    }
        },
        {
            "from": 3,
            "to": 1,
            "data": {   # data 
                    }
        }
    ]
}

g = DAG(DAG_config)

g.topologicalSort()
