import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import copy

#genomeA = [[1,4,5,6,2,3],[7,8,9]]
#genomeB = [[1,2,3,4,5,6,7],[8,9]]

genomeA = [[1,2,3], [6,7,8,9,4,5], [10,13,14,11,12,15]]
genomeB = [[1,2,3,4,5],[6,7,8,9],[10,11,12,13,14,15]]

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



def greedy_DCJ_sorting(adjacencies_genomeA, adjacencies_genomeB):
    for element in adjacencies_genomeB:
        #if element is an adjacency:
        if type(element) is tuple:
            print('adjacency: ',element)
            p = element[0]
            q = element[1]

            p_element = [(x,y) for x,y in adjacencies_genomeA if x == p or y ==  p]
            if len(p_element) != 0:

                u = p_element[0]
            #else the element of A containing p is a telomere
            else:
                #u = (p, '.')
                u = p

            q_element = [(x, y) for x, y in adjacencies_genomeA if x == q or y == q]
            if len(q_element) != 0:
                v = q_element[0]

            #else the element of A containing q is a telomere
            else:
                #v = (q, '.')
                v = q

            if u != v:
                adjacencies_genomeA.append((p, q))
                adjacencies_genomeA.remove(u)
                adjacencies_genomeA.remove(v)

                #if u is an adjacency:
                if type(u) is tuple:
                    #if v is an adjacency:
                    if type(v) is tuple:
                        adjacencies_genomeA.append(([extremity for extremity in u if extremity != p][0], [extremity for extremity in v if extremity != q][0]))
                    #else v is a telomere
                    else:
                        adjacencies_genomeA.append([extremity for extremity in u if extremity != p][0])

                #else u is a telomere
                else:
                    #if v is an adjacency
                    if type(v) is tuple:
                        adjacencies_genomeA.append([extremity for extremity in v if extremity != q][0])



        #else if the element is a telomere:

        elif type(element) is str:
            print('telomere: ', element)

            p = element

            p_element = [(x,y) for x, y in adjacencies_genomeA if x == p or y == p]

            if len(p_element) != 0:
                u = p_element[0]
            #else the element of A containing p is a telomere
            else:
                u = p


            #if u is not a telomere:
            if u != p:
                adjacencies_genomeA.append(u[0])
                adjacencies_genomeA.append(u[1])
                adjacencies_genomeA.remove(u)

        print(adjacencies_genomeA)

    return adjacencies_genomeA

#sortingA = greedy_DCJ_sorting(adjacencies_genomeA, adjacencies_genomeB)
#print(sortingA)

def sort_one_level_down(adjacencies_genomeA, adjacencies_genomeB):
    level_operations = []
    level_adjacency_intermediates = []
    adjacencies_genomeA_copy= copy.deepcopy(adjacencies_genomeA)

    for element in adjacencies_genomeB:
        adjacencies_genomeA_intermediate = copy.deepcopy(adjacencies_genomeA)
        # if element is an adjacency:
        if type(element) is tuple:
            print('adjacency: ', element)
            p = element[0]
            q = element[1]

           

            p_element = [(x, y) for x, y in adjacencies_genomeA_intermediate if x == p or y == p]
            if len(p_element) != 0:

                u = p_element[0]
            # else the element of A containing p is a telomere
            else:
                # u = (p, '.')
                u = p

            q_element = [(x, y) for x, y in adjacencies_genomeA_intermediate if x == q or y == q]
            if len(q_element) != 0:
                v = q_element[0]

            # else the element of A containing q is a telomere
            else:
                # v = (q, '.')
                v = q

            print('u: ',u, '    v: ',v)
            if u != v:
                adjacencies_genomeA_intermediate.append((p, q))
                adjacencies_genomeA_intermediate.remove(u)
                adjacencies_genomeA_intermediate.remove(v)

                # if u is an adjacency:
                if type(u) is tuple:
                    # if v is an adjacency:
                    if type(v) is tuple:
                        adjacencies_genomeA_intermediate.append(([extremity for extremity in u if extremity != p][0],
                                                    [extremity for extremity in v if extremity != q][0]))
                        operation = ((u, v), ((p,q), ([extremity for extremity in u if extremity != p][0],
                                                    [extremity for extremity in v if extremity != q][0])))
                        level_operations.append((operation))
                        level_adjacency_intermediates.append((adjacencies_genomeA_intermediate))

                    # else v is a telomere
                    else:
                        adjacencies_genomeA_intermediate.append([extremity for extremity in u if extremity != p][0])
                        operation = ((u,v), ((p,q), ([extremity for extremity in u if extremity != p][0])))
                        level_operations.append((operation))
                        level_adjacency_intermediates.append((adjacencies_genomeA_intermediate))

                # else u is a telomere
                else:
                    # if v is an adjacency
                    if type(v) is tuple:
                        adjacencies_genomeA_intermediate.append([extremity for extremity in v if extremity != q][0])
                        operation = ((v, u),((p,q), ([extremity for extremity in v if extremity != q][0])))
                        level_operations.append((operation))
                        level_adjacency_intermediates.append((adjacencies_genomeA_intermediate))
                    #else v is a telomere
                    else:
                        operation = ((u),(v),((p,q)))
                        level_operations.append(operation)
                        level_adjacency_intermediates.append(adjacencies_genomeA_intermediate)






        # else if the element is a telomere:

        elif type(element) is str:
            print('telomere: ', element)

            p = element

            p_element = [(x, y) for x, y in adjacencies_genomeA_intermediate if x == p or y == p]

            if len(p_element) != 0:
                u = p_element[0]
            # else the element of A containing p is a telomere
            else:
                u = p

            # if u is not a telomere:
            if u != p:
                adjacencies_genomeA_intermediate.append(u[0])
                adjacencies_genomeA_intermediate.append(u[1])
                adjacencies_genomeA_intermediate.remove(u)
                operation = ((u), (u[0]), (u[1]))
                level_operations.append((operation))
                level_adjacency_intermediates.append((adjacencies_genomeA_intermediate))


    return level_operations, level_adjacency_intermediates


sort_down = sort_one_level_down(adjacencies_genomeA, adjacencies_genomeB)
print()
print(sort_down[0])
print(sort_down[1])

for i in range(0, len(sort_down[0])):
    print()
    print(i)
    print(adjacencies_genomeA)
    print(sort_down[0][i])
    print(sort_down[1][i])

print()

print(adjacencies_genomeA)
print(adjacencies_genomeB)

#[((('1h', '4t'), ('6h', '2t')), (('1h', '2t'), ('4t', '6h'))), (('3h', ('1h', '4t')), (('3h', '4t'), '1h')), ((('6h', '2t'), '7t'), (('6h', '7t'), '2t')), (('7h', '8t'), ('7h', ('7h', '8t'))), (('7h', '8t'), ('8t', ('7h', '8t')))]