import time

class Node:
    def __init__(self, node_id, nodes):
        self.node_id = node_id  # ID of the current node
        self.nodes = nodes  # List of all other nodes
        self.is_leader = False  # Initially, no node is the leader
        self.active = True  # The node is active by default
        self.election_in_progress = False  # Flag to indicate if an election is in progress
        self.has_received_ok = False  # Track if the node has received an OK message
        self.sent_messages = []  # Initialize sent messages list

    def send_message(self, message, target_node):
        """Send a message to a target node."""
        if target_node.active:
            print(f"Node {self.node_id} sends {message} to Node {target_node.node_id}")
            target_node.receive_message(message, self)
            self.sent_messages.append(message)  # Track sent message

    def receive_message(self, message, sender):
        """Handle the receipt of various types of messages."""
        if not self.active:
            return
        
        print(f"Node {self.node_id} received {message} from Node {sender.node_id}")
        if message == "Election":
            print(f"Node {self.node_id} handling Election message from Node {sender.node_id}")
            if not self.election_in_progress:
                self.send_message("OK", sender)
                self.start_election()

        elif message == "OK":
            print(f"Node {self.node_id} received OK message from Node {sender.node_id}")
            self.has_received_ok = True

        elif message == "Coordinator":
            print(f"Node {self.node_id} received Coordinator message from Node {sender.node_id}")
            self.is_leader = False
            self.election_in_progress = False
            print(f"Node {self.node_id} recognizes Node {sender.node_id} as the leader")

        # If in election, terminate the election process
        if self.election_in_progress and message == "Coordinator":
            print(f"Node {self.node_id} ends its election process due to Coordinator message.")
            self.election_in_progress = False

    def start_election(self):
        """Start the election process using time-based waiting."""
        print(f"Node {self.node_id} starts an election.")
        self.election_in_progress = True
        self.has_received_ok = False  # Reset OK reception flag

        higher_nodes = [n for n in self.nodes if n.node_id > self.node_id and n.active]

        if not higher_nodes:
            print(f"Node {self.node_id} did not find any higher active nodes. Becoming leader.")
            self.become_leader()
        else:
            # Send Election message to all higher nodes
            for node in higher_nodes:
                self.send_message("Election", node)

            # Wait for a short period to simulate waiting for OK responses
            wait_time = 0.1  # Adjust this value as needed for the wait time
            
            print(f"Node {self.node_id} is waiting for OK messages for {wait_time} seconds...")
            time.sleep(wait_time)  # Simulate waiting for OK messages

            # After waiting, check if any OK messages were received
            if not self.has_received_ok:
                print(f"Node {self.node_id} did not receive any OK messages. Becoming the leader.")
                self.become_leader()
            else:
                print(f"Node {self.node_id} received OK messages. Waiting for higher nodes to conclude the election.")

    def become_leader(self):
        """Make this node the leader.""" 
        self.is_leader = True
        self.election_in_progress = False
        print(f"Node {self.node_id} becomes the leader.")

        # Notify all other nodes that this node is the new leader
        for node in self.nodes:
            if node != self and node.active:
                self.send_message("Coordinator", node)

    def fail_node(self):
        """Simulate node failure.""" 
        self.active = False
        print(f"Node {self.node_id} has failed.")

    def check_leader_status(self):
        """Check if the current leader is still active. If not, start a new election.""" 
        if  not any(node.is_leader and   node.active for node in self.nodes):
            print(f"Node {self.node_id} detects that there is no active leader. Starting a new election.") 
            self.start_election()





def test_original_algorithm(node_count):
    nodes = [Node(i, []) for i in range(1, node_count + 1)]
    for node in nodes:
        node.nodes = nodes  # Set the nodes list for each node

    # Simulate a leader failure
    nodes[0].become_leader()  # Assume the first node is the leader
    nodes[0].fail_node()  # Fail the leader

    start_time = time.time()
    for node in nodes:
        node.check_leader_status()  # Check for leader status and initiate election if needed
    end_time = time.time()

    messages_sent = sum([len(node.sent_messages) for node in nodes])
    execution_time = end_time - start_time

    print(f"Original Algorithm: Node Count: {node_count}, Messages Sent: {messages_sent}, Execution Time: {execution_time:.2f} seconds")

# Test with different node counts

test_original_algorithm(10)