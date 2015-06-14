def valid_year(year):
	if year and year.isdigit():
		year=int(year)
		if 1900<=year<=2020:
			return year


