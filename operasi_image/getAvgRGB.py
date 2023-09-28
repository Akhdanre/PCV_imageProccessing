import cv2
import numpy as np
import pandas as pd

def extractFitures(image_path):
    image = cv2.imread(image_path)
    r, g, b = cv2.split(image)

    avgR =  np.mean(r)
    avgG = np.mean(g)
    avgB = np.mean(b)


    return [ avgR, avgG, avgB]

imagePath = "/home/akeon/Pictures/Screenshot_20230927_141320.png"
features = extractFitures(imagePath)
featureMatrix = np.reshape(features, (1, len(features)))
data = pd.DataFrame(featureMatrix, columns=["Average R", "Average G", "Average B"])
data.to_excel('imageRGBResutl.xlsx', index=False)