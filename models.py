from pomegranate import *


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


def create_bn_example2(name, christian_prob):
    print(f"\t {name}:")
    
    #V = {‘Secular’ = 0, ‘Christian’ = 1} r
    node_v = DiscreteDistribution( { 'Secular' : 1-christian_prob, 'Cristiano' : christian_prob } )

    #H = {‘Human’ = 0, ‘Divine’ = 1}
    node_h = ConditionalProbabilityTable([
        ['Secular', 'Divino', 0.1],
        ['Secular', 'Humano', 0.9],

        ['Cristiano', 'Divino', 0.9],
        ['Cristiano','Humano', 0.9],       
        ],[node_v])


    # D = {‘Not persecuted’ = 0, ‘Persecuted’ = 1}
    node_d = ConditionalProbabilityTable([
        ['Secular', 'Humano', 'Perseguido', 0.4],
        ['Secular', 'Humano', 'NoPerseguido', 0.6],

        ['Secular', 'Divino', 'Perseguido', 0.01],
        ['Secular', 'Divino', 'NoPerseguido', 0.99],

        ['Cristiano', 'Humano', 'Perseguido', 0.4],
        ['Cristiano', 'Humano', 'NoPerseguido', 0.6],

        ['Cristiano', 'Divino', 'Perseguido', 0.6],
        ['Cristiano', 'Divino', 'NoPerseguido', 0.4],
    ],[node_v,node_h])

    v=Node(node_v, name="V")
    h=Node(node_h, name="H")
    d=Node(node_d, name="D")

    network = BayesianNetwork("Religious Belief")
    network.add_nodes(v,h,d)
    network.add_edge(v,d)
    network.add_edge(v,h)
    network.add_edge(h,d)
    network.bake()

    prev_val = network.marginal()[1].parameters[0]['Divino']
    print(f"\t\t Prior value: {prev_val}")
    prediction = network.predict_proba({'D':'Perseguido'})[1].parameters[0]['Divino']
    print(f"\t\t Updated value: {prediction}")


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
    prediction = network.predict_proba({'D':'AumentaGasto'}) 
    
    prev_val = network.marginal()[2].parameters[0]['Buena']
    print(f"\t\t Prior value: {prev_val}")

    print(f"\t\t Updated value: {prediction[2].parameters[0]['Buena']}")
   

def create_bn_example1_simulation(name, reputable_prob, calif_prob, i):
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
    #if i == 1:
    #    network.plot()

    prediction = network.predict_proba({'D':'Promovido'})[1]
    #print(f"\t {name}:")
    prev_val = calif_prob
    updated_val = prediction.parameters[0]['Calificado']
    #print(f"\t\t Prior value: {prev_val}")
    #print(f"\t\t Updated value: {updated_val}")
    if (prev_val < 0.5) and (updated_val < prev_val) and abs(updated_val - prev_val) > 0.1:
        #print("BELIEF UPDATE! From bad to even worse")
        #print(f"Case {sim_number} with values\
        #        \n\t Previous {prev_val} \n\t Updated {updated_val}")
        return True
    elif (prev_val > 0.5) and (updated_val > prev_val) and abs(updated_val - prev_val) > 0.1:
        #print("BELIEF UPDATE! From good to even better")
        #print(f"Case {sim_number} with values\
        #        \n\t Previous {prev_val} \n\t Updated {updated_val}")
        return True


def create_bn_example2_simulation(name, christian_prob, i):
    node_v = DiscreteDistribution( { 'Secular' : 1-christian_prob, 'Cristiano' : christian_prob } )

    #H = {‘Human’ = 0, ‘Divine’ = 1}
    node_h = ConditionalProbabilityTable([
        ['Secular', 'Divino', 0.1],
        ['Secular', 'Humano', 0.9],

        ['Cristiano', 'Divino', 0.9],
        ['Cristiano','Humano', 0.9],       
        ],[node_v])


    # D = {‘Not persecuted’ = 0, ‘Persecuted’ = 1}
    node_d = ConditionalProbabilityTable([
        ['Secular', 'Humano', 'Perseguido', 0.4],
        ['Secular', 'Humano', 'NoPerseguido', 0.6],

        ['Secular', 'Divino', 'Perseguido', 0.01],
        ['Secular', 'Divino', 'NoPerseguido', 0.99],

        ['Cristiano', 'Humano', 'Perseguido', 0.4],
        ['Cristiano', 'Humano', 'NoPerseguido', 0.6],

        ['Cristiano', 'Divino', 'Perseguido', 0.6],
        ['Cristiano', 'Divino', 'NoPerseguido', 0.4],
    ],[node_v,node_h])

    v=Node(node_v, name="V")
    h=Node(node_h, name="H")
    d=Node(node_d, name="D")

    network = BayesianNetwork("Religious Belief")
    network.add_nodes(v,h,d)
    network.add_edge(v,d)
    network.add_edge(v,h)
    network.add_edge(h,d)
    network.bake()

    prev_val = network.marginal()[1].parameters[0]['Divino']
    #print(f"\t\t Prior value: {prev_val}")
    updated_val = network.predict_proba({'D':'Perseguido'})[1].parameters[0]['Divino']
    #print(f"\t\t Updated value: {updated_val}")
    if (prev_val < 0.5) and (updated_val < prev_val) and abs(updated_val - prev_val) > 0.1:
        #print("BELIEF UPDATE! From bad to even worse")
        #print(f"Case {sim_number} with values\
        #        \n\t Previous {prev_val} \n\t Updated {updated_val}")
        return True
    elif (prev_val > 0.5) and (updated_val > prev_val) and abs(updated_val - prev_val) > 0.1:
        #print("BELIEF UPDATE! From good to even better")
        #print(f"Case {sim_number} with values\
        #        \n\t Previous {prev_val} \n\t Updated {updated_val}")
        return True


def create_bn_example4_simulation(name, liberal, spend, sim_number):
    #print(f"\t {name}:")
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
    prediction = network.predict_proba({'D':'AumentaGasto'}) 
    
    prev_val = network.marginal()[2].parameters[0]['Buena']
    updated_val = prediction[2].parameters[0]['Buena']
    #print(f"\t\t Prior value: {prev_val}")
    #print(f"\t\t Updated value: {updated_val}")
    if (prev_val < 0.5) and (updated_val < prev_val) and abs(updated_val - prev_val) > 0.1:
        #print("BELIEF UPDATE! From bad to even worse")
        #print(f"Case {sim_number} with values\
        #        \n\t Previous {prev_val} \n\t Updated {updated_val}")
        return True
    elif (prev_val > 0.5) and (updated_val > prev_val) and abs(updated_val - prev_val) > 0.1:
        #print("BELIEF UPDATE! From good to even better")
        #print(f"Case {sim_number} with values\
        #        \n\t Previous {prev_val} \n\t Updated {updated_val}")
        return True
