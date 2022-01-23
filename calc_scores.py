from calc_stats import getData
import sys
from pathlib import Path
import json

#Load stats

#Calculate scores
def getHullData(hullsFolder):
	hulls_folder = Path(hullsFolder)
	return [json.load(open(shipFile)) for shipFile in hulls_folder.glob("*.ship")]

def removeHiddenMounts(slots):
	return [slot for slot in slots if slot['mount'] != 'HIDDEN']

ship_data = getData(sys.argv[1] + "\\starsector-core\\data\\hulls\\ship_data.csv")
hull_data = getHullData(sys.argv[1] + "\\starsector-core\\data\\hulls")