
class RK4Integrator(object):

	def __init__(self,data=None):
		self.N0=1500.
		self.dt=0.1
		self.thr=0.05
		self.qd=100.
		self.I0=0.000001
		self.t0=self.N0

	def integrate(self):
		S = 1.0 - self.I0
		I = self.I0
		R = 0.
		DT = self.dt
		sus = []
		inf = []
		rec = []
		time = []
		#Implementation of RK4:
		for t in range(int(self.N0)):
			time.append(t)
			t+=1
			sus.append(S)
			inf.append(I)
			rec.append(R)
			k_1_S = self.dSdt(t,S,I,R)
			k_1_I = self.dIdt(t,S,I,R)
			k_1_R = self.dRdt(t,S,I,R)
			k_2_S = self.dSdt(t + 0.5 * DT,S + 0.5 * DT * k_1_S, I + 0.5 * DT * k_1_I, R + 0.5 * DT * k_1_R)
			k_2_I = self.dIdt(t + 0.5 * DT,S + 0.5 * DT * k_1_S, I + 0.5 * DT * k_1_I, R + 0.5 * DT * k_1_R)
			k_2_R = self.dRdt(t + 0.5 * DT,S + 0.5 * DT * k_1_S, I + 0.5 * DT * k_1_I, R + 0.5 * DT * k_1_R)
			k_3_S = self.dSdt(t + 0.5 * DT,S + 0.5 * DT * k_2_S, I + 0.5 * DT * k_2_I, R + 0.5 * DT * k_2_R)
			k_3_I = self.dIdt(t + 0.5 * DT,S + 0.5 * DT * k_2_S, I + 0.5 * DT * k_2_I, R + 0.5 * DT * k_2_R)
			k_3_R = self.dRdt(t + 0.5 * DT,S + 0.5 * DT * k_2_S, I + 0.5 * DT * k_2_I, R + 0.5 * DT * k_2_R)
			k_4_S = self.dSdt(t + DT,S + DT * k_3_S, I + DT * k_3_I, R + DT * k_3_R)
			k_4_I = self.dIdt(t + DT,S + DT * k_3_S, I + DT * k_3_I, R + DT * k_3_R)
			k_4_R = self.dRdt(t + DT,S + DT * k_3_S, I + DT * k_3_I, R + DT * k_3_R)
			#update N
			S = S + DT * 1.0/6.0 * (k_1_S + 2 * k_2_S + 2 * k_3_S + 2 * k_4_S)
			I = I + DT * 1.0/6.0 * (k_1_I + 2 * k_2_I + 2 * k_3_I + 2 * k_4_I)
			R = R + DT * 1.0/6.0 * (k_1_R + 2 * k_2_R + 2 * k_3_R + 2 * k_4_R)	
		sus.append(S)
		inf.append(I)
		rec.append(R)
		time.append(t)
		self.sus=sus
		self.inf=inf
		self.rec=rec
		self.time=time

	def dSdt(self,t,S,I,R):
		return self.growth_rate(t,S,I,R) * S * I *(-1.0)

	def dIdt(self,t,S,I,R):
		return self.growth_rate(t,S,I,R)  * S * I - self.recovery_rate(t,S,I,R)  * I

	def dRdt(self,t,S,I,R):
		return self.recovery_rate(t,S,I,R)  * I 
		
	def growth_rate(self,t,S,I,R):
		c = 3.0/10.0 #the numer of people infected by one individual per day (3 in ten days)
		if(I>self.thr):
			c = 1.0/10
			if(t<self.t0):
				self.t0 = t
		if(t>self.t0 + self.qd):
			c = 3.0/10.0
		return c

	def recovery_rate(self,t,S,I,R):
		return 1.0/10.0   #if the infection lasts ten days