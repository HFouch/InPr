import copy

class Node:

    def __init__(self, adjacencies, parent = None):
        self.state = adjacencies
        self.parent_operation = None
        self.previous = None
        self.next = None
        self.h = 0
        self.g = 0
        self.f = 0


    def get_legal_operations(self, adjacenciesB ):
        list_of_legal_operations = []
        adjacenciesA = self.state
        adjacenciesB = adjacenciesB

        for element in adjacenciesB:
            adjacenciesA_copy = copy.deepcopy(adjacenciesA)

            #if element is an adjacency:
            if type(element) is tuple:
                p = element[0]
                q = element[1]
                u=0
                v=0

                #if elements containing p and q respectively in a are adjacencies
                for marker in adjacenciesA_copy:
                    if type(marker) is tuple:
                        if marker[0] == p or marker[1] == p:
                            u = marker
                            print('u: ', u)
                        if marker[0] == q or marker[1] == q:
                            v = marker
                            print('v: ', v)

                # element containing p in A is a telomere
                if u == 0:
                    u = p
                # element containing q in A is a telomere
                if v == 0:
                    v = q

                
                if u != v:
                    adjacenciesA_copy.append((p,q))
                    adjacenciesA_copy.remove(u)
                    adjacenciesA_copy.remove(v)

                    # if u is an adjacency:
                    if type(u) is tuple:
                        # calcultate u'p
                        if u[0] == p:
                            u_not_p = u[1]
                        else:
                            u_not_p = u[0]

                        # if v is an adjacency:
                        if type(v) is tuple:
                            # calcultate v'q
                            if v[0] == q:
                                v_not_q = v[1]
                            else:
                                v_not_q = v[0]

                            adjacenciesA_copy.append((u_not_p, v_not_q))
                            operation = ((u, v), ((p, q), (u_not_p, v_not_q)))
                            list_of_legal_operations.append((operation))


                        # else v is a telomere
                        else:
                            adjacenciesA_copy.append(u_not_p)
                            operation = ((u, v), ((p, q), (u_not_p)))
                            list_of_legal_operations.append((operation))


                   #else u is a telomere
                    else:
                        # if v is an adjacency
                        if type(v) is tuple:
                            #calculate v'q
                            if v[0] == q:
                                v_not_q = v[1]
                            else:
                                v_not_q = v[0]
                            adjacenciesA_copy.append(v_not_q)
                            operation = ((v,u),((p,q),(v_not_q)))
                            list_of_legal_operations.append(operation)

                        #e;se v is a telomere
                        else:
                            operation = (u,v,((p,q)))
                            list_of_legal_operations.append(operation)

            #else if the element is a telomere
            elif type(element) is str:
                u = 0
                p = element

                for marker in adjacenciesA_copy:
                    if type(marker) is tuple:
                        if marker[0] == p or marker[1] == p:
                            u = marker

                if u == 0 :
                    u=p

                #if u is not a telomere:
                if u != p:
                    adjacenciesA_copy.append(u[0])
                    adjacenciesA_copy.append(u[1])
                    adjacenciesA_copy.remove(u)
                    operation = ((u), (u[0]), (u[1]))
                    list_of_legal_operations.append(operation)

        return list_of_legal_operations




    def take_action(self, operation):

        state_copy = copy.deepcopy(self.state)

        #if it is a fusion or fission:
        if len(operation) == 3:

            #fission
            if type(operation[0]) is tuple:
                state_copy.remove(operation[0])
                state_copy.append(operation[1])
                state_copy.append(operation[2])

            #fusion
            else:
                state_copy.remove(operation[0])
                state_copy.remove(operation[1])

                #ensure gene extremities in correct order for downstream comparisions with genome B extremities
                if operation[2][0][0] < operation[2][1][0]:
                    state_copy.append(operation[2])
                else:
                    state_copy.append((operation[2][1], operation[2][0]))

        #else it is another rearrangment
        elif len(operation) == 2:
            #transpositions, balanced translcations and block interchanges:
            if type(operation[0]) is tuple and type(operation[-1]) is tuple:
                state_copy.remove(operation[0][0])
                state_copy.remove(operation[0][1])

                # ensure gene extremities in correct order for downstream comparisions with genome B extremities
                if operation[1][0][0][0] < operation[1][0][1][0]:
                    state_copy.append(operation[1][0])
                else:
                    state_copy.append((operation[1][0][1], operation[1][0][0]))

                print('operation: ', operation)
                if operation[1][1][0][0] < operation[1][1][1][0]:
                    state_copy.append(operation[1][1])
                else:
                    state_copy.append((operation[1][1][1], operation[1][1][0]))



            #unbalanced translocations
            elif type(operation[0]) is tuple and type(operation[-1]) is str:
                state_copy.remove(operation[0][0])
                state_copy.remove(operation[0][1])

                # ensure gene extremities in correct order for downstream comparisions with genome B extremities
                if operation[1][0][0][0] < operation[1][0][1][0]:
                    state_copy.append(operation[1][0])
                else:
                    state_copy.append((operation[1][0][1], operation[1][0][0]))

                state_copy.append(operation[1][1])


        else:
            #RAISE AN ERROR
            print("YOU'VE GOT A PROBLEM DARLING")

        return state_copy

    def get_heuristic(self, adjacenciesB):
        adjacenciesA = self.state
        adjacenciesB = adjacenciesB

        counter = 0
        for adj in adjacenciesB:
            if adj in adjacenciesA:
                counter+=1

        heuristic = counter/2
        return heuristic

        pass

    def get_children(self, adjacenciesB ):
        pass

    def is_equivalent(self, adjacenciesB):
        adjacenciesA = copy.deepcopy(self.state)
        adjacenciesB = adjacenciesB

        ordered_adjacenciesA = []
        for element in adjacenciesA:
            if type(element) is tuple:
                if element[0][0] < element[1][0]:
                    ordered_adjacenciesA.append(element)
                else:
                    #adjacenciesA.remove(element)
                    ordered_adjacenciesA.append((element[1], element[0]))
            else:
                ordered_adjacenciesA.append(element)

        for element in adjacenciesB:
            if element in ordered_adjacenciesA:
                pass
            else:
                return False

        return True





    def aStar(self, start_state, end_state):
        #initialize open and closed sets
        openset = set()
        closedset = set()
        #set current state as the starting state
        current_state = start_state
        #add starting state to the open set
        openset.add(current_state)

        #while the open set is non empty:
        while openset:
            #find item with lowest f score (h score + g score)
            current_state = min(openset, key=lambda o: o.g + o.h)

            #if the current_state == the goal_state then retrace the path and return it
            if current_state == end_state:
                path = []
                while current_state.previous:
                    path.append(current_state)
                    current_state = current_state.previous
                path.append(current_state)
                return path[::-1]

            #remove item from openset
            openset.remove(current_state)
            #add item to clodes set
            closedset.add(current_state)
            #loop throught the current_state's children/siblings


