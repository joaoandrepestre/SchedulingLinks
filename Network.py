from random import *
from Graph import Graph

class Network:

    def __init__(self, Pt=100, alfa=4, beta=25, T=300, B=2000000000000, L=1000, n=25,FD=False):
        self.Pt = Pt
        self.alfa = alfa
        self.beta = beta
        self.T = T
        self.L = L
        self.n = n
        self.k = 1.38064852*(10**(-23)) #Boltzmann constant(k[(m**2)*kg*(s**-2)*(K**-1)])
        self.B = B
        self.G = self.generateRandomNetwork()
        self.Gphy = self.getConflictGraph(FD)


    def getConflictGraph(self,FD):
        """Returns the conflict graph of the nerwork"""
        links = []
        for i in range(self.G.dim):
            #v1 = self.G.vertices[i]
            for j in range(i+1,self.G.dim):
                #v2 = self.G.vertices[j]
                if self.G.adjacencies[i][j]:
                    links.append((i,j))
        g = Graph(links)
        for i in range(g.dim):
            for j in range(i+1,g.dim):
                s = self.SINR(links[i],[links[j]])
                if FD:
                    g.setAdj(i,j,s<self.beta and not(links[i][0] in links[j] or links[i][1] in links[j]))
                else:
                    g.setAdj(i,j,s<self.beta)
        return g
                    


    def NoiseFloor(self):
        """Returns the noise floor of a region considering a temperature
        'T'(in Kelvin) and a band width 'B'(in MHz)"""
        return self.k*self.T*self.B


    def maxDistance(self):
        """Retruns the maximum distance between two nodes for that a link can be
        established, considering a transmitting power 'Pt', an ambient coefficient
        'alfa', a SNR treshold 'beta', a temperature 'T'(in Kelvin) and a band width
        'B'(in MHz)"""
        N = self.NoiseFloor()
        return (self.Pt/(N*self.beta))**(1.0/self.alfa)


    def generateRandomNetwork(self):
        """Chooses random positions for 'n' nodes on a square of side 'L'
        and returns the graph of feasible links considering  a transmitting
        power 'Pt'(in Mw), an ambient coefficient 'alfa', a SNR treshold 'beta'(in dB)
        and a tempeture 'T'(in Kelvin)"""
        nodes = [(self.L*random(),self.L*random()) for i in range(self.n)] #Creates a list of 'n' nodes placed randomly in the square of side 'L'
        network = Graph(nodes) #Creates a graph to represent the network
        maxD = self.maxDistance()
        for i in range(self.n):
            node1 = nodes[i]
            x1, y1 = node1[0], node1[1]
            for j in range(i+1,self.n):
                node2 = nodes[j]
                x2, y2 = node2[0], node2[1]
                d = ((x1-x2)**2+(y1-y2)**2)**0.5
                if d < maxD:
                    network.setAdj(i, j, True)

        return network

    def interferenceNumber(self,i,G):
        """Returns the interference number of the vertex 'i' in the conflict graph
        'Gphy'"""
        return G.getDegree(i)


    def order(self,E,G): 
        """Orders the list E according to the interference number in the conflict
        graph 'G'"""
        if len(E)>1:
            mid = len(E)/2
            left = E[:mid]
            right = E[mid:]

            self.order(left,G)
            self.order(right,G)

            i = 0
            j = 0
            k = 0
            while i < len(left) and j < len(right):
                if self.interferenceNumber(left[i],G) > self.interferenceNumber(right[j],G):
                    E[k] = left[i]
                    i += 1
                else:
                    E[k] = right[j]
                    j += 1
                k += 1

            while i < len(left):
                E[k] = left[i]
                i += 1
                k += 1

            while j < len(right):
                E[k] = right[j]
                j += 1
                k += 1


    def distance(self,v,u):
        """Returns the distance between the vectors 'v' and 'u'"""
        x,y = v
        x1,y1 = u
        return ((x-x1)**2+(y-y1)**2)**(0.5)
        

    def SINR(self,v,slot):
        """Returns the Signal to Interference and Noise Ratio"""
        v1,v2 = self.G.vertices[v[0]],self.G.vertices[v[1]]
        d = self.distance(v1,v2)
        S = self.Pt/(d**self.alfa)
        N = self.NoiseFloor()
        I = 0
        for i in range(len(slot)):
            v1,v2 = self.G.vertices[slot[i][0]],self.G.vertices[slot[i][1]]
            d = self.distance(v1,v2)
            I += self.Pt/(d**self.alfa)
        return S/(I+N)

    def isFeasible(self,i,slot):
        """Returns true if, and only if, scheduling the link 'i' in the slot 'slot'
        according to the conflict graph 'Gphy' is feasible under the physical
        interference model"""
        for j in range(len(slot)):
            if self.Gphy.adjacencies[i][slot[j][2]]:
                return False
        return True


    def schedule(self,i,j,slots):
        """Adds the link 'i' of the conflict graph 'Gphy' to the slot of index 'j'
        in the slots dictionary 'slots'"""
        link = self.Gphy.vertices[i]
        s = slots.get(j,[])
        s.append((link[0],link[1],i))
        slots[j] = s


    def remove(self,e,l,G):
        """Removes the element 'e' from the list 'l' and its influence in the graph 'G'"""
        l.remove(e)
        for i in range(G.dim):
            G.setAdj(e,i,False)
            

    def GreedyPhysical(self):
        """Returns the feasible schedule and its length under physical interference
        model  given a weighted communication graph 'G' and the conflict graph Gphy"""
        tmp = self.Gphy.copy()
        slots = {}
        E = [i for i in range(tmp.dim)]
        self.order(E,tmp)
        while len(E)>0:
            scheduled = False
            for j in range(len(slots)):
                s = slots.get(j,[])
                if self.isFeasible(E[0],s):
                    self.schedule(E[0],j,slots)
                    self.remove(E[0],E,tmp)
                    scheduled = True
                    break
            if not scheduled:
                self.schedule(E[0],len(slots),slots)
                self.remove(E[0],E,tmp)
            self.order(E,tmp)
        return (slots,len(slots))
        
    def __repr__(self):
        """Returns a string representation of the network"""
        return "Network with "+str(self.n)+" nodes and "+str(self.Gphy.dim)+" links."