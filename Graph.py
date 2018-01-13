class Graph:
    """Graph data structure to be used in the network representation"""

    def __init__(self,v):
        """Class constructor"""
        self.vertices = v
        self.dim = len(self.vertices)
        self.adjacencies = [[False for i in range(self.dim)]for j in range(self.dim)]

    def setAdj(self, i, j, b):
        """Sets the adjacencies between the vertices i and j of the graph to
        the boolean 'b'"""

        self.adjacencies[i][j] = b
        self.adjacencies[j][i] = b

    def getAdj(self, i):
        """Returns a list of all adjacencies of vertex i"""

        return [(j,self.vertices[j][0],self.vertices[j][1]) for j in range(self.dim) if self.adjacencies[i][j]]

    def getAllAdj(self):
        """Returns the adjacencies matrix of the graph"""

        return self.adjacencies

    def getDegree(self, i):
        """Return the number of adjacencies of vertex i"""

        degree = 0
        for j in range(self.dim):
            if self.adjacencies[i][j]:
                degree +=1

        return degree
        
    def copy(self):
        """Returns a new graph that is a copy of this one"""
        
        g = Graph(self.vertices)
        for i in range(self.dim):
            for j in range(self.dim):
                g.setAdj(i,j,self.adjacencies[i][j])
                
        return g

        
    def __repr__(self):
        """Returns a string representation of the graph for
        functions like 'print'"""

        r = "     "

        for i in range(self.dim):
            if i<10:
                r += "0" + str(i) + " "
            else:
              r += str(i) + " "
        r += "\n"

        for i in range(self.dim):
            
            s = str(i)
            if len(s)<2:
                r += "0"
            r += s + " | "

            for j in range(self.dim):
                if self.adjacencies[i][j]:
                    r += " 1 "
                else:
                    r += " 0 "

            r += "| "
            s = str(i)
            if len(s)<2:
                r += "0"
            r += s + "\n"

        r += "     "

        for i in range(self.dim):
            if i<10:
                r += "0" + str(i) + " "
            else:
                r += str(i) + " "
        r += "\n"
        return r
