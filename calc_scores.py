import csv
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
			if 'builtInMods' in hull:
				for mod in hull['builtInMods']:
					pass
		
		#Vent points
		if netflux > 0:
			score -= netflux / 10 #Vent OPs	
		
		#Fighter bays
		score -= int(ship['fighter bays'] or 0) * fighter_data['op']

	except FileNotFoundError:
		print("Ship file not found:", id)

	return id, score

def getHullmodData(file):
	with open(file) as hullfile: #Hullmod data
		hullreader = csv.DictReader(hullfile)
		return [row for row in hullreader if row['hidden'] != 'TRUE']

hullmod_data = getHullmodData(sys.argv[1] + "\\starsector-core\\data\\hullmods\\hull_mods.csv")
print(hullmod_data)

with open(sys.argv[1] + "\\starsector-core\\data\\hulls\\ship_data.csv") as csvfile: #Ship data
	reader = csv.DictReader(csvfile)
	for row in reader:
		if row['id'] != '':
			ship_name, ship_score = calcScore(row, hullmod_data)
			#print(ship_name, ':', ship_score)

'''
Calculation order:
Add hull OP points
Subtract average OP point cost for weapon mounts and fighter bays
Subtract average vents needed
Add built-in hullmods bonus
Account for unique built-ins
'''