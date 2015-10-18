import csv
with open('hours.csv', 'r') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='"')
	print("[")
	for row in reader:
		print('{{"contributor": "JohnLockwood", "date": "{0}", "hours": {1}, "description": "{2}"}},'.format(row[0], row[1], row[2]))
		#print  ("\n".join(row) + "\n")
		#print (type(row))
	print("]")