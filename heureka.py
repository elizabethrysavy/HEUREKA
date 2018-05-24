"""
Elizabeth Rysavy s176182
Introduction to Artificial Intelligence 02180
heureka.py
Created on Tue Mar 13 13:30:05 2018
"""

#import statements
import math
from queue import PriorityQueue
import time

class Node: #Node in form (x,y)
    def __init__(self, xcoord, ycoord):
        self.x = xcoord
        self.y = ycoord
        self.neighbors = [] #list of edges beginning at this node
    
    def getLoc(self): #return coordinates as a tuple
        return (self.x, self.y)
     
    def __hash__(self): #node identification
        locString = str(self.x) + str(self.y)
        return hash(locString)

    def __eq__(self, other): #Are they the same node?
        (nx, ny) = other.getLoc()
        if nx != self.x: #same x coordinate
            return False
        elif ny != self.y: #same y coordinate
            return False
        else:
            return True
    
    def __lt__(self, other):
        ##For priority queue when nodes have same cost, lower coordinates = higher priority 
        #i.e. (0,1) has higher priority than (1,0) and (2,0) has higher priority than (2,1)
        (nx, ny) = other.getLoc()
        if self.x < nx:
            return True
        elif self.x > nx:
            return False
        else: ##same x coordinate
            if self.y < ny:
                return True
            else:
                return False
        
    def getNeighbors(self, edgeList):
        #edgeList is a list of edges/roads in the map
        #return a list of edges that start at this node
        for e in edgeList:
            n = e.getStart()
            if self == n: #if this node is the start of the edge
                self.neighbors.append(e)
        return self.neighbors
    
    def distBetween(self, other): #Euclidean distance this node and another node
        (ox, oy) = other.getLoc()
        dist = math.sqrt((math.pow(abs(ox - self.x), 2)) + (math.pow(abs(oy - self.y), 2)))
        return dist
    
    def __str__(self): #convert node to string ie str(Node) = "(x, y)"
        coord = "({}, {})".format(self.x, self.y)
        return coord
    
               
class Edge: #Edge A from (x1,y1) to (x2,y2)
    def __init__(self, edgeData):
        #edgeData is an array containing start node, name, and end node
        #intOrFloat is a function that determines if a string is an int or float and converts it
        self.x1 = intOrFloat(edgeData[0])
        self.y1 = intOrFloat(edgeData[1])
        self.x2 = intOrFloat(edgeData[3])
        self.y2 = intOrFloat(edgeData[4])
        self.name = edgeData[2]
        self.sNode = Node(self.x1, self.y1)
        self.eNode = Node(self.x2, self.y2)
        self.dist = self.sNode.distBetween(self.eNode) #calculate distance between start and end node
    
    def getStart(self): #return starting node on edge
        return self.sNode
   
    def getEnd(self): #return ending node on edge
        return self.eNode
    
    def getName(self): #return street name
        return self.name
    
    def getEdgeLength(self): #return edge length
        return self.dist
    
    def __str__(self): #convert edge to string ie str(edge) = "Name     dist" where dist is a float with 2 decimal points
        return "{}:\t{:.2f}".format(self.name, self.dist)
           
    
def intOrFloat(num): #determine if number is a float or int and convert it
    #ex1: a = "3"     ex2: b = "5.5"
    f = float(num)   #in examples fa = 3.0   fb = 5.5
    i = int(f)       #in examples ia = 3   ib = 5
    if i == f:   #ex1:  3.0 = 3 so i (3) is returned      
        return i
    else:        #ex2: 5.5 != 5 so f (5.5) is returned
        return f
    

def isNum(num): #determine if a string is a number (float or int)
    dec = num.replace(".", "", 1) # removes 1 "." from the string if it exists 
    #ie 3.14 will be considered a number but 3..14 or .3.14 will not
    neg = dec.replace("-", "", 1) #removes 1 "-" from the dec string if it exists
    #ie -5 will be considered a number but --5 or -5- will not
    isNum = neg.isdigit() #true if string (with 1 "." and 1 "-" removed) contains only numbers
    return isNum

        
def createMap(ifile): #take file input and create the map (list of edges)
    #each line in file is an edge, formatted as: x1 y1 Name x2 y2
    try:
        f = open(ifile, "r") #open file
    except FileNotFoundError: #if file doesn't exist
        print("\nERROR: File Not Found")
        return None
    
    edges = []
    for line in f:
        data = line.split() #convert line of text into array [x1, y1, Name, x2, y2]
        if len(data) == 0: #empty line
            continue
        elif not len(data) == 5 or not isNum(data[0]) or not isNum(data[1]) or not isNum(data[3]) or not isNum(data[4]):
            ##if file formatted wrong: exit
            print("\nINVALID FILE INPUT: Incorrect format")
            print("Lines of file should be in form: x1 y1 Street_Name x2 y2")
            return None
        else: #if file is good
            edges.append(Edge(data)) #add edge to list
    
    f.close() #close file
    return edges


def findRoute(nodes, edges, start, goal): #find route from start node to goal node       
    pq = PriorityQueue() #create priority queue
    sdist = start.distBetween(goal)
    pq.put((sdist, start)) #add start node to pq 
    
    cost = {} #dictionary of cost of each node
    cost[start] = 0
    path = {} #dictionary of previous node used to reach node in path
    path[start] = None
    visited = [] #list of visited nodes
    visited.append(start)
    
    while not pq.empty():
        current = pq.get()[1] #get highest priority node
        if current == goal: #if goal reached, exit
            break
        if len(current.getNeighbors(edges)) == 0: #if goal unreachable, return none and exit
            path = None
            break
        for edge in current.getNeighbors(edges): #loop through list of node's neighbors
            newCost = cost[current] + edge.getEdgeLength() #determine cost to reach neighbor node
            nextNode = edge.getEnd()
            if nextNode not in visited or newCost < cost[nextNode]: #if node unvisited and lowest cost of neighbors
                #add node to path
                cost[nextNode] = newCost
                priority = newCost + nextNode.distBetween(goal) #heuristic weight
                visited.append(nextNode)
                pq.put((priority, nextNode))
                path[nextNode] = edge 
                    
    return path
   
         
