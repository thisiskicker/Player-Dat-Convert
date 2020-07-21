import python_nbt.nbt as nbt
import glob

files = []
count = 0

#loop through all the player dat files in the world folder
for file in glob.glob('world/playerdata/*.dat'):
    #add add a dictionary with filepath to dat file to dictionary list
    files.append({"filename": file})

#loop through the list of file paths to player dat files
for x in files:
    #read in player dat file and get their 'lastKnownName'
    playerName = nbt.read_from_nbt_file(x["filename"]).value['bukkit'].value['lastKnownName'].value
    #add name to dictionary
    x["name"] = playerName
    #increment count
    count += 1
    #check if increment is over 100
    if count > 100:
        count = 0

print(files)