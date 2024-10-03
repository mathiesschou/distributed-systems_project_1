from node import Node

class Node:
    def __init__(self, node_id, nodes):
        self.node_id = node_id
        self.nodes = nodes  # List for knowing other nodes
        self.is_leader = False
        self.active = True  # Node is active by default
         
    def send_message(self, message, target_node):
        if target_node.active:
            target_node.receive_message(message, self)

    def receive_message(self, message, sender):
        if not self.active:
            return
        if message == 'Election':
            print(f"Node {self.node_id} received Election message from Node {sender.node_id}")
            if sender.node_id < self.node_id:
                self.send_message('Answer', sender)
                self.start_election()
        elif message == 'Answer':
            print(f"Node {self.node_id} received Answer message from Node {sender.node_id}")
        elif message == 'Coordinator':
            self.is_leader = False
            print(f"Node {self.node_id} recognizes Node {sender.node_id} as the leader")

    def start_election(self):
        print(f"Node {self.node_id} starts an election.")
        higher_nodes = [n for n in self.nodes if n.node_id > self.node_id and n.active]
        
        if not higher_nodes:
            self.become_leader()
        else:
            for node in higher_nodes:
                self.send_message('Election', node)

    def become_leader(self):
        self.is_leader = True
        print(f"Node {self.node_id} becomes the leader.")
        for node in self.nodes:
            if node != self and node.active:
                self.send_message('Coordinator', node)

    def fail_node(self):
        self.active = False
        print(f"Node {self.node_id} has failed.")

