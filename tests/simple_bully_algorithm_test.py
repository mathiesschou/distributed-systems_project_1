import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.simple_bully_algorithm import Node

def setup_module(module):
    """ Setup """
    global nodes
    nodes = [Node(i, []) for i in range(1, 6)]
    for node in nodes:
        node.nodes = nodes

def test_leader_elected():
    # Start from node 2. Expect node 5 as leader.
    for node in nodes[1:]:
        node.start_election()
        if node.is_leader:
            break
    assert nodes[-1].is_leader == True, "Node 5 should be the leader"

def test_lower_node_not_leader():
    # Node 1 should not be the leader.
    for node in nodes[1:]:
        node.start_election()
        if node.is_leader:
            break
    assert not nodes[0].is_leader, "Node 1 should not be the leader"

def test_election_starts_from_node_2():
    # Ensuring node 2 does not include node 1 in election. 
    for node in nodes[1:]:
        node.start_election()
    assert not nodes[0].is_leader, "Node 1 should not participate in the election"
