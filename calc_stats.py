import csv

def getData(file):
	with open(file, newline='\n') as csvfile:
		reader = csv.DictReader(csvfile)
		return [row for row in reader]

#Get average weapon OP costs and flux/s
weapon_data = getData("weapon_data.csv")

#Get average fighter costs
wing_data = getData(sys.argv[1] + "\\starsector-core\\data\\hulls\\wing_data.csv")

#Get hull mod costs