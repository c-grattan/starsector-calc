import csv
from operator import contains
import sys
from pathlib import Path
import json

#Load stats
with open("data/weapon_data.json") as wepData:
	weapon_data = json.load(wepData)

with open("data/fighter_data.json") as fightData:
	fighter_data = json.load(fightData)

#Calculate scores
def getHullData(hullsFolder):
	hulls_folder = Path(hullsFolder)
	return [json.load(open(shipFile)) for shipFile in hulls_folder.glob("*.ship")]

#ship_data = getData(sys.argv[1] + "\\starsector-core\\data\\hulls\\ship_data.csv")
#hull_data = getHullData(sys.argv[1] + "\\starsector-core\\data\\hulls")

def calcScore(ship, hullmod_data):
	score = int(ship['ordnance points'] or 0)
	netflux = -int(ship['flux dissipation'] or 0)
	id = ship['id']

	try:
		with open(sys.argv[1] + "\\starsector-core\\data\\hulls\\" + id + ".ship") as shipFile:

			#Weapon points
			hull = json.load(shipFile)
			shipSize = hull['hullSize']
			if shipSize == "FRIGATE":
				shipSize = 0
			elif shipSize == "DESTROYER":
				shipSize = 1
			elif shipSize == "CRUISER":
				shipSize = 2
			elif shipSize == "CAPITAL_SHIP":
				shipSize = 3

			if 'weaponSlots' in hull:
				for slot in hull['weaponSlots']:
					mount = slot['mount']
					type = slot['type']
					if mount != 'HIDDEN' and type != 'SYSTEM':
						if type == 'BUILT_IN':
							id += '*' #Built-in weapon found
						elif type in ["BALLISTIC", "ENERGY", "MISSILE", "COMPOSITE", "SYNERGY", "HYBRID", "UNIVERSAL"]:
							size = slot['size']
							op = 0
							fluxsec = 0
							if type == "COMPOSITE":
								#Ballistic, missile
								fluxsec = weapon_data["BALLISTIC"][size]['fluxsec'] + weapon_data["MISSILE"][size]['fluxsec'] / 2
								op = weapon_data["BALLISTIC"][size]['op'] + weapon_data["MISSILE"][size]['op'] / 2
							elif type == "SYNERGY":
								#Energy, missile
								fluxsec = weapon_data["ENERGY"][size]['fluxsec'] + weapon_data["MISSILE"][size]['fluxsec'] / 2
								op = weapon_data["ENERGY"][size]['op'] + weapon_data["MISSILE"][size]['op'] / 2
							elif type == "HYBRID":
								#Ballistic, energy
								fluxsec = weapon_data["ENERGY"][size]['fluxsec'] + weapon_data["BALLISTIC"][size]['fluxsec'] / 2
								op = weapon_data["ENERGY"][size]['op'] + weapon_data["BALLISTIC"][size]['op'] / 2
							elif type == "UNIVERSAL":
								#All types
								fluxsec = weapon_data["ENERGY"][size]['fluxsec'] + weapon_data["BALLISTIC"][size]['fluxsec'] + weapon_data["MISSILE"][size]['fluxsec'] / 3
								op = weapon_data["ENERGY"][size]['op'] + weapon_data["BALLISTIC"][size]['op'] + + weapon_data["MISSILE"][size]['op']/ 3
							else:
								fluxsec = weapon_data[type][size]['fluxsec']
								op = weapon_data[type][size]['op']
							netflux += fluxsec
							score -= op
			
			#Hull mods
			if shipSize != "FIGHTER" and 'builtInMods' in hull:
				for mod in hull['builtInMods']:
					mod_data = [m for m in hullmod_data if m[0] == mod]
					if len(mod_data) != 0:
						score += mod_data[0][1][shipSize]
		
		#Vent points
		if netflux > 0:
			score -= netflux / 10 #Vent OPs	
		
		#Fighter bays
		score -= int(ship['fighter bays'] or 0) * fighter_data['op']

	except FileNotFoundError:
		print("Ship file not found:", id)
		id += "(File not found)"
		score = 0

	return id, score

def getHullmodData(file):
	with open(file) as hullfile: #Hullmod data
		hullreader = csv.DictReader(hullfile)
		retArray = []
		for row in hullreader:
			id = row['id']
			if id != '' and row['hidden'] != 'TRUE':
				retArray.append([id, [int(row['cost_frigate'] or 0), int(row['cost_dest'] or 0), int(row['cost_cruiser'] or 0), int(row['cost_capital'] or 0)]])
		return retArray

hullmod_data = getHullmodData(sys.argv[1] + "\\starsector-core\\data\\hullmods\\hull_mods.csv")
#print(hullmod_data)

scores = []

with open(sys.argv[1] + "\\starsector-core\\data\\hulls\\ship_data.csv") as csvfile: #Ship data
	reader = csv.DictReader(csvfile)
	for row in reader:
		if row['id'] != '':
			ship_name, ship_score = calcScore(row, hullmod_data)
			scores.append([ship_name, ship_score])

with open("scores.csv", "w", newline='') as csvfile:
	csvwriter = csv.writer(csvfile)
	for ship in scores:
		csvwriter.writerow(ship)

'''
Calculation order:
Add hull OP points - Done
Subtract average OP point cost for weapon mounts and fighter bays - Done
Subtract average vents needed - Done
Add built-in hullmods bonus - Done
Account for unique built-ins - Done
'''