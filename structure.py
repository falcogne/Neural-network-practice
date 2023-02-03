# slow down there bud, you're already lost

class Network():
    def __init__(self, nodes):
        self.layers = [InputLayer(nodes[0])]
        for num in nodes[1:]:
            layers.append(Layer(num))

        # now have layers with nodes in them but no connections between them
        # and no input/output layer

        for i in range(len(self.layers)-1, 0, -1): # go backwards through list of layers - don't include input layer
            layer[i].connect(layer[i-1])

class Layer():
    def __init__(self, numNodes):
        self.nodes = []
        for _ in range(numNodes):
            newNode = Node()
            self.nodes.append(newNode)

class InputLayer(Layer):
    def __init__(self, inputVector):
        pass

class Node():
    def connect(self, layer):
        for node in layer.nodes:
            self.connections.append(Connection(self, node))

class Connection():
    pass


