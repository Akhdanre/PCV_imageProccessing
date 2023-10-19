import cv2
import numpy as np
import pandas as pd
import glob
import os

arr = []


def getInformationInFolder(path):
    for iteration, filename in enumerate(glob.glob(os.path.join(path, '*.png'))):
        arr.append(extractFeatures(filename))

    print(arr)


def extractFeatures(image_path):
    image = cv2.imread(image_path)
    r, g, b = cv2.split(image)

    avgR = np.mean(r)
    avgG = np.mean(g)
    avgB = np.mean(b)

    return [avgR, avgG, avgB]


imagePath = "/home/akeon/Pictures"
getInformationInFolder(imagePath)

# Once you have all the features in 'arr', you can convert it to a DataFrame:
data = pd.DataFrame(arr, columns=["Average R", "Average G", "Average B"])
data.to_excel('imageRGBResult.xlsx', index=False)
