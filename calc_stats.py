from asyncore import read
import csv
import json
from pprint import pformat
import sys

pFile = open("params.json")
params = json.load(pFile)
pFile.close()

weapon_data = {
	'BALLISTIC': {
		'SMALL': {
			'fluxsec': 0,
			'op': 0,
			'count': 0
		},
		'MEDIUM': {
			'fluxsec': 0,
			'op': 0,
			'count': 0
		},
		'LARGE': {
			'fluxsec': 0,
			'op': 0,
			'count': 0
		}
	},

	'ENERGY': {
		'SMALL': {
			'fluxsec': 0,
			'op': 0,
			'count': 0
		},
		'MEDIUM': {
			'fluxsec': 0,
			'op': 0,
			'count': 0
		},
		'LARGE': {
			'fluxsec': 0,
			'op': 0,
			'count': 0
		}
	},

	'MISSILE': {
		'SMALL': {
			'fluxsec': 0,
			'op': 0,
			'count': 0
		},
		'MEDIUM': {
			'fluxsec': 0,
			'op': 0,
			'count': 0
		},
		'LARGE': {
			'fluxsec': 0,
			'op': 0,
			'count': 0
		}
	}
}

def getWeaponData(file):
	with open(file, newline='\n') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			if row['id'] and row['hints'] != 'SYSTEM': #Skip fighter-exclusive and built-in weapons
				weaponFile = sys.argv[1] + "\\starsector-core\\data\\weapons\\" + row['id'] + ".wpn"
				if not params['omega'] and ' omega' in row['tags'].split(','):
					break
				with open(weaponFile) as weapon:
					#Get weapon type/mount size
					size = ''
					type = ''
					for line in weapon:
						field = line[2:6]
						if field == "size":
							size = line[9:-3]
						elif field == "type":
							type = line[9:-3]
					
					if size != '' and type != '': #Valid weapon
						#Calculate flux per second
						energy_shot = float(row['energy/shot'] or 0)
						chargeup = float(row['chargeup'] or 0)
						chargedown = float(row['chargedown'] or 0)
						firing_delay = chargeup + chargedown

						#Update flux/second data
						if firing_delay == 0:
							weapon_data[type][size]['fluxsec'] += energy_shot
						else:
							weapon_data[type][size]['fluxsec'] += energy_shot / firing_delay
						
						#Update weapon data
						weapon_data[type][size]['op'] += int(row['OPs'] or 0)
						weapon_data[type][size]['count'] += 1

	#Calculate averages
	for type in ["BALLISTIC", "ENERGY", "MISSILE"]:
		for size in ["SMALL", "MEDIUM", "LARGE"]:
			count = weapon_data[type][size]['count']
			weapon_data[type][size]['fluxsec'] /= count
			weapon_data[type][size]['op'] /= count

#Get average fighter costs
#wing_data = getData(sys.argv[1] + "\\starsector-core\\data\\hulls\\wing_data.csv")

#Get hull mod costs

getWeaponData(sys.argv[1] + "\\starsector-core\\data\\weapons\\weapon_data.csv")
print(weapon_data)