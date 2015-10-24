import csv
with open('hours.csv', 'r') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='"')
	total = 0.0
	print("[")
	for row in reader:
		print('{{"contributor": "JohnLockwood", "date": "{0}", "hours": {1}, "description": "{2}"}},'.format(row[0], row[1], row[2]))
		total = total + float(row[1])
		#print  ("\n".join(row) + "\n")
		#print (type(row))
	print("]")
	print("-------------------------------------------")
	print("Total hours:  {0}".format(total))