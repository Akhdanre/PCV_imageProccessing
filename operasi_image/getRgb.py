import cv2 

def getPixelValues(imagePath):
    image = cv2.imread(imagePath)
    b, g, r = cv2.split(image)
    pixels = cv2.merge((r, g, b))
    return pixels

imagePath = "/home/akeon/Pictures/Screenshot_20230927_141320.png"
pixels = getPixelValues(imagePath)
for pixel in pixels:
    print(f"R: {pixel[0]}, G: {pixel[1]}, B: {pixel[2]}")