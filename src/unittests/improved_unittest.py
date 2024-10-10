import unittest
from unittest.mock import patch
import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from improved_bully_algorithm import Node




class TestNode(unittest.TestCase):

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


    @patch('time.sleep', return_value=None)  # To avoid waiting
    def test_send_message(self, _):
        """Test sending a message to an active node."""
        with patch('builtins.print') as mocked_print:
            self.node1.send_message("Hello", self.node2)
            self.assertIn("Node 1 sends Hello to Node 2", [call[0][0] for call in mocked_print.call_args_list])

    @patch('time.sleep', return_value=None)  # To avoid waiting
    def test_receive_election_message(self, _):
        """Test receiving an Election message."""
        self.node1.receive_message("Election", self.node2)
        self.assertTrue(self.node1.election_in_progress)

    @patch('time.sleep', return_value=None)  # To avoid waiting
    def test_receive_ok_message(self, _):
        """Test receiving an OK message."""
        self.node1.receive_message("OK", self.node2)
        self.assertTrue(self.node1.has_received_ok)
        self.assertTrue(self.node1.knows_higher_active)

    @patch('time.sleep', return_value=None)  # To avoid waiting
    def test_receive_coordinator_message(self, _):
        """Test receiving a Coordinator message."""
        self.node1.is_leader = True  # Setting it to true for the test
        self.node1.receive_message("Coordinator", self.node2)
        self.assertFalse(self.node1.is_leader)
        self.assertFalse(self.node1.election_in_progress)

    @patch('time.sleep', return_value=None)  # To avoid waiting
    def test_start_election_no_higher_node(self, _):
        """Test starting an election when no higher active nodes are available."""
        self.node1.start_election()  # Node 1 starts the election
        self.assertTrue(self.node1.is_leader)

    @patch('time.sleep', return_value=None)  # To avoid waiting
    def test_start_election_with_higher_nodes(self, _):
        """Test starting an election with higher active nodes."""
        self.node1.active = True  # Ensure Node 1 is active
        self.node4.start_election()  # Node 4 should initiate an election

        with patch('builtins.print') as mocked_print:
            self.node1.start_election()
            self.assertTrue(self.node1.is_leader)
            self.assertFalse(self.node4.is_leader)

            # Check the printed output for expected messages
            mocked_print.assert_any_call("Node 1 becomes the leader.")

    @patch('time.sleep', return_value=None)  # To avoid waiting
    def test_become_leader(self, _):
        """Test the behavior of becoming a leader."""
        self.node1.start_election()  # Should not become a leader yet
        self.node1.become_leader()
        self.assertTrue(self.node1.is_leader)

    @patch('time.sleep', return_value=None)  # To avoid waiting
    def test_fail_node(self, _):
        """Test simulating a node failure."""
        self.node1.fail_node()
        self.assertFalse(self.node1.active)

    @patch('time.sleep', return_value=None)  # To avoid waiting
    def test_check_leader_status(self, _):
        """Test checking the leader status and starting a new election if needed."""
        self.node4.is_leader = True  # Make Node 4 the leader
        self.node4.active = False  # Simulate failure of Node 4
        self.node1.check_leader_status()  # Should trigger a new election, which will result in node 1 being the leader
        self.assertTrue(self.node1.is_leader)

if __name__ == '__main__':
    unittest.main()


