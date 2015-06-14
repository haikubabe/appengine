months = ['January',
	  'February',
	  'March',
	  'April',
	  'May',
	  'June',
	  'July',
	  'August',
	  'September',
	  'October',
	  'November',
	  'December']

months_abbvs=dict((m[:3].lower(),m) for m in months)
print months_abbvs

def valid_month(month):

	if month:
		short_month=month[:3].lower()
		return months_abbvs.get(short_month)

#print valid_month("jpoijanuary")