def astar(start_state, end_state):

    #create start and end node
    start_node = Node(start_state, None)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(end_state, None)
    end_node.g = end_node.h = end_node.f = 0

    #initialize open and closed lists
    open_list = []
    closed_list = []

    #add start_node
    open_list.append(start_node)
    print('open list: ', open_list[0].state)

    while len(open_list)>0:

        #get current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        #pop current node off open list and add it to the closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        #if the end state is achieved:
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.state)
                current = current.parent
            return path [::-1]

        children = []
        for operation in current_node.get_legal_operations(end_state):
            new_state = current_node.take_action(operation)
            new_node = Node(new_state, current_node)
            children.append(new_node)

        #loop through children
        for child in children:

            #child is on the closed list
            for closed_child in closed_list:
                 if child == closed_child:
                     continue

            #calculate f, g, and h values
            child.g = current_node.g + 1
            child.h = child.get_heuristic(child.state)
            child.f = child.g + child.h

            #child is already in the open list
            # can use hash table hear if run out of memory

            #add child to open list
            open_list.append(child)











genomeA = [[1,2,-8,-7,3],[4,5,6,9, 10, 11]]
genomeB = [[1,2,3,4,5,6,7,8,9,10,11]]
#genomeA = [[1,2,3,4,5,6,7,8,9]]

def gene_extremities(genome):
    genome_gene_ext = []
    for chromosome in genome:
        chromosome_gene_ext = []
        for marker in chromosome:
            if int(marker) >= 0:
                marker_str = str(marker)
                chromosome_gene_ext.append(marker_str + 't')
                chromosome_gene_ext.append(marker_str + 'h')
            else:
                marker_str = str(abs(marker))
                chromosome_gene_ext.append(marker_str + 'h')
                chromosome_gene_ext.append(marker_str + 't')
        genome_gene_ext.append(chromosome_gene_ext)

    return genome_gene_ext


def create_adjacency_list(gene_extremities):
    adjacencies = []
    for chromosome in gene_extremities:
        i=0
        while i < len(chromosome):
            if chromosome[i] == chromosome[0] or chromosome[i] == chromosome[-1]:
                adjacencies.append((chromosome[i]))
                i +=1
            else:
                adjacencies.append((chromosome[i], chromosome[i+1]))
                i += 2
    return adjacencies

adjacencies_genomeA = create_adjacency_list(gene_extremities(genomeA))

adjacencies_genomeB = create_adjacency_list(gene_extremities(genomeB))


currentnode = Node(adjacencies_genomeA)

ops = currentnode.get_legal_operations(adjacencies_genomeB)
for op in ops:
    print(adjacencies_genomeA)
    print(op)
    takeAct = currentnode.take_action(op)

    print(takeAct)
    print()
print(currentnode.is_equivalent(adjacencies_genomeB))



'''
def main():

    start = adjacencies_genomeA
    end = adjacencies_genomeB
    path = astar(start,end)

    print(path)


if __name__ == '__main__':
    main()

'''

