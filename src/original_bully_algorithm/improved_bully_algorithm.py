import time
import random

class Node:
    def __init__(self, node_id, nodes):
        self.node_id = node_id  # ID of the current node
        self.nodes = nodes  # List of all other nodes
        self.is_leader = False  # Initially, no node is the leader
        self.active = True  # The node is active by default
        self.election_in_progress = False  # Flag to indicate if an election is in progress
        self.leader_heartbeat_interval = 2  # Heartbeat check interval
        self.leader_check_timeout = 6  # Timeout for leader heartbeat

    def send_message(self, message, target_node):
        """Send a message to a target node."""
        if target_node.active:
            print(f"Node {self.node_id} sends {message} to Node {target_node.node_id}")
            target_node.receive_message(message, self)

    def receive_message(self, message, sender):
        """Handle the receipt of various types of messages."""
        if not self.active:
            return

        print(f"Node {self.node_id} received {message} from Node {sender.node_id}")

        if message == "Election":
            print(f"Node {self.node_id} handling Election message from Node {sender.node_id}")
            if not self.election_in_progress:
                # Respond with OK only once and initiate election if not in progress
                self.send_message("OK", sender)
                self.start_election()

        elif message == "OK":
            print(f"Node {self.node_id} received OK message from Node {sender.node_id}")
            # Acknowledge receipt of OK but do not start election again

        elif message == "Coordinator":
            print(f"Node {self.node_id} received Coordinator message from Node {sender.node_id}")
            self.is_leader = False
            print(f"Node {self.node_id} recognizes Node {sender.node_id} as the leader")

    def start_election(self):
        """Start the election process."""
        print(f"Node {self.node_id} starts an election.")
        self.election_in_progress = True

        higher_nodes = [n for n in self.nodes if n.node_id > self.node_id and n.active]

        if not higher_nodes:
            print(f"Node {self.node_id} did not find any higher active nodes. Becoming leader.")
            self.become_leader()
        else:
            # Send Election message to all higher nodes
            for node in higher_nodes:
                self.send_message("Election", node)

            # Wait for a response to determine the outcome of the election
            wait_time = 0.1  # Adjust this value as needed for the wait time
            print(f"Node {self.node_id} is waiting for responses for {wait_time} seconds...")
            time.sleep(wait_time)  # Simulate waiting for OK messages

            # If no OK responses were received, this node becomes the leader
            self.become_leader()

    def become_leader(self):
        """Make this node the leader."""
        self.is_leader = True
        print(f"Node {self.node_id} becomes the leader.")
        self.election_in_progress = False

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
        if not any(node.is_leader and node.active for node in self.nodes):
            print(f"Node {self.node_id} detects that there is no active leader. Starting a new election.")
            self.start_election()

    def send_leader_heartbeat(self):
        """Send a heartbeat signal to indicate the leader's status."""
        while self.is_leader:
            for node in self.nodes:
                if node != self and node.active:
                    self.send_message("Coordinator", node)
            time.sleep(self.leader_heartbeat_interval)  # Sleep for the heartbeat interval

