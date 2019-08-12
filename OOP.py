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
                            level_operations.append(operation)
                            level_adjacency_intermediates.append(adjacencies_genomeA_intermediate)


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
        #(i) adjacency + adjacency --> adjacency +adjacency
        if type(operation[0]) is tuple and type(operation[-1]) is tuple:


        #fission
        elif (type(operation[0]) is tuple and type(operation[-1]) is str):

        #fusion
        elif (type(operation[0]) is str and type(operation[-1]) is tuple):

        elif (type(operation[0]) is


   #(ii) telomere +telomer --> adjacency

   #fission: (('3h', '4t'), '3h', '4t'): (a,b) --> a, b
   #fusion: ('3h', '4t', ('3h', '4t')): a, b __> (a,b)
   #balanced translocation: ((('7h', '4t'), ('3h', '8t')), (('7h', '8t'), ('4t', '3h'))): (a,b),(c,d) --> (a,c),(b,d)
   #unbalanced translocation: (('3h', ('9h', '4t')), (('3h', '4t'), '9h')): a, (b,c) --> (a,b), c
   #transposition: ((('5h', '8t'), ('3h', '6t')), (('5h', '6t'), ('8t', '3h'))): (a,b),(c,d) --> (a,c),(b,d)




genomeA = [[1,4,5,6,2,3],[7,8]]
genomeB = [[1,2,3,4,5,6,7],[8]]

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
    print(op)



