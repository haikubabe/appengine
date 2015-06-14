def valid_day(day):
	if day and day.isdigit():
		day=int(day)
		if day in range(1,32):
			return day

#print valid_day('23')
