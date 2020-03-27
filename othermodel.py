#S: percentage of susceptable individuals
#I: percentage of infected individuals
#R: percentage of recovered individuals

#DE for S: dSdt =  - growth_rate * S * I  + loss_of_immunity * R   //Leaving the susceptible group via infection, and getting added via deimmunization
#DE for R: dRdt =    recovery_rate * I                         //The recovery rate is the inverse of the infection duration
#DE for I: dIdt = -  dSdt - dRdt = growth_rate * S * I - recovery_rate * I // since the sum of R + I + S const, therefore dRdt + dSdt + dIdt = 0


def dSdt(t,S,I,R):
	return growth_rate(t,S,I,R) * S * I *(-1.0)

def dIdt(t,S,I,R):
	return growth_rate(t,S,I,R)  * S * I - recovery_rate(t,S,I,R)  * I 

def dRdt(t,S,I,R):
	return recovery_rate(t,S,I,R)  * I 	
	
def growth_rate(t,S,I,R):
	c = 3.0/10.0 #the numer of people infected by one individual per day (3 in ten days)
	if(I>0.002):
		c=1.0/20.0
	if(I>0.008):
		c=3.0/10.0
	return c

def recovery_rate(t,S,I,R):
	return 1.0/10.0   #if the infection lasts ten days


	
NT = 1000 #days
DT = 0.1

#set initial values:
I = 0.1
S = 1.0 - I
R = 0
sus = []
inf = []
rec = []
time = []

#Implementation of RK4:
for t in range(NT):
	time.append(t)
	t = t+1
	#calculate new susceptables
	sus.append(S)
	inf.append(I)
	rec.append(R)
	k_1_S = dSdt(t,S,I,R)
	k_1_I = dIdt(t,S,I,R)
	k_1_R = dRdt(t,S,I,R)
	
	k_2_S = dSdt(t + 0.5 * DT,S + 0.5 * DT * k_1_S, I + 0.5 * DT * k_1_I, R + 0.5 * DT * k_1_R)
	k_2_I = dIdt(t + 0.5 * DT,S + 0.5 * DT * k_1_S, I + 0.5 * DT * k_1_I, R + 0.5 * DT * k_1_R)
	k_2_R = dRdt(t + 0.5 * DT,S + 0.5 * DT * k_1_S, I + 0.5 * DT * k_1_I, R + 0.5 * DT * k_1_R)
	
	k_3_S = dSdt(t + 0.5 * DT,S + 0.5 * DT * k_2_S, I + 0.5 * DT * k_2_I, R + 0.5 * DT * k_2_R)
	k_3_I = dIdt(t + 0.5 * DT,S + 0.5 * DT * k_2_S, I + 0.5 * DT * k_2_I, R + 0.5 * DT * k_2_R)
	k_3_R = dRdt(t + 0.5 * DT,S + 0.5 * DT * k_2_S, I + 0.5 * DT * k_2_I, R + 0.5 * DT * k_2_R)
	

	k_4_S = dSdt(t + DT,S + DT * k_3_S, I + DT * k_3_I, R + DT * k_3_R)
	k_4_I = dIdt(t + DT,S + DT * k_3_S, I + DT * k_3_I, R + DT * k_3_R)
	k_4_R = dRdt(t + DT,S + DT * k_3_S, I + DT * k_3_I, R + DT * k_3_R)
	#update N
	S = S + DT * 1.0/6.0 * (k_1_S + 2 * k_2_S + 2 * k_3_S + 2 * k_4_S)
	I = I + DT * 1.0/6.0 * (k_1_I + 2 * k_2_I + 2 * k_3_I + 2 * k_4_I)
	R = R + DT * 1.0/6.0 * (k_1_R + 2 * k_2_R + 2 * k_3_R + 2 * k_4_R)
	
sus.append(S)
inf.append(I)
rec.append(R)
time.append(t)	

#print(time)
#print(result)

import matplotlib.pyplot as plt
from matplotlib import ticker, cm

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(time, sus, label =  "susceptable")
ax.plot(time, inf, label =  "infected")
ax.plot(time, rec, label =  "recovered")
ax.legend()

plt.show()

