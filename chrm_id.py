from Class_DCJ_Node import Node
from Class_extremities_and_adjacencies import Extremities_and_adjacencies

genomeA = [[1,-3,-2, 4, 5,6,9,7], [8, 10]]
genomeB = [[1, 2,3 ,4 , 5, 6, 7], [8, 9, 10]]

#from genes to adjacencies
get_adjacencies = Extremities_and_adjacencies()
adjacencies_genomeA = get_adjacencies.adjacencies_ordered_and_sorted(genomeA)
adjacencies_genomeB = get_adjacencies.adjacencies_ordered_and_sorted(genomeB)

print('Adjacencies of the genomes: ')
print('Genome A: ', adjacencies_genomeA)
print('Genome B: ', adjacencies_genomeB)
print('____________________________________')
print()
print()





def find_chromosomes(adjacencies):

    telomeres = [element for element in adjacencies if type(element) is not tuple]
    not_telomeres = [element for element in adjacencies if type(element) is tuple]
    linear_chromosomes = []
    circular_chromosomes = []
    chromosome = []

    while len(telomeres) > 0:
        current = telomeres[0]

        telomeres.remove(current)
        chromosome.append(current)

        if current%1 == 0:
            next_extremity = current+0.5
        else:
            next_extremity = current-0.5

        if next_extremity in telomeres:
            current = next_extremity

            telomeres.pop(current)
            chromosome.append(current)
            linear_chromosomes.append(chromosome)
            chromosome = []

        else:

            #find_adjacency_cycle(next_extremity, chromosome, not_telomeres)
            cycle_result = find_adjacency_cycle(next_extremity, chromosome, not_telomeres)
            print('CYCLE RESULT: ', cycle_result)
            if cycle_result is not None:
                print(cycle_result[0])
                print(cycle_result[1])
                print(cycle_result[2])
                print('____________________________')
                next_extremity = cycle_result[0]
                chromosome = cycle_result[1]
                not_telomeres = cycle_result[2]

                print('next_extremity = ', next_extremity)
                print('chromosome: ', chromosome)
                print('not_telomeres: ', not_telomeres)
                print()
                print('*********')
                print('next: ', next_extremity)
                print('telomeres: ', telomeres)
                print('***************')
                if next_extremity in telomeres:
                    print('LAST TELOMERE ADDIONTION EXCECUTION')
                    current = next_extremity
                    telomeres.remove(current)
                    chromosome.append(current)
                    linear_chromosomes.append(chromosome)
                    chromosome = []
            else:
                pass



    while len(not_telomeres) > 0:
        current = not_telomeres[0]
        not_telomeres.remove(current)
        chromosome.append(current)

        if current[0]%1==0:
            next_extremity = current[0]+0.5
        else:
            next_extremity = current[0]-0.5

        #if it is a single gene chromosome:
        if next_extremity == current[1]:
            circular_chromosomes.append(chromosome)
            chromosome=[]
            pass

        #if end of the circular chromosomes:
        elif next_extremity == chromosome[0][1]:
            circular_chromosomes.append(chromosome)
            chromosome = []
            pass

        else:
            find_adjacency_cycle(next_extremity, chromosome, not_telomeres)

    print('IS RETURNING')
    print('________________')
    print('telomeres: ', telomeres)
    print('not telomeres: ', not_telomeres)
    print('_________________________')
    return linear_chromosomes, circular_chromosomes


def find_adjacency_cycle(next_extremity, chromosome, not_telomeres):



    #if element not in not_telomeres at all, need to know

    i=0
    while i < len(not_telomeres):
        if not_telomeres[i][0] == next_extremity or not_telomeres[i][1] == next_extremity:
            current =not_telomeres[i]
            break
        else:
            i+=1
    else:
        print('----------------------------')
        print('extremity: ', next_extremity)
        print('chromosome: ', chromosome)
        print('not telomeres: ', not_telomeres)
        print('-----------------------------')
        return next_extremity, chromosome, not_telomeres

    not_telomeres.remove(current)
    chromosome.append(current)

    if current[0] == next_extremity:
        if current[1]%1==0:
            next_extremity = current[1] +0.5
        else:
            next_extremity = current[1]-0.5
    else:
        if current[0]%1==0:
            next_extremity = current[0]+0.5
        else:
            next_extremity = current[0]-0.5

    print('--> ', next_extremity)
    find_adjacency_cycle(next_extremity, chromosome, not_telomeres)



chromosomes = find_chromosomes(adjacencies_genomeB)

print(chromosomes[0])
print()
print(chromosomes[1])

