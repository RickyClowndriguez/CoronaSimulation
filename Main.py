

def load_model(pars=None):
	if pars==None:
		pars=[None for i in range(5)]
	N0,dt,thr,qd,I0=pars
	from Model import RK4Integrator
	m=RK4Integrator()
	if N0!=None:
		m.N0=N0
	if dt!=None:
		m.dt=dt
	if thr!=None:
		m.thr=thr
	if qd!=None:
		m.qd=qd
	if I0!=None:
		m.I0=I0
	m.integrate()
	return m

def load_data(which=None,countries=None,daterange=None):
	from CoronaParser import parse
	from numpy import logical_and
	d=parse(which)
	if countries==None:
		countries=d.keys()
		countries.remove('dates')
	max_date=d['dates'][-1]
	min_date=d['dates'][0]
	if daterange==None:
		daterange=(min_date,max_date)
	datemask=logical_and(d['dates']>=min_date,d['dates']<=max_date)
	data={}
	data['dates']=d['dates'][datemask]
	for country in countries:
		if country not in d.keys():
			print('No data for country \"{}\"'.format(country))
			raise Exception()
		else:
			data[country]=d[country][datemask]
	return data

def plot_data(data,fig=None,which=None,fname=None):
	import matplotlib.pyplot as plt
	if which==None:
		which='Germany'
	if not fig:
		fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.set_xlabel('Days')
	ax.set_ylabel('N(d)')
	ax.plot(data[which])
	ax.legend([which])
	if fname:
		fig.savefig(fname)
	else:
		plt.show()
	return fig

def plot_model(model,fig=None,fname=None):
	import matplotlib.pyplot as plt
	if not fig:
		fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.plot(model.time, model.sus, label =  "susceptable")
	ax.plot(model.time, model.inf, label =  "infected")
	ax.plot(model.time, model.rec, label =  "recovered")
	ax.axvspan(model.t0, model.t0+model.qd, alpha=0.5, color='green')
	ax.set_xlabel("time in days")
	ax.set_ylabel("ratio of total population")
	ax.legend()
	if fname:
		fig.savefig(fname)
	else:
		plt.show()
	return fig


if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('--defaults',
						dest = 'defaults',
						action = 'store_true',
						help = 'Run the script with default settings.')
	args=parser.parse_args()

	d=load_data()
	m=load_model()
	fig=plot_data(d,fname='dataplot.pdf')
	fig=plot_model(m,fname='modelplot.pdf')
	#print d