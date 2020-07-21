import python_nbt.nbt as nbt
import glob
import requests
from requests.exceptions import HTTPError
import os

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
    if count > 100 | (x == len(files) - 1 & count > 0):
        #send post request to mojang api
        try:
            response = requests.post("https://api.mojang.com/profiles/minecraft", data=names)
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            print('Success! Get Reply from mojang api')
        #merge response and list of files
        for id in response.json:
            #find index of dictionary with matching name
            index = next((index for (index, d) in enumerate(files) if d["name"] == response.json["name"]), None)
            #add new filepath to dictionary:
            files[index]["newfilename"] = files[index]["newfilename"][:files[index]["newfilename"].rfind(os.sep)] + response.json["id"] + ".dat"
        #reset count and names
        count = 0
        names = []

print(files)