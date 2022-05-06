import json
import os
from os.path import join as osjoin
print('This script will remove the json object of the provided label as well as echo back any potential placeholders discovered.\n')
whatdir = input('Enter the full folder path containing ONLY your json files:')
removethis = input('Enter the label name of the object you want to remove:')
whatdir = osjoin(whatdir, '')
dirs = os.listdir(whatdir)
for file in dirs:
    jsondata = open(whatdir + file, 'r').read().strip()
    jsondata = json.loads(jsondata)
    alterjson = dict(jsondata)
    for topkey in jsondata['721']['POLICY_ID'].keys():
        for check in jsondata['721']['POLICY_ID'][topkey]:
            if '<' in check:
                print('Discovered possible placeholder: ', check)
        for key in [key for key in jsondata['721']['POLICY_ID'][topkey] if key == removethis]: del jsondata['721']['POLICY_ID'][topkey][key]
    with open(whatdir + file, 'w') as jsonout:
        jsonout.write(json.dumps(alterjson, indent=4))
print('Complete! Check files to verify.')
