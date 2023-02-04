# slow down there bud, you're already lost

import math

class Network():
    def __init__(self, nodes=[2,2]):
        self.layers = [InputLayer(nodes[0])]
        for num in nodes[1:]:
            self.layers.append(Layer(num))

        # now have layers with nodes in them but no connections between them
        # and no input/output layer

        for i in range(1, len(self.layers)): # layer at index 0 is input layer
            self.layers[i].connect(self.layers[i-1])

class Layer():
    def __init__(self, numNodes):
        self.nodes = []
        for _ in range(numNodes):
            newNode = Node()
            self.nodes.append(newNode)

    def connect(self, otherLayer, backwards=True):
        for node in self.nodes:
            for othernode in otherLayer.nodes:
                node.connect(othernode, backwards=backwards)

class InputLayer(Layer):
    def setInputs(self, inputVector):
        if len(inputVector) != len(self.nodes):
            raise AssertionError(f'length of input vector does not equal length of input nodes: vector length - {len(inputVector)}, nodes - {len(self.nodes)}')
        
        for i in range(len(self.nodes)):
            if type(inputVector[i]) != int:
                raise TypeError(f'input vector is not all integers | index: {i}, value: {inputVector[i]}, type: {type(inputVector[i])}')
            self.nodes[i].value = inputVector[i]

class Node():

    def __init__(self, value, b, prevLayer=None, nextLayer=None):
        self.val = value # this is `a` on the slides
        self.b = b
        self.z = None
        # self.a = None
        self.dldz = None
        self.func =  lambda z : 1 / (1+math.e**(-z))
        self.deriv = lambda z : (math.e**(-z)) / ((1+math.e**(-z))**2)
        # self.sigmaDeriv = lambda z : (math.e**(z)) / ((1+math.e**(z))**2) # apparently equivalent
        self.backConnections = []
        self.frontConnections = []

        if prevLayer is not None:
            self.connect(prevLayer)    
        if nextLayer is not None:
            self.connect(nextLayer)

    def __init__(self):
        self.__init__(0, 0)

    def connect(self, layer, backward=True):
        for node in layer.nodes:
            if backward:
                self.backConnections.append(Connection(node, self))
            else:
                self.frontConnections.append(Connection(self, node))

    def calcVal(self):
        sum = 0
        for conn in self.backConnections:
            sum += conn.weight * conn.backNode.val
        self.z = sum + self.b
        self.val = self.func(self.z)

    def calcdldz(self):
        sum = 0
        for conn in self.frontConnections:
            if conn.frontNode.dldz is None:
                raise ValueError('front node must have already calculated dl/dz in order to calculate node\'s dldz value - not implemented recursively')
            sum += conn.weight * conn.frontNode.dldz
        if self.z is None:
            raise ValueError('self node\'s z must already be set when trying to calculate dldz')
        return self.deriv(self.z) * sum

    def errorCheck(self):
        if type(self.val) is not float:
            raise TypeError(f'node value is not float: {self.val}')
        if self.val != self.func(self.z):
            raise TypeError(f'node value is not equal to sigma function of self.z: {self.val} != func({self.z})')
        if type(self.b) is not int:
            raise TypeError(f"node's b is not float: {self.b}")
        
        for conn in self.backConnections:
            if conn.frontNode is not self:
                raise ValueError('front node of back connection must be this node')
        for conn in self.frontConnections:
            if conn.backNode is not self:
                raise ValueError('back node of front connection must be this node')



class Connection():
    def __init__(self, backNode, frontNode):
        self.backNode = backNode
        self.frontNode = frontNode
        self.weight = 0 # TODO: does it initialize to 0?

    def calcdzdw(self):
        return self.backNode.val
    
    def calcdldw(self):
        return self.calcdzdw() * self.frontNode.calcdldz()
