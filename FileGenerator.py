import os
import pickle
from Network import Network

os.chdir("./data")

def generate():
    """Generates a random network and stores it in a file"""
    a = raw_input("Set network arguments or use defaults?(s/d)\n")
    if a == 's':
        Pt = input("Input desired transmitting power:\n")
        alfa = input("Input desired ambient coefficient:\n")
        beta = input("Input desired SNR treshold:\n")
        T = input("Input desired temperature(in Kelvin):\n")
        B = input("Input desired band width:\n")
        L = input("Input desired square side length:\n")
        n = input("Input desired number of nodes:\n")
        FD = input("Generate a full-duplex network?(True/False)\n")
        with open('rand_network'+str(dir_size)+'.pk1','wb') as output:
            net = Network(Pt,alfa,beta,T,B,L,n,FD)
            pickle.dump(net,output,pickle.HIGHEST_PROTOCOL)
    if a == 'd':
        with open('rand_network'+str(dir_size)+'.pk1','wb') as output:
            net = Network()
            pickle.dump(net,output,pickle.HIGHEST_PROTOCOL)
    del net
    print("You have created the file: rand_network"+str(dir_size)+"\n")

    
while True:
    dir_size = 0
    for f in os.listdir('.'):
        dir_size += 1
    s = raw_input("Generate a new network, access existing one or quit the generator?(g/a/q)\n")
    if s == 'g':
        generate()
    if s == 'a':
        if dir_size == 0:
            print("There are no networks to be accessed.\n")
        else:
            i = input("Wich file do you want to access?(0 to "+str(dir_size-1)+")\n")
            with open('rand_network'+str(i)+'.pk1','rb') as input:
                net = pickle.load(input)
            print("You have loaded the network rand_network"+str(i)+" as 'net'")
            sch = raw_input("Schedule the links of the network?(y/n)\n")
            if sch == 'y':
                slots, T = net.GreedyPhysical()
                print("Scheduled links are in the dictionary 'slots' of length 'T'\n")
            if sch == 'n':
                print("Links not scheduled.\n")
            break
    if s == 'q':
        break

os.chdir("..")