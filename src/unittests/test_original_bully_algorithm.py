import unittest
import sys
import os
from time import sleep

# Add the `src` directory to sys.path for import purposes
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Import the Node class from the original_bully_algorithm module
from original_bully_algorithm.original_bully_algorithm import Node

class TestBullyAlgorithm(unittest.TestCase):
    def setUp(self):
        """Setup the nodes for each test."""
        # Create a list of 5 nodes with IDs 1 through 5
        self.nodes = [Node(i, []) for i in range(1, 6)]
        
        # Let each node know about the other nodes
        for node in self.nodes:
            node.nodes = self.nodes

    def test_leader_election_with_all_nodes_active(self):
        """Test the election process when all nodes are active."""
        print("\nStarting test: test_leader_election_with_all_nodes_active")
        self.nodes[0].start_election()
        print("Election completed for test_leader_election_with_all_nodes_active")

        # The expected leader is node 5 (the one with the highest ID)
        self.assertTrue(self.nodes[-1].is_leader, "Node 5 should be the leader")
        for node in self.nodes:
            if node.node_id != 5:
                self.assertFalse(node.is_leader, f"Node {node.node_id} should not be the leader")

    def test_leader_election_with_one_node_failure(self):
        """Test the election process when one of the nodes fails."""
        print("\nStarting test: test_leader_election_with_one_node_failure")
        # Fail node 3
        self.nodes[2].fail_node()
        print(f"Node {self.nodes[2].node_id} has failed")

        # Start the election process from node 1
        self.nodes[0].start_election()
        print("Election completed for test_leader_election_with_one_node_failure")

        # The expected leader is node 5, even though node 3 has failed
        self.assertTrue(self.nodes[-1].is_leader, "Node 5 should be the leader")
        self.assertFalse(self.nodes[2].is_leader, "Node 3 should not be the leader because it has failed")

    def test_leader_election_with_multiple_node_failures(self):
        """Test the election process when multiple nodes fail."""
        print("\nStarting test: test_leader_election_with_multiple_node_failures")
        # Fail node 3 and node 5
        self.nodes[2].fail_node()
        self.nodes[4].fail_node()
        print(f"Node {self.nodes[2].node_id} and Node {self.nodes[4].node_id} have failed")

        # Start the election process from node 1
        self.nodes[0].start_election()
        print("Election completed for test_leader_election_with_multiple_node_failures")

        # The expected leader is node 4, since node 5 has failed
        self.assertTrue(self.nodes[3].is_leader, "Node 4 should be the leader")
        self.assertFalse(self.nodes[4].is_leader, "Node 5 should not be the leader because it has failed")

    def test_simultaneous_elections(self):
        """Test simultaneous leader elections."""
        print("\nStarting test: test_simultaneous_elections")
        # Start election from both node 2 and node 4 simultaneously
        from threading import Thread
        thread1 = Thread(target=self.nodes[1].start_election)  # Node 2
        thread2 = Thread(target=self.nodes[3].start_election)  # Node 4

        # Start both threads
        thread1.start()
        thread2.start()

        # Wait for both threads to complete
        thread1.join(timeout=5)
        thread2.join(timeout=5)
        print("Threads joined for test_simultaneous_elections")

        # The expected leader is node 5 since it has the highest ID
        self.assertTrue(self.nodes[4].is_leader, "Node 5 should be the leader even in simultaneous elections")
        self.assertFalse(self.nodes[1].is_leader, "Node 2 should not be the leader")
        self.assertFalse(self.nodes[3].is_leader, "Node 4 should not be the leader")

    def test_leader_fails_after_election(self):
        """Test what happens if the leader fails after the election."""
        print("\nStarting test: test_leader_fails_after_election")
        # Start the election process from node 1 and let node 5 become the leader
        self.nodes[0].start_election()
        self.assertTrue(self.nodes[4].is_leader, "Node 5 should be the leader")

        # Fail the leader
        self.nodes[4].fail_node()
        print(f"Leader Node {self.nodes[4].node_id} has failed")

        # Start a new election process
        self.nodes[0].check_leader_status()
        print("Leader failure handled in test_leader_fails_after_election")

        # The expected leader is node 4, since node 5 failed
        self.assertTrue(self.nodes[3].is_leader, "Node 4 should be the new leader after node 5 failure")
        for node in self.nodes:
            if node.node_id not in [4, 5]:  # Node 5 should be failed
                self.assertFalse(node.is_leader, f"Node {node.node_id} should not be the leader")

if __name__ == '__main__':
    unittest.main()

