#!/usr/bin/env python

import math
from pomegranate import *

#Lo hago una vez para Alice
# represents whether The Directory is a reputable publication
def create_bn_example1(name, reputable_prob, calif_prob):
    print(f"\t {name}:")
    print(f"\t\t Prior value: {calif_prob}")
    node_v = DiscreteDistribution( { 'Reputable' : reputable_prob, 'NoReputable' : 1-reputable_prob } )

    # represents whether or not Carol is qualified for the promotion
    node_h = DiscreteDistribution( { 'Calificado' : calif_prob, 'NoCalificado' : 1-calif_prob } )

    # represents whether Carol is featured in the Directory
    node_d = ConditionalProbabilityTable([
        ['NoReputable', 'NoCalificado', 'Promovido', 0.5],
        ['NoReputable', 'NoCalificado', 'NoPromovido', 0.5],

        ['NoReputable', 'Calificado', 'Promovido', 0.1],
        ['NoReputable', 'Calificado', 'NoPromovido', 0.9],

        ['Reputable', 'NoCalificado', 'Promovido', 0.1],
        ['Reputable', 'NoCalificado', 'NoPromovido', 0.9],

        ['Reputable', 'Calificado', 'Promovido', 0.9],
        ['Reputable', 'Calificado', 'NoPromovido', 0.1]
    ],[node_v,node_h])

    v=Node(node_v, name="V")
    h=Node(node_h, name="H")
    d=Node(node_d, name="D")

    network = BayesianNetwork("The promotion")
    network.add_nodes(v,h,d)
    network.add_edge(v,d)
    network.add_edge(h,d)
    network.bake()

    prediction = network.predict_proba({'D':'Promovido'})[1]
    print(f"\t\t Updated value: {prediction.parameters[0]['Calificado']}")


print("Running example 1:")
create_bn_example1("Alice", 0.99, 0.6)
create_bn_example1("Bob", 0.1, 0.4)



def create_bn_example4(name, liberal, spend):
    print(f"\t {name}:")
    #V1 ={‘Fiscally conservative’= 0,‘Fiscally liberal’= 1}
    #Represents the optimal economy philosophy
    node_v1 =  DiscreteDistribution( { 'Conservador' : 1-liberal, 'Liberal' : liberal } )
    #V2 ={‘No spending’= 0,‘Spending increase’= 1}
    #Represents the new bill's spending policy
    node_v2 =  DiscreteDistribution( { 'NoGasto' : 1-spend, 'Gasto' : spend } )

    #H={‘Bad policy’= 0,‘Good policy’= 1}
    node_h = ConditionalProbabilityTable([
        ["Conservador", "NoGasto", "Buena", 0.5],
        ["Conservador", "NoGasto", "Mala", 0.5],

        ["Conservador", "Gasto", "Buena", 0.1],
        ["Conservador", "Gasto", "Mala", 0.9],

        ["Liberal", "NoGasto", "Buena", 0.5],
        ["Liberal", "NoGasto", "Mala", 0.5],

        ["Liberal", "Gasto", "Buena", 0.9],
        ["Liberal", "Gasto", "Mala", 0.1],
    ],[node_v1, node_v2])

    #D={‘No spending’= 0,‘Spending increase’= 1}
    #Conclusion by independent study
    node_d = ConditionalProbabilityTable([
        ["NoGasto", "NoAumentaGasto", 0.9],
        ["NoGasto", "AumentaGasto", 0.1],

        ["Gasto", "AumentaGasto", 0.9],
        ["Gasto", "NoAumentaGasto", 0.1],
    ],[node_v2])

    v1=Node(node_v1, name="V1")
    v2=Node(node_v2, name="V2")
    h=Node(node_h, name="H")
    d=Node(node_d, name="D")

    network = BayesianNetwork("Political Belief")
    network.add_nodes(v1,v2,h,d)
    network.add_edge(v1,h)
    network.add_edge(v2,h)
    network.add_edge(v2,d)
    network.bake()

    #import pdb; pdb.set_trace()
    prediction = network.predict_proba({'D':'Gasto'}) 
    
    prev_val = network.marginal()[2].parameters[0]['Buena']
    print(f"\t\t Prior value: {prev_val}")

    print(f"\t\t Updated value: {prediction[2].parameters[0]['Buena']}")
    

print("Running example 4:")

create_bn_example4("Alice", 0.9, 0.5)
create_bn_example4("Bob", 0.1, 0.5)










print("Done")