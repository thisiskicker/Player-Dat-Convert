import python_nbt.nbt as nbt
import glob

files = []
names = []
count = 0

for file in glob.glob('world/playerdata/*.dat'):
    files.append({"filename": file})

for x in files:
    # print(x["filename"])
    playerName = nbt.read_from_nbt_file(x["filename"]).value['bukkit'].value['lastKnownName'].value
    names.append(playerName)
    x["name"] = playerName
    count += 1
    if count > 100:
        count = 0

print(names)
print(files)