#Small parser for the COVID-19 data provided by the JHU: https://github.com/CSSEGISandData/COVID-19

#Please make sure your local COVID-19 data repository is cloned to the same parent directory in which this repo is located. 

path='./../COVID-19/csse_covid_19_data/csse_covid_19_time_series/'
fname='time_series_covid19_*_global.csv'

def parse(which='confirmed'):
	f=path+fname.replace('*',which)
	data={}
	try:
		fl=open(f,'r')
		header=True
		for line in fl:
			d=line.split(',')
			d[-1]=d[-1].strip('\n')
			if header:
				data['dates']=d[4:]
				header=False
			else:
				province=d[0]
				region=d[1]
				lat=d[2]
				lon=d[3]
				N_t=d[4:]
				if region in data.keys():
					data[region]+=N_t
				else:
					data[region]=N_t
		fl.close()
		return data
	except Exception as e:
		print 'Failed to load data!'
		import traceback
		traceback.print_exc()

