'''
This program detects boxes from the given input files.

Author: Vaibhavi Awghate
'''

# import the necessary packages
import cv2
import argparse
import json

# parse the arguments and read the input file
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to the input image")
args = vars(ap.parse_args())
img = cv2.imread(args["image"])

# convert the image to grayscale and threshold it
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_TOZERO)[1]

# find contours in the thresholded image and store the contours in a dictionary
image, contours,h = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
data = {}
data['boxes']= []

# plot the boxes
for cnt in contours:
    data['boxes'].append({'points': cnt.tolist()})
    approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
    if len(approx) == 4:
        (x, y, w, h) = cv2.boundingRect(approx)
        if h >= 15:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 3)

# print the response
with open('response.txt', 'w') as outfile:
    json.dump(data, outfile, sort_keys=True, indent=4)

with open('response.txt', 'r') as handle:
    parsed = json.load(handle)

print json.dumps(parsed, indent=4, sort_keys=True)

# show the output image
cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()

