

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

def load_pop(countries=None,daterange=None):
	from CoronaParser import parse_pop
	pop_timeseries=parse_pop()
	pop_2018={}
	for key in pop_timeseries.keys():
		pop_2018[key]=pop_timeseries[key][-1]
	return pop_2018

def load_data(which=None,countries=None,daterange=None):
	from CoronaParser import parse
	from numpy import logical_and
	d=parse(which)
	if countries==None:
		countries=list(d.keys())
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
	else:
		ax=fig.gca()
	ax.set_xlabel('Days')
	ax.set_ylabel('N(d)')
	ax.plot(data[which])
	ax.legend([which])
	if fname:
		fig.savefig(fname)
		print('Plot saved as {}'.format(fname))
	else:
		plt.show()
	return fig

def plot_model(model,fig=None,fname=None):
	import matplotlib.pyplot as plt
	if not fig:
		fig = plt.figure()
		ax = fig.add_subplot(111)
	else:
		ax=fig.gca()
	ax.plot(model.time, model.sus, label =  "susceptable")
	ax.plot(model.time, model.inf, label =  "infected")
	ax.plot(model.time, model.rec, label =  "recovered")
	ax.axvspan(model.t0, model.t0+model.qd, alpha=0.5, color='green')
	ax.set_xlabel("time in days")
	ax.set_ylabel("ratio of total population")
	ax.legend()
	if fname:
		fig.savefig(fname)
		print('Plot saved as {}'.format(fname))
	else:
		plt.show()
	return fig

'''
	Function to normalize the COVID-19 data to 1 by dividing by the total population number stored in the pop dictionary
'''
def normalize_data(data,pop,which=None):
	import numpy as np
	normed_data={}
	if which==None:
		try:
			for key in data.keys():
				normed_data[key]=np.array(data[key])/pop[key]
		except:
			print('Failed to normalize data!')
			import traceback
			traceback.print_exc()
	else:
		try:
			if type(which)==str:
				raise TypeError()
			for key in which:
				normed_data[key]=np.array(data[key])/pop[key]
		except TypeError:
			try:
				normed_data[which]=np.array(data[which]/pop[which])
			except Exception as e:
				print('Failed to normalize data!')
				import traceback
				traceback.print_exc()
		except KeyError: 
			print('Error: Key \"{}\" does not exist in the population dictionary.'.format(key))
	return normed_data

'''
	Function to determine a starting time stamp for the simulation which matches the real COVID-19 data
'''
def find_dayz(data,which=None,thr=None):
	if thr==None:
		thr=1.
	dayz_dict={}
	if which==None:
		#all
		which=[key for key in data.keys()]
	else:
		if type(which)==str:
			which=[which]
	try:
		for key in which:
			dayz=None
			i=0
			while i<len(data[key]-1) and dayz==None:
				if data[key][i]<thr:
					i+=1
				else:
					dayz=i
			if i==len(data[key]):
				print('Warning: Could not determine day zero. Total number of cases does not surpass the threshold \"{}\" for key \"{}\".'.format(thr,key))
			dayz_dict[key]=dayz
	except Exception as e:
		print('Failed to find day zero!')
		import traceback
		traceback.print_exc()
	else:
		return dayz_dict

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('--defaults',
						dest = 'defaults',
						action = 'store_true',
						help = 'Run the script with default settings.')
	args=parser.parse_args()

	if args.defaults:
		print('Loading COVID-19 data...')
		d=load_data()
		print('Done!')
		print('Initializing simulation model...')
		m=load_model()
		print('Done!')
		print('Loading population data for normalization...')
		p=load_pop()
		print('Done!')
		print('Normalizing data...')
		nd=normalize_data(d,p,which='Germany')
		print('Done.')
		print('Sample data set for Germany:')
		print(d['dates'],d['Germany'])
		print('Normalized data:')
		print(nd)
		print('Beginning of infection {} days after 21/1/20.')
		fig=plot_data(nd,fname='dataplot.pdf')
		fig=plot_model(m,fig=fig,fname='modelplot.pdf')