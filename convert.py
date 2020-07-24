import python_nbt.nbt as nbt
import glob
import requests
from requests.exceptions import HTTPError
import os
import json

files = []
names = []
count = 0

#loop through all the player dat files in the world folder
for file in glob.glob('world/playerdata/*.dat'):
    #add add a dictionary with filepath to dat file to dictionary list
    files.append({"filename": file})

#loop through the list of file paths to player dat files
for x in range(len(files)):
    #read in player dat file and get their 'lastKnownName'
    playerName = nbt.read_from_nbt_file(files[x]["filename"]).value['bukkit'].value['lastKnownName'].value
    #add name to dictionary and names list
    files[x]["name"] = playerName
    names.append(playerName)
    #increment count
    count += 1
    #run if count is over 100 or if at last loop and count is over 0
    if count >= 10 or (x == len(files) - 1 and count > 0):
        #send post request to mojang api
        try:
            response = requests.post("https://api.mojang.com/profiles/minecraft", data=json.dumps(names))
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            print("got response for " + str(count) + " players")
        #merge response and list of files
        #print(response.json())
        for id in response.json():
            #print(id["name"])
            #find index of dictionary with existing name key and matching name
            index = next((index for (index, d) in enumerate(files) if "name" in d and d["name"] == id["name"]), -1)
            #check if index was found
            if index > 0:
                filename = id["id"][:7] + "-" + id["id"][8:11] + "-" + id["id"][12:15] + "-" + id["id"][16:19] + "-" + id["id"][20:] + ".dat"
                #add new filepath to dictionary:
                files[index]["newfilename"] = files[index]["filename"][:files[index]["filename"].rfind(os.sep)+1] + filename
        #reset count and names
        count = 0
        names = []

countDat = 0
#loop through the files list
for f in files:
    #check if the files is to be renamed
    if "newfilename" in f:
        #rename the file
        os.rename(f["filename"],f["newfilename"])
        countDat += 1

print("updated " + str(countDat) + " files.")