import random
import os

stills = list(range(1,3872)) # MAKE SURE TO ADJUST END-FRAME


## Store paths
shuffledStills = [f"{num:04}" for num in stills] ## formats stills to 00001 - 01925
random.shuffle(shuffledStills)

# print(shuffledStills)

#path = r"C:\Users\bethv\Dropbox\Family Room\BETH\00. Work Desk\14. LAS\CUTS\FLICKER1Scrambled" ## IT WAS DONE DIRECTLY ON THE FOLDER (MICROSCOPIC)
path = r"C:\\Users\\bethv\\Dropbox\\Family Room\\BETH\\LAS Footage\\For Beth to chop and remix\\Choppedd\\FRAMES04HandsBlue" ## (Color Graded)


files = os.listdir(path)

print(files)

formattedStills = []

for s in shuffledStills:
    formattedStills.append(s+".png")
    
print(formattedStills)


id = 0

for f in files:
    old = os.path.join(path, f)
    new = os.path.join(path, formattedStills[id])
    os.rename(old, new)
    id = id + 1

## Write frame nemes to btoh framesOriginal and framesShuffled


##
## path 1 range "0001" - "1925"
## "C:\Users\bethv\Dropbox\Family Room\BETH\00. Work Desk\14. LAS\BethsCutFrames"
## path 2
## "C:\Users\bethv\Dropbox\Family Room\BETH\00. Work Desk\14. LAS\BethsCutFramesScrambled"
##


