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