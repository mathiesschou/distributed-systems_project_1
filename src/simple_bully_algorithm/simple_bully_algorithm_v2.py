class Node:
    def __init__(self, node_id, nodes):
        self.node_id = node_id                # ID of the current node
        self.nodes = nodes                    # List of all other nodes
        self.is_leader = False                # Initially, no node is the leader
        self.active = True                    # The node is active by default
        self.election_in_progress = False     # Flag to indicate if an election is in progress

    def send_message(self, message, target_node):
        """Send a message to a target node."""
        if target_node.active:
            print(f"Node {self.node_id} sends {message} to Node {target_node.node_id}")
            target_node.receive_message(message, self)

    def receive_message(self, message, sender):
        """Handle the receipt of various types of messages."""
        if not self.active:
            return
        if message == 'Election':
            print(f"Node {self.node_id} received Election message from Node {sender.node_id}")
            # Send an OK message back
            self.send_message('OK', sender)
            # Start its own election process if it's not already in progress
            if not self.election_in_progress:
                self.start_election()
        elif message == 'OK':
            print(f"Node {self.node_id} received OK message from Node {sender.node_id}")
            # OK message indicates that a higher node is in the middle of an election
        elif message == 'Coordinator':
            print(f"Node {self.node_id} received Coordinator message from Node {sender.node_id}")
            self.is_leader = False
            print(f"Node {self.node_id} recognizes Node {sender.node_id} as the leader")

    def start_election(self):
        """Start the election process."""
        print(f"Node {self.node_id} starts an election.")
        self.election_in_progress = True
        higher_nodes = [n for n in self.nodes if n.node_id > self.node_id and n.active]
        
        if not higher_nodes:
            self.become_leader()
        else:
            # Send Election messages to all higher nodes
            for node in higher_nodes:
                self.send_message('Election', node)

    def become_leader(self):
        """Make this node the leader."""
        self.is_leader = True
        self.election_in_progress = False
        print(f"Node {self.node_id} becomes the leader.")
        # Notify all other nodes that this node is the new leader
        for node in self.nodes:
            if node != self and node.active:
                self.send_message('Coordinator', node)

    def fail_node(self):
        """Simulate node failure."""
        self.active = False
        print(f"Node {self.node_id} has failed.")

    def check_leader_status(self):
        """Check if the current leader is still active. If not, start a new election."""
        if not any(node.is_leader and node.active for node in self.nodes):
            print(f"Node {self.node_id} detects that there is no active leader. Starting a new election.")
            self.start_election()


def simulate():
    """Simulate the Bully Election algorithm."""
    # Create a list of 5 nodes
    nodes = [Node(i, []) for i in range(1, 6)]

    # Let each node know about the other nodes
    for node in nodes:
        node.nodes = nodes
    
    # Fail node 3 to simulate a node failure
    nodes[2].fail_node()

    # Start the election process from the lowest active node
    for node in nodes:
        if node.active:
            node.start_election()
            if node.is_leader:
                break

    # After the election is complete, the elected leader fails
    nodes[4].fail_node()

    # Check leader status and start a new election if needed
    for node in nodes:
        if node.active:
            node.check_leader_status()
            if node.is_leader:
                break

if __name__ == "__main__":
    simulate()

