

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




if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('--defaults',
						dest = 'defaults',
						action = 'store_true',
						help = 'Run the script with default settings.')
	args=parser.parse_args()

	d=load_data()
	#print d