def reconstructPath(path, start, goal): #return route taken to get from start to goal
    if path == None: #if no route exists
        print("\nFAILED: No route found from {} to {}".format(str(start), str(goal)))
        return
    
    current = goal
    route = []
    cost = 0
    
    while path[current] != None: #until start node is reached
        edge = path[current] #use dictionary to determine previous node in path
        route.insert(0, edge)
        cost += edge.getEdgeLength()
        current = edge.getStart()
   
    #output
    print("\nRoute")
    print("-"*10)
    print("Start: " + str(start))
    returnRoute(route)
    print("End: " + str(goal))
    print("Total Cost: {:.2f}".format(cost)) #print total cost to 2 decimal places
    

def returnRoute(routeList): #print the route
    route = [] #list of streets in form [start, name, end, distance]
    prev = None
    
    for edge in routeList:
        if not prev == None and prev.getName() == edge.getName():
            #if continuing on same street just increase length, dont add new edge
            #i.e. 00 00 avenue1 00 02 to 00 02 avenue1 00 04 becomes 00 00 avenue1 00 04
            route[-1][3] += edge.getEdgeLength() #update length travelled on street
            route[-1][2] = edge.getEnd() #update end node on street
        else:
            route.append([edge.getStart(), edge.getName(), edge.getEnd(), edge.getEdgeLength()])
        prev = edge
    
    for street in route:
        #print street in form "(startX, startY) -> (endX, endY):     Name     dist"   where dist has 2 decimal places
        print("{} -> {}\t {}: \t {:.2f}".format(street[0], street[2], street[1], street[3]))


def manhattanTime(nodeList, edgeList): ##evaluate performance of route finding for Manhattan map
    sNode = Node(0,0)
    times = [0,0,0,0,0,0,0,0,0]
    
    for i in range(9): #path from (0,0) to (1,1), (2,2), ... or (9,9)
        eNode = Node(i+1, i+1)
        t1 = time.time()
        path = findRoute(nodeList, edgeList, sNode, eNode) #determine path from (0,0) to (i,i)
        #comment or uncomment following line if you want path reconstruction and output to be included in timing
        reconstructPath(path, sNode, eNode)
        t2 = time.time()
        times[i] = t2-t1 #add time taken to list of times
    
    print("\n\n")
    for i in range(9): #print time taken to find each route
        print("(0,0) -> ({},{}): {:.4f}s".format(i+1, i+1, times[i]))


def nodeInput(nodeList): #ask user for start and end nodes and check validity
    i = 1
    print("Nodes in Map:") #prints a list of nodes in the map for the user to choose from
    for node in nodeList:
        if i % 3 == 0:
            print(str(node))
        else:
            print(str(node), end="\t")
        i += 1
    print()
             
    valids = False
    sNode = None
    while not valids: #continuously ask user for start node until a valid one is entered
        sNodein = input("Start Node (in form 'x y'): ").split()
        if not len(sNodein) == 2 or not isNum(sNodein[0]) or not isNum(sNodein[1]): 
            #if node is invalid or in incorrect form
            print("INVALID NODE INPUT: Incorrect Form")
            print("Please enter node as 2 numbers seperated by a space\n\n")
            print(sNodein)
            continue #ask again
        sNode = Node(intOrFloat(sNodein[0]), intOrFloat(sNodein[1])) #create node if input is valid
        if sNode not in nodeList: #if input node is not in list of nodes in map
            print("INVALID NODE INPUT: Not in Map\n\n")
        else:
            valids = True #exit loop once a valid node has been entered
    
    valide = False
    eNode = None
    while not valide: #continuously ask user for goal node until a valid one is entered
        eNodein = input("Goal Node (in form 'x y'): ").split()
        if not len(eNodein) == 2 or not isNum(eNodein[0]) or not isNum(eNodein[1]): 
            #if node is invalid or in incorrect form
            print("INVALID NODE INPUT: Incorrect Form")
            print("Please enter node as 2 numbers seperated by a space\n\n")
            continue #ask again
        eNode = Node(intOrFloat(eNodein[0]), intOrFloat(eNodein[1])) #create node if input is valid
        if eNode not in nodeList: #if input node is not in list of nodes in map
            print("INVALID NODE INPUT: Not in Map\n\n")     
        else:
            valide = True #exit loop once a valid node has been entered
    
    return (sNode, eNode) #return start and goal nodes
    
    
def main():
    ifile = input("File Name (i.e. 'map.txt'): ") #Ask user for input file  
    edgeList = createMap(ifile) #create list of edges
    
    if edgeList == None: #if file not found or formatted wrong: exit
        return
    
    nodeList = [] #create list of unique nodes
    for edge in edgeList:
        nodeList.append(edge.getStart())
        nodeList.append(edge.getEnd())
    nodeList = list(set(nodeList))
    (sNode, eNode) = nodeInput(nodeList) #Ask user for start and goal nodes
   
    path = findRoute(nodeList, edgeList, sNode, eNode) #find path from start node to goal node
    reconstructPath(path, sNode, eNode) #reconstruct and print found path
    
        
main()  #run program     