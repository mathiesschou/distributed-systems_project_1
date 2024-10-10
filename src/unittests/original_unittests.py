import unittest
from unittest.mock import patch
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from original_bully_algorithm import Node

class TestNode(unittest.TestCase):

    def setUp(self):
        # Create a network of nodes
        self.node1 = Node(1, [])
        self.node2 = Node(2, [])
        self.node3 = Node(3, [])
        self.node4 = Node(4, [])

        # Set the nodes' references to each other
        self.node1.nodes = [self.node2, self.node3, self.node4]
        self.node2.nodes = [self.node1, self.node3, self.node4]
        self.node3.nodes = [self.node1, self.node2, self.node4]
        self.node4.nodes = [self.node1, self.node2, self.node3]

    def test_send_message(self):
        """Test that a message is correctly sent to another active node."""
        with patch('builtins.print') as mocked_print:
            self.node1.send_message("Election", self.node2)
            mocked_print.assert_any_call("Node 1 sends Election to Node 2")
            mocked_print.assert_any_call("Node 2 received Election from Node 1")

    def test_receive_message_ok(self):
        """Test that a node correctly responds to an Election message by sending an OK."""
        with patch('builtins.print') as mocked_print:
            self.node2.receive_message("Election", self.node1)
            mocked_print.assert_any_call("Node 2 received Election from Node 1")
            mocked_print.assert_any_call("Node 2 handling Election message from Node 1")
            mocked_print.assert_any_call("Node 2 sends OK to Node 1")

    def test_start_election(self):
        """Test that a node starts an election and sends Election messages to higher nodes."""
        with patch('time.sleep', return_value=None):  # Patch sleep to avoid waiting
            with patch('builtins.print') as mocked_print:
                self.node2.start_election()
                mocked_print.assert_any_call("Node 2 starts an election.")
                mocked_print.assert_any_call("Node 2 sends Election to Node 3")
                mocked_print.assert_any_call("Node 2 sends Election to Node 4")

    def test_become_leader(self):
        """Test that a node becomes a leader and sends Coordinator messages."""
        with patch('builtins.print') as mocked_print:
            self.node3.become_leader()
            self.assertTrue(self.node3.is_leader)
            mocked_print.assert_any_call("Node 3 becomes the leader.")
            mocked_print.assert_any_call("Node 3 sends Coordinator to Node 1")
            mocked_print.assert_any_call("Node 3 sends Coordinator to Node 2")
            mocked_print.assert_any_call("Node 3 sends Coordinator to Node 4")

    def test_fail_node(self):
        """Test that a node fails and becomes inactive."""
        self.node3.fail_node()
        self.assertFalse(self.node3.active)

    def test_check_leader_status(self):
        """Test that nodes detect the absence of a leader and start a new election."""
        # Set up node3 as a leader and fail it
        self.node3.become_leader()
        self.node3.fail_node()

        with patch('builtins.print') as mocked_print:
            self.node1.check_leader_status()
            mocked_print.assert_any_call("Node 1 detects that there is no active leader. Starting a new election.")
            mocked_print.assert_any_call("Node 1 starts an election.")
    
if __name__ == '__main__':
    unittest.main()
