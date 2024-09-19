# Bully Election Algorithm - Distributed Systems Project

This project is part of the Distributed Systems course in the 5th semester of Computer Science. It is a collaborative effort by:
- Amad
- Alan
- Mohammed
- Mathies

## Project Overview
This project focuses on implementing and optimizing the **Bully Election Algorithm** for leader election in distributed systems. Leader election is crucial for many distributed systems, where a single node or process must act as the leader to coordinate tasks. The project involves designing, implementing, verifying, and comparing:

- The **original Bully Election Algorithm**.
- An **improved version of the Bully Election Algorithm** optimized for message complexity and optionally time and space complexities.

The project is designed using UML diagrams to model the behavior of the algorithms, and it is implemented in Python. Optionally, the system can be deployed using **Docker** containers and orchestrated with **Kubernetes** to simulate a real distributed system.

## How the Bully Election Algorithm Works
The Bully Election Algorithm operates as follows:

1. A node detects the leader has failed.
2. It starts a leader election by sending election messages to all higher-ID nodes.
3. If a higher-ID node responds, it takes over the election.
4. The node with the highest ID eventually becomes the leader.
   
The algorithm is effective but may generate a high volume of messages, particularly in large distributed systems.

## Project Structure (for now)
The repository is organized as follows:

- `/docs`: Contains the UML diagrams made in draw.io in the design phase.
- `/src`: Contains the Python source code for both the original and improved versions of the Bully Election algorithm.
- `/tests`: Unit tests and system tests for verifying the correctness of the algorithms.

## Requirements
- **Python 3.x**
- **Pytest 8.3.3**

## VS Code extensions for UML-diagrams
- **Draw.io Integration v1.6.6 or later**

## Installation and Setup (for now)
1. Clone the repository:
    ```bash
    git clone https://github.com/<your-group>/<repo-name>.git
    cd <repo-name>
    ```

2. Install the necessary Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. To run the original Bully Election algorithm:
    ```bash
    python src/simple_bully_election.py
    ```

## Running the Tests
1. Running `simple_bully_algorithm_test.py` from root:
    ```bash
    pytest
    ```

