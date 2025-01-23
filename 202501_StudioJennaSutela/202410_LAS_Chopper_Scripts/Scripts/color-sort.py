## THIS PROGRAM WILL SCAN AN IMAGE FOR A CERTAIN COLOR VALUE
import cv2
import numpy as np
import os

# img = cv2.imread("img/path.file")

# check for value of blue

# myImg = cv2.imread(r"C:\Users\bethv\Dropbox\Family Room\BETH\00. Work Desk\14. LAS\CUTS\FLICKER2Frames\0079.png")

nums = list(range(4000,5336)) #5337
fiveNums = [f"{num:04}" for num in nums]

#print(fourNums)
folderPath = "C:\\Users\\bethv\\Dropbox\\Family Room\\BETH\\LAS Footage\\For Beth to chop and remix\\Choppedd\\FRAMES03DolphinsWavesBlue"
images = []
pathNums = []

# Reading images as NP arrays into a list of arrays.
for i in fiveNums:
    path = f"C:\\Users\\bethv\\Dropbox\\Family Room\\BETH\\LAS Footage\\For Beth to chop and remix\\Choppedd\\FRAMES03DolphinsWavesBlue\\{i}.png"
    img = cv2.imread(path)
    print(f"reading image {i}")
    images.append(img)
    pathNums.append(str(i) + ".png")
    

# Creating a list of images according to their "green" value (1)
wImages = []
#gImages = []
#bImages = []
#rImages = []
n = 0

for img in images:
    white = np.sum(img[:,:,:]) # Sum of all)
    #green = np.sum(img[:,:,1]) # Sum of pixel green values across entire matrix
    #blue = np.sum(img[:,:,0])
    #red = np.sum(img[:,:,2])
    wImages.append(white)
    #gImages.append(green)
    #bImages.append(blue)
    #rImages.append(red)
    print(f"extracting {white} white from " + str(n))
    n = n + 1
    
# Creating a dictionary pairing each image path with it's total green calue - ZIPPING IT
imgColorDict = dict(zip(pathNums, wImages))
# Sorting the dict from heighst to lowest
sortedColorDict = dict(sorted(imgColorDict.items(), key=lambda item: item[1], reverse=True)) # This is a way of sorting the algorithm dictionary according to the Green Val
# making a new list of paths after they have been sorted
newPathNums = list(sortedColorDict.keys())
print(sortedColorDict)

newestPathNums = []
for num in newPathNums:
    num = "0" + num
    newestPathNums.append(num)
    

idx = 0

print("Reogranising!")

for p in pathNums:
    old = os.path.join(folderPath, p)
    new = os.path.join(folderPath, newestPathNums[idx])
    os.rename(old, new)
    idx = idx + 1


print("All good.")
############
##### I THINK YOU COULD HAVE DONE IT IN A SMARTER WAY BY JUST MAKING MORE ADVANCED MATRIX MULTIPLLICATIONS WITH NUMPY BUT THIS IS GOOD FOR NOW
##### SOMEHOW I THINK IT WOULD HAVE BEEN COOLER AND MORE MATHY IF YOU HAD JUST USED NUMPY OPERATIONS
##### MAYBE JUST GET BETTER AT THAT
############



    




#print("Image Shape:")
#print(myImg.shape)

#print("Pixel 500, 1000 Value:")
#print(myImg[0,0])

#print(myImg[:, :, 0]) # Green Value of each pixel in frame

#print(np.sum(myImg[:,:,0])) # Total Blue in image



