# slow down there bud, you're already lost

class Network():
    pass


class Layer():
    def __init__(self, prevLayer, numNodes):
        self.nodes = []
        for _ in range(numNodes):
            newNode = Node()
            newNode.connect(prevLayer)
            self.nodes.append(newNode)


class Node():
    def connect(self, layer):
        for node in layer.nodes:
            self.connections.append(Connection(self, node))


class Connection():
    pass


