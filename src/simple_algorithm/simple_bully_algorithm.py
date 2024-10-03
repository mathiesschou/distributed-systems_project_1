class SimpleBullyAlgorithm:
    def __init__(self, node_id, nodes):
        self.node_id = node_id
        self.nodes = nodes # List for knowing other nodes
        self.is_leader = False

    def start_election(self):
        print(f"Node {self.node_id} starts an election.")
        # Check for higher nodes, and adds them to a list
        higher_nodes = [n for n in self.nodes if n.node_id > self.node_id]
        
        # Pick the leader with the highest node
        if not higher_nodes:
            self.become_leader()
        else:
            for node in higher_nodes:
                if node.respond_to_election():
                    print(f"Node {node.node_id} responds to the election.")
                    return False
            self.become_leader()

    def respond_to_election(self):
        print(f"Node {self.node_id} responds.")
        return True

    def become_leader(self):
        self.is_leader = True
        print(f"Node {self.node_id} becomes the leader.")

# Simple simulation
def simulate():
    # Create a list of nodes with IDs 1 to 5
    nodes = [SimpleBullyAlgorithm(i, []) for i in range(1, 6)]

    # Let each node know about the others
    for node in nodes:
        node.nodes = nodes
    
    # Start election from the node with the lowest ID
    # Starts from node 2, such that we see no involvement 
    # of lower node 1 in the election process
    for node in nodes[1:]:
        node.start_election()
        if node.is_leader:
            break 

if __name__ == "__main__":
    simulate()
