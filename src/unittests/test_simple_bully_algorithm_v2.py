import unittest
import sys
import os

# Add the `src` directory to sys.path for import purposes
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

# Import Node from the original_bully_algorithm module
from original_bully_algorithm.original_bully_algorithm import Node

class TestOriginalBullyAlgorithm(unittest.TestCase):
    def setUp(self):
        """Setup the nodes for each test."""
        # Create 5 nodes with IDs 1 through 5
        self.nodes = [Node(i, []) for i in range(1, 6)]
        
        # Let each node know about the other nodes
        for node in self.nodes:
            node.nodes = self.nodes

    def test_leader_elected(self):
        """Test if node 5 is elected as leader when starting from node 2."""
        # Start election from node 2
        for node in self.nodes[1:]:
            node.start_election()
            if node.is_leader:
                break

        # Node 5 should be the leader
        self.assertTrue(self.nodes[-1].is_leader, "Node 5 should be the leader")

    def test_lower_node_not_leader(self):
        """Test that node 1 is not elected as leader."""
        # Start election from node 2
        for node in self.nodes[1:]:
            node.start_election()
            if node.is_leader:
                break

        # Node 1 should not be the leader
        self.assertFalse(self.nodes[0].is_leader, "Node 1 should not be the leader")

    def test_election_starts_from_node_2(self):
        """Test that the election excludes node 1 when starting from node 2."""
        # Start election from node 2
        for node in self.nodes[1:]:
            node.start_election()
        
        # Node 1 should not participate or be elected as leader
        self.assertFalse(self.nodes[0].is_leader, "Node 1 should not participate in the election")

    def test_leader_failure(self):
        """Test what happens if the leader fails and a new election is conducted."""
        # Start the election process and let node 5 become the leader
        for node in self.nodes[1:]:
            node.start_election()
            if node.is_leader:
                break
        
        # Check that node 5 is the leader
        self.assertTrue(self.nodes[-1].is_leader, "Node 5 should be the leader")

        # Fail the leader (node 5)
        self.nodes[-1].fail_node()

        # Start a new election process after leader failure
        for node in self.nodes:
            if node.active:
                node.start_election()
                if node.is_leader:
                    break

        # Node 4 should be the new leader since node 5 has failed
        self.assertTrue(self.nodes[-2].is_leader, "Node 4 should be the new leader after node 5 failure")

if __name__ == '__main__':
    unittest.main()

