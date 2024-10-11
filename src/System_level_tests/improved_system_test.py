import unittest
from unittest.mock import patch
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from improved_bully_algorithm import Node



class TestLeaderElection(unittest.TestCase):

    def setUp(self):
        # Create nodes
        self.node1 = Node(1, [])
        self.node2 = Node(2, [])
        self.node3 = Node(3, [])
        self.node4 = Node(4, [])

        # Set up connections (add other nodes to each node's list)
        self.node1.nodes = [self.node2, self.node3, self.node4]
        self.node2.nodes = [self.node1, self.node3, self.node4]
        self.node3.nodes = [self.node1, self.node2, self.node4]
        self.node4.nodes = [self.node1, self.node2, self.node3]

    def test_initial_leader_election(self):
        """Test that the highest node becomes the leader initially."""
        # Start an election from node 1
        self.node1.start_election()
        
        # node 1 should become the leader
        self.assertTrue(self.node1.is_leader)
        self.assertFalse(self.node2.is_leader)
        self.assertFalse(self.node3.is_leader)
        self.assertFalse(self.node4.is_leader)
        
        print("Initial leader election test passed.")

def test_node_failure_and_new_leader_election(self):
    """Test that a new leader is elected when the current leader fails."""
    # Start an initial election
    self.node1.start_election()
    
    # Node 1 should be the leader (as it is the highest node)
    self.assertTrue(self.node1.is_leader)

    # Simulate failure of the leader (node 1)
    self.node1.fail_node()

    # Node 2 should detect the failure and start a new election
    self.node2.check_leader_status()

    # After the election, node 2 (next smallest ID) should be the new leader
    self.assertTrue(self.node2.is_leader)
    self.assertFalse(self.node1.is_leader)
    self.assertFalse(self.node1.active)

    
    print("Leader re-election after failure test passed.")


def test_multiple_nodes_fail(self):
    """Test the behavior when multiple higher nodes fail."""
    # Simulate the failure of nodes 3 and 4
    self.node4.fail_node()
    self.node3.fail_node()

    # Start an election from node 2
    self.node2.start_election()

    # Node 1 should become the leader, as it is the highest remaining active node
    self.assertTrue(self.node1.is_leader)
    self.assertFalse(self.node2.is_leader)
    self.assertFalse(self.node3.is_leader)
    self.assertFalse(self.node4.is_leader)

    print("Leader election with multiple node failures test passed.")




if __name__ == '__main__':
    unittest.main()
