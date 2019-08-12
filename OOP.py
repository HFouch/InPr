import copy

class Node:

    def __init__(self, adjacencies):
        self.state = adjacencies

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

                #find element of A containing p:
                p_elementA = [(x,y) for x,y in adjacenciesA_copy if x==p or y==p]

                #if element with p in A is an adjacency:
                if len(p_elementA) != 0:
                    u = p_elementA[0]

                #else it is a telomer:
                else:
                    u = p

                #find element of A containing q
                q_elementA = [(x,y) for x,y in adjacenciesA_copy if x==q or y==q]

                # if element with q in A is an adjacency:
                if len(q_elementA) != 0:
                    v = q_elementA[0]

                # else it is a telomer:
                else:
                    v = q

                #if the element of B is not also an element of A:
                if u!=v:
                    # if u is an adjacency:
                    if type(u) is tuple:
                        #if v is an adjacency:
                        if type(v) is tuple:
                            operation = ((v,u), ((p,q), ([extremity for extremity in u if extremity != p][0],
                                                    [extremity for extremity in v if extremity != q][0])))
                            list_of_legal_operations.append(operation)
                        #else v is a telomere
                        else:
                            operation = ((u, v), ((p, q), ([extremity for extremity in u if extremity != p][0])))
                            list_of_legal_operations.append(operation)
                    #else u is a telomere
                    else:
                        #if v is an adjacency
                        if type(v) is tuple:
                            operation = ((v,u), ((p, q), ([extremity for extremity in v if extremity != q][0])))
                            list_of_legal_operations.append(operation)
                        # else v is a telomere
                        else:
                            operation = ((u),(v),((p,q)))
                            list_of_legal_operations.append(operation)



            #else if the element in B is a telomere:
            elif type(element) is str:
                p = element
                p_elementA = [(x,y) for x,y in adjacenciesA_copy if x==p or y==p]

                #if the element in A containg p is an adjacency:
                if len(p_elementA)!=0:
                    u = p_elementA[0]
                #else the element of A containing p is a telomere
                else:
                    u=p
                #if u is not a telomere:
                if u!=p:
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
                state_copy.append(operation[2])

        #else it is another rearrangment
        elif len(operation) == 2:
            #transpositions, balanced translcations and block interchanges:
            if type(operation[0]) is tuple and type(operation[-1]) is tuple:
                state_copy.remove(operation[0][0])
                state_copy.remove(operation[0][1])
                state_copy.append(operation[1][0])
                state_copy.append(operation[1][1])


            #unbalanced translocations
            elif type(operation[0]) is tuple and type(operation[-1]) is str:
                state_copy.remove(operation[0][0])
                state_copy.remove(operation[0][1])
                state_copy.append(operation[1][0])
                state_copy.append(operation[1][1])


        else:
            #RAISE AN ERROR
            print("YOU'VE GOT A PROBLEM DARLING")

        return state_copy






genomeB = [[1,2,3],[4,5,6,7,8]]
genomeA = [[1,2,3],[4,6,7,5,8]]

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

gene_extremities_genomeA = gene_extremities(genomeA)
gene_extremities_genomeB = gene_extremities(genomeB)

print(gene_extremities_genomeA)

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

adjacencies_genomeA = create_adjacency_list(gene_extremities_genomeA)
print('genome A adjacencies: ', adjacencies_genomeA)
adjacencies_genomeB = create_adjacency_list(gene_extremities_genomeB)
print('genome B adjacencies: ', adjacencies_genomeB)

currentnode = Node(adjacencies_genomeA)

ops = currentnode.get_legal_operations(adjacencies_genomeB)
for op in ops:
    print(adjacencies_genomeA)
    print(op)
    takeAct = currentnode.take_action(op)

    print(takeAct)
    print()






