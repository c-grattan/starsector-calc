from array import array
import csv
from webbrowser import get

def getData(file):
	with open(file, newline='\n') as csvfile:
		reader = csv.DictReader(csvfile)
		return [row for row in reader]

ship_data = getData("ship_data.csv")
weapon_data = getData("weapon_data.csv")
wing_data = getData("wing_data.csv")