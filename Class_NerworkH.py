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
        self.level = 0
        self.last_operation = False
        print('Hash', self.hash_table)



    # Build network
    def build_hash_table(self, current_node):
        node = current_node
        print('current: ', node, node.state)
        print('level: ', self.level)

        #check if node is target node
        #node is equivalent if hash(str(node.state)) == hash(str(target_node.state)):
        if node.is_equivalent(self.adjacenciesB):
            self.level=-1
            pass

        #check if a .next_operation exists

        # if .next_operation exists it is a decirculization and reinsertion
        if node.next_operation:
            print('there is a next op: ', node.next_operation)
            child_state = node.take_action(node.next_operation)
            print('child state: ', child_state)

            #check whether child state in #T:
            check_hash_table = Network.check_hash_key(self, child_state)

            #if child_state in #T
            if check_hash_table[0]:
                print('it is in #T')

                #child = the node in the #T with that state
                child = check_hash_table[1]
                node.children.append(child)

                print('the children: ', node.children)
                print()
                pass

            #if the child_state is not in the #T
            else:
                print('it is not in #T')
                child = Node(child_state)
                hash_key = hash(str(child.state))
                self.hash_table.update({hash_key: child})
                print('new #T: ', self.hash_table)
                node.children.append(child)
                self.level+=1
                print('the children: ', node.children)
                print()
                Network.build_hash_table(self, child)

        #else if no .next_operation exists:
        else:
            print('there is no next op')
            #get operations
            operations = node.get_legal_operations(self.adjacenciesB)

            #final return step up
            if node == self.start_node:
                operations.append('Return')

            print('Ops: ', operations)

            for operation in operations:
                if operation == 'Return':
                    print('')
                    print('IS RETURNING')
                    print()
                    return self.hash_table
                print('index: ', operations.index(operation), 'len: ',len(operations))

                else:

                if operations.index(operation) == len(operations)-1:
                    self.last_operation = True
                    print('this is the last op')
                else:
                    self.last_operation = False

                print('operation: ', operation)
                child_state = node.take_action(operation)
                print('childe state: ', child_state)
                #check whether in #T
                check_hash_table = Network.check_hash_key(self, child_state)

                #if in #T
                if check_hash_table[0]:
                    print('in #T')
                    # child = the node in the #T with that state
                    child = check_hash_table[1]
                    node.children.append(child)

                    print('the children: ', node.children)
                    pass

                # if the child_state is not in the #T
                else:
                    print('not in #T')
                    #make a child node
                    child = Node(child_state)
                    print('child: ',  child)

                    #check whether a circular chromosome has been created
                    child.find_chromosomes(child.state)

                    # if a circular chromosome has been created:
                    if len(child.circular_chromosomes) != 0:
                        print('there is a circle')
                        print('state: ', child.state)

                        #get legal reinsertion operation
                        for adjacency in operation[-1]:
                            print('operation: ', operation)
                            if adjacency in child.circular_chromosomes[0]:
                                print('adj is in')
                                circular_join = adjacency
                                print('join: ', circular_join)
                                potential_operation = child.check_if_operation_exists(circular_join, self.adjacenciesB)
                                print('legal op: ', potential_operation)


                                #if the a legal operation exists:

                                if potential_operation:
                                    print('legal op exists')
                                    child.next_operation = potential_operation
                                    hash_key = hash(str(child.state))
                                    self.hash_table.update({hash_key: child})
                                    print('#T: ', self.hash_table)
                                    node.children.append(child)
                                    self.level+=1
                                    print('the children: ', node.children)
                                    Network.build_hash_table(self, child)
                                    print()

                                #else if there exists no legal reinsertion operation
                                else:
                                    print('there was no legal op.. moving on..')
                                    print()
                                    pass

                    # else if no circular chromosome has been created:
                    else:
                        print('no cicular chrms')
                        print('state: ', child.state)

                        hash_key = hash(str(child.state))
                        self.hash_table.update({hash_key: child})
                        print('#T: ', self.hash_table)
                        node.children.append(child)
                        self.level+=1
                        print('the children: ', node.children)
                        Network.build_hash_table(self, child)

        #return self.hash_table









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