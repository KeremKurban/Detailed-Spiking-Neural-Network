from pylab import *
import numpy as np
from random import *
import random
import pylab
from matplotlib.pyplot import pause
import networkx as nx
pylab.ion()

#************************************************************************
tmax = 1000
dt = 0.5
T = ceil(tmax/dt)
T = int(T)
tr = array([200,700])/dt
glob_t = 0

Neurons = [] #list of actual neurons
Neurons_attr = []
adj_list = [] #list of adjacency of neurons
Network = nx.Graph()
color_map = []

#************************************************************************
class Neuron:
    #attributes
    l_in = 0
    l_out = 0
    v_id = np.zeros(T)
    u_id = np.zeros(T)

    #start
    def __init__(self):
        self.l_in = 0
    
    #initializing
    def init_neuron(self, n_id, tresh, v0, u0, a,b,c,d, neighbor_neurons):
        self.n_id = n_id
        self.tresh = tresh
        self.neig_neurons = neighbor_neurons
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.c_t = 0
        self.v_id[0] = v0
        self.u_id[0] = u0

    '''
    def fire(self, current_in):
        if(current_in >= 1 ):
            color_map[self.n_id] = 'red'
            for i in self.neig_neurons:
                Neurons[i].fire(Network[Neurons[self.n_id]][Neurons[i]]['weight'] * current_in)
                visualize()
    '''

#************************************************************************
def randomized_neuron_generator():
    ans = np.zeros(7)
    f = 1
    if f == 1:
        ans[0] = int(random.random()*2+34) #tresh
        ans[1] =  -1*(int(random.random()*5+67.5)) #v0
        ans[2] =  -1*(int(random.random()*8+10)) #u0
        ans[3] = (random.random()*2+1)/100 
        ans[4] = (random.random()*2+1)/10
        ans[5] = -1*(int(random.random()*10+60))
        ans[6] = int(random.random()*10)
    else:
        ans[0] = 35 
        ans[1] =  -1*70
        ans[2] =  -1*14
        ans[3] = 0.02
        ans[4] = 0.2
        ans[5] = -1*65
        #print(ans[5])
        ans[6] = 10

    return(ans)

#************************************************************************
def self_loop_handler(num, ll):
    lll = []
    for i in ll:
        if num != i:
            lll.append(i)
    return(lll)

#************************************************************************
def processing(n1, firing_time):

    n1.c_t = firing_time
    v = n1.v_id
    u = n1.u_id
    a = n1.a
    b = n1.b
    c = n1.c
    d = n1.d
    
    t = glob_t
    for t in arange(T-1):
        if t < tr[1]:
            l = n1.l_in
        else:
            l = 0
        if v[t] < n1.tresh:
            dv = (0.04*v[t]+5)*v[t]+140-u[t]
            v[t+1] = v[t]+(dv+l)*dt
            du = a*(b*v[t]-u[t])
            u[t+1] = u[t] + dt*du
        else:
            v[t] = n1.c
            v[t+1] = c
            u[t+1] = u[t] + d

    #print(n1.n_id)
    
    figure()
    tvec = arange(n1.c_t, tmax+n1.c_t, dt)
    plot(tvec, v, 'b', label='Voltage trace of' + str(n1.n_id))
    xlabel('Time[ms]')
    ylabel('Membrane voltage [mV]')
    title('A single qIF neuron --  ' + str(n1.n_id))
    pause(3)
    

#************************************************************************
def graphizer():
    
    for i in Neurons:
        Network.add_node(i, Position=(random.randrange(0, 100), random.randrange(0, 100)))

    for i in Neurons:
        for j in i.neig_neurons:
            Network.add_edge(i, Neurons[j], weight = random.random()/2+0.5, color = 'cyan')
            #print(Network[i][Neurons[j]]['weight'])


#************************************************************************
def visualize():
    nx.draw(Network, node_color = color_map, pos = nx.get_node_attributes(Network, 'Position'))
    pause(1)

#************************************************************************
#
#   Events occur after this point :)
#
#************************************************************************
num_of_neurons = int(input("What is the number of neurons? "))
choice = input("do you want random generation of connections?")

if choice == 'y':
    for i in range(num_of_neurons):
        q_rand = randomized_neuron_generator()
        neighbors = random.sample(range(num_of_neurons), int(random.random()*num_of_neurons-1))
        neighbors = self_loop_handler(i, neighbors)
        adj_list.append(neighbors)
        new_neuron = Neuron()
        new_neuron.init_neuron(i, q_rand[0], q_rand[1], q_rand[2], q_rand[3], q_rand[4], q_rand[5], q_rand[6], neighbors)
        Neurons.append(new_neuron)
        Neurons_attr.append([0,0])
        color_map.append('blue')
else:
    for i in range(num_of_neurons):
        q_rand = randomized_neuron_generator()
        neighbors = [int(x) for x in input().split()]
        adj_list.append(neighbors)
        new_neuron = Neuron()
        new_neuron.init_neuron(i, q_rand[0], q_rand[1], q_rand[2], q_rand[3], q_rand[4], q_rand[5], q_rand[6], neighbors)
        Neurons.append(new_neuron)
        Neurons_attr.append([0,0])
        color_map.append('blue')

graphizer()

#iterator   **************************************************************
Neurons_attr[0][0] = 9

plt.figure(1,figsize = (10,12))
for i in range(0, 10):
    llll = []
    for j in range(0,len(Neurons_attr)):
        if Neurons_attr[j][0] >= 1:
            llll.append(j)
            color_map[j] = 'red'
            Neurons_attr[j][1] = Neurons_attr[j][1] + Neurons_attr[j][0]
            Neurons_attr[j][0] = 0
    
    visualize()

    for j in llll:
        color_map[j] = 'blue'

    for j in range(0,len(Neurons_attr)):
        if Neurons_attr[j][1] >= 1:
            for adj in adj_list[j]:
                Neurons_attr[adj][0] = Neurons_attr[adj][0] + Network[Neurons[j]][Neurons[adj]]['weight']*Neurons_attr[j][1]
            Neurons_attr[j][1] = 0


