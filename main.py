#!/usr/bin/env python

from models import (create_bn_example1,
                    create_bn_example2, 
                    create_bn_example4, 
                    create_bn_example1_simulation,
                    create_bn_example2_simulation,
                    create_bn_example4_simulation)
from numpy.random import beta



print("Running example 1 -The Promotion-:")
create_bn_example1("Alice", 0.99, 0.6)
create_bn_example1("Bob", 0.1, 0.4)
 

print("Running example 2 -Religious Belief-:")
create_bn_example2("Alice", 0.9)
create_bn_example2("Bob", 0.1)


print("Running example 4 -Political Belief-:")
create_bn_example4("Alice", 0.9, 0.5)
create_bn_example4("Bob", 0.1, 0.5)

#---------------------------SIMULATIONS-------------------------------------------------

def simulate_network_1():
    print("\n")
    print('*'*30)
    print("\n")
    print("Running simulation on Bayes Net 1 -The Promotion-")
    def simulate_biased(n=100):
        updates = 0
        for i in range(0,n):
            #print(f"Simulation {i}")
            #print("Generating biased priors...")
            reputable_prob  = beta(0.1,0.1)
            calif_prob = beta(0.1,0.1)
            #print(f"Values: \n\tLiberal {liberal}\n\t Spend {spend}")
            is_updated = create_bn_example1_simulation("Alice", reputable_prob, calif_prob, i)
            if is_updated:
                updates+=1
        #print(f"\n\n\t\t\tUsing {n} biased simulations obtained belief updates in {updates} cases")
        return n, updates


    def simulate_uniform(n=100):
        updates = 0
        for i in range(0,n):
            #print(f"Simulation {i}")
            #print("Generating biased priors...")
            reputable_prob = beta(1,1)
            calif_prob = beta(1,1)
            #print(f"Values: \n\tLiberal {liberal}\n\t Spend {spend}")
            is_updated = create_bn_example1_simulation("Alice", reputable_prob, calif_prob, i)
            if is_updated:
                updates+=1
        #print(f"\n\n\t\t\tUsing {n} uniform simulations obtained belief updates in {updates} cases")
        return n, updates



    n_bias, update_bias = simulate_biased(1000)

    n_uniform, update_uniform = simulate_uniform(1000)
    print("Bias conclusion:")
    print(f"\n\n\t\t\tUsing {n_bias} biased simulations obtained belief updates in {update_bias} cases")
    print(f"\t\t {(update_bias/n_bias)*100}% on contrary updated belief")

    print("Uniform conclusion:")
    print(f"\n\n\t\t\tUsing {n_uniform} uniform simulations obtained belief updates in {update_uniform} cases")
    print(f"\t\t {(update_uniform/n_uniform)*100}% on contrary updated belief")
    print("Done")


def simulate_network_2():
    print("\n")
    print('*'*30)
    print("\n")
    print("Running simulation on Bayes Net 2 -Religious Belief-")
    def simulate_biased(n=100):
        updates = 0
        for i in range(0,n):
            #print(f"Simulation {i}")
            #print("Generating biased priors...")
            christian_prob = beta(0.1,0.1)
            #print(f"Values: \n\tLiberal {liberal}\n\t Spend {spend}")
            is_updated = create_bn_example2_simulation("Alice", christian_prob, i)
            if is_updated:
                updates+=1
        #print(f"\n\n\t\t\tUsing {n} biased simulations obtained belief updates in {updates} cases")
        return n, updates


    def simulate_uniform(n=100):
        updates = 0
        for i in range(0,n):
            #print(f"Simulation {i}")
            #print("Generating biased priors...")
            christian_prob = beta(1,1)
            #print(f"Values: \n\tLiberal {liberal}\n\t Spend {spend}")
            is_updated = create_bn_example2_simulation("Alice", christian_prob, i)
            if is_updated:
                updates+=1
        #print(f"\n\n\t\t\tUsing {n} uniform simulations obtained belief updates in {updates} cases")
        return n, updates



    n_bias, update_bias = simulate_biased(1000)

    n_uniform, update_uniform = simulate_uniform(1000)
    print("Bias conclusion:")
    print(f"\n\n\t\t\tUsing {n_bias} biased simulations obtained belief updates in {update_bias} cases")
    print(f"\t\t {(update_bias/n_bias)*100}% on contrary updated belief")

    print("Uniform conclusion:")
    print(f"\n\n\t\t\tUsing {n_uniform} uniform simulations obtained belief updates in {update_uniform} cases")
    print(f"\t\t {(update_uniform/n_uniform)*100}% on contrary updated belief")
    print("Done")


def simulate_network_4():
    print("\n")
    print('*'*30)
    print("\n")
    print("Running simulation on Bayes Net 4 -Political Belief- (Not included in paper)")
    def simulate_biased(n=100):
        updates = 0
        for i in range(0,n):
            #print(f"Simulation {i}")
            #print("Generating biased priors...")
            liberal = beta(0.1,0.1)
            spend = beta(0.1,0.1)
            #print(f"Values: \n\tLiberal {liberal}\n\t Spend {spend}")
            is_updated = create_bn_example4_simulation("Alice", liberal, spend, i)
            if is_updated:
                updates+=1
        #print(f"\n\n\t\t\tUsing {n} biased simulations obtained belief updates in {updates} cases")
        return n, updates


    def simulate_uniform(n=100):
        updates = 0
        for i in range(0,n):
            #print(f"Simulation {i}")
            #print("Generating biased priors...")
            liberal = beta(1,1)
            spend = beta(1,1)
            #print(f"Values: \n\tLiberal {liberal}\n\t Spend {spend}")
            is_updated = create_bn_example4_simulation("Alice", liberal, spend, i)
            if is_updated:
                updates+=1
        #print(f"\n\n\t\t\tUsing {n} uniform simulations obtained belief updates in {updates} cases")
        return n, updates



    n_bias, update_bias = simulate_biased(1000)

    n_uniform, update_uniform = simulate_uniform(1000)
    print("Bias conclusion:")
    print(f"\n\n\t\t\tUsing {n_bias} biased simulations obtained belief updates in {update_bias} cases")
    print(f"\t\t {(update_bias/n_bias)*100}% on contrary updated belief")

    print("uniform conclusion:")
    print(f"\n\n\t\t\tUsing {n_uniform} uniform simulations obtained belief updates in {update_uniform} cases")
    print(f"\t\t {(update_uniform/n_uniform)*100}% on contrary updated belief")
    print("Done")

simulate_network_1()
simulate_network_2()
simulate_network_4()
