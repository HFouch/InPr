from Class_DCJ_Node import Node
import networkx as nx
import matplotlib.pyplot as plt
class Network:

    def __init__(self, start_node, target_node, adjacenciesB):
        self.hash_table = {}
        self.start_node = start_node
        self.target_node = target_node
        self.adjacenciesB = adjacenciesB

        hash_key_start = hash(str(self.start_node.state))
        hash_key_target = hash(str(self.target_node.state))
        self.hash_table.update({hash_key_start: self.start_node})
        self.hash_table.update({hash_key_target: self.target_node})
        print('Hash', self.hash_table)



    # Build network
    def build_hash_table(self, current_node):
        node = current_node

        # if node is equivalent if hash(str(node.state)) == hash(str(target_node.state)):

        if node.is_equivalent(self.adjacenciesB):
            # if hash(str(node.state)) == hash(str(target_node.state)):

            pass

        #if previous operation was a circularization
        if node.next_operation != 0:
            print('the next op will be: ', node.next_operation)
            child_state = node.take_action(node.next_operation)
            # check whether in hash table:
            check_hash_table = Network.check_hash_key(self, child_state)

            # if in hash table:
            if check_hash_table[0]:
                child = check_hash_table[1]
                node.children.append(child)
                pass

            # if not in hash table
            else:
                child = Node(child_state)
                child.find_chromosomes(child.state)

                #if a circular chromosome was formed
                if len(child.circular_chromosomes) != 0:
                    for adjacency in node.next_operation[1]:
                        if adjacency in child.circular_chromosomes[0]:
                            circular_join = adjacency
                            potential_operation = child.check_if_operation_exists(circular_join, self.adjacenciesB)
                            if potential_operation:
                                child.next_operation = potential_operation

                hash_key = hash(str(child.state))
                self.hash_table.update({hash_key: child})
                node.children.append(child)
                Network.build_hash_table(self, child)


        #if the previous operation did not resilt in the formation of a circular chromosomal intermediate:
        operations = node.get_legal_operations(self.adjacenciesB)

        for operation in operations:
            child_state = node.take_action(operation)

            # check whether in hash table:
            check_hash_table = Network.check_hash_key(self, child_state)

            #if in hash table:
            if check_hash_table[0]:
                child = check_hash_table[1]
                node.children.append(child)
                pass

            #if not in hash table
            else:
                child = Node(child_state)
                child.find_chromosomes(child.state)
                print('circular chromosomes: ', child.circular_chromosomes)
                if len(child.circular_chromosomes) != 0:
                    print('operation: ', operation)
                    for adjacency in operation[-1]:
                        if adjacency in child.circular_chromosomes[0]:
                            circular_join = adjacency

                            potential_operation = child.check_if_operation_exists(circular_join, self.adjacenciesB)

                            if potential_operation:
                                child.next_operation = potential_operation


                hash_key = hash(str(child.state))
                self.hash_table.update({hash_key: child})
                node.children.append(child)
                Network.build_hash_table(self, child)

        return self.hash_table

    def check_hash_key(self, child_state):
        key = hash(str(child_state))
        if key in self.hash_table.keys():
            return True, self.hash_table.get(key)
        return False, None

    def build_network(self):
        network = nx.DiGraph()
        nodes = []
        Network.build_hash_table(self, self.start_node)
        list_of_values = self.hash_table.values()
        for value in list_of_values:
            if value not in nodes:
                nodes.append(value)
        for node in nodes:
            network.add_node(node)
        for node in nodes:
            for child in node.children:
                network.add_edge(node, child)

        return network

    def get_all_shortest_paths(self):
        network = Network.build_network(self)
        all_paths = nx.all_simple_paths(network, self.start_node, self.target_node)
        return all_paths
