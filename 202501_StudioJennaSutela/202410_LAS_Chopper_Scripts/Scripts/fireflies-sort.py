## THIS PROGRAM WILL SCAN AN IMAGE FOR A CERTAIN COLOR VALUE
import cv2
import numpy as np
import os

# img = cv2.imread("img/path.file")

# check for value of blue

# myImg = cv2.imread(r"C:\Users\bethv\Dropbox\Family Room\BETH\00. Work Desk\14. LAS\CUTS\FLICKER2Frames\0079.png")

### FUNCTIONS ###
def curveSort(array):
    sortedArr = sorted(array) #Initially sorting the array from highest to lowest
    n = len(sortedArr)
    indices = np.argsort([np.sin(2 * np.pi * i / n) for i in range(n)])
    sineArray = [sortedArr[i] for i in indices]
    
    return sineArray  
# sineNums = curveSort(nums)

#### MAIN CODE #### 
nums = list(range(1,6507))
fourNums = [f"{num:04}" for num in nums]

#print(fourNums)
folderPath = "C:\\Users\\bethv\\Dropbox\\Family Room\\BETH\\00. Work Desk\\14. LAS\\CUTS\\FLICKER5Scrambled"
images = []
pathNums = []

print("reading images...")

# Reading images as NP arrays into a list of arrays
for i in fourNums:
    path = f"C:\\Users\\bethv\\Dropbox\\Family Room\\BETH\\00. Work Desk\\14. LAS\\CUTS\\FLICKER5Scrambled\\{i}.png"
    img = cv2.imread(path) # Reading image into 3D Array (Height, Width, RGB)
    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Converting to grayscale
    images.append(grayImg)
    pathNums.append(str(i) + ".png")
    

# Creating a list of images according to their "green" value (1)
wImages = []
#bImages = []
n = 0
wThreshold = 235
wCheck = 0

# I THINK THERE MIGHT BE A QUICKER WAY TO DO IT
for img in images:
    print(f"analysing img {n} for white pixels above wThreshold")
    whiteSum = 0
    for i in range(1080):
        for j in range(1920):
            if img[i][j] > wThreshold:
                whiteSum = whiteSum + img[i][j]
    if whiteSum > 0:
        print(f"img{n} has white")
    wImages.append(whiteSum) # Appending the whiteSum value to a list 
    n = n + 1





print("zipping images... ")    
# Creating a dictionary pairing each image path with it's whiteSum value - ZIPPING IT
imgWhiteDict = dict(zip(pathNums, wImages))
# Sorting the dict from heighst to lowest
sortedWhiteDict = dict(sorted(imgWhiteDict.items(), key=lambda item: item[1], reverse=True)) # This is a way of sorting the algorithm dictionary according to the Green Val
# making a new list of paths after they have been sorted
newPathNums = list(sortedWhiteDict.keys())

newestPathNums = []
for num in newPathNums:
    num = "0" + num
    newestPathNums.append(num)
    
idx = 0

print("renaming files...")

for p in pathNums:
    old = os.path.join(folderPath, p)
    new = os.path.join(folderPath, newestPathNums[idx])
    os.rename(old, new)
    idx = idx + 1


print("All good!")
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



