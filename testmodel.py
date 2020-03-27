#input 
NT = 1000
DT = 0.1
N_0 = 1000

#N(t) is th number of people who had or have the diesease
def dNdt(t,N):
	return growth_rate(t,N) * N * (1 - N/N_0)


def growth_rate(t,N):
	return 0.2
	

#set initial values:
N=10
t=0
result = []
time = []

#Implementation of RK4:
for t in range(NT):
	result.append(N)
	time.append(t)
	t = t+1
	k_1 = dNdt(t,N)
	k_2 = dNdt(t + 0.5 * DT, N + 0.5 * DT * k_1)
	k_3 = dNdt(t + 0.5 * DT, N + 0.5 * DT * k_2)
	k_4 = dNdt(t + DT, N + DT * k_3)
	#update N
	N = N + DT * 1.0/6.0 * (k_1 + 2 * k_2 + 2 * k_3 + 2 * k_4)
	
result.append(N)
time.append(t)	

#print(time)
#print(result)

import matplotlib.pyplot as plt
from matplotlib import ticker, cm

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(time, result, label =  "Number of infected or recovered")

plt.show()


