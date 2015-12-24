from json import loads
file_name = input("Enter a file name:  ")
with open(file_name, 'r') as f:
    read_data = f.read()
data = loads(read_data)
hours = [i["hours"] for i in data["hours"]] 
print("Total hours: ", round(sum(hours), 1))
