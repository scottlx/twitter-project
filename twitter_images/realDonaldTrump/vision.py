import os
import glob
import io
from google.cloud import vision
from google.cloud.vision import types
import csv

client = vision.ImageAnnotatorClient()
CURRENT_PATH = os.getcwd()
image_paths = glob.glob(os.path.join(CURRENT_PATH, '*.jpg'))
image_paths.sort()
print ("Number of images: ", len(image_paths));


for index, file_name in enumerate(image_paths):
	with io.open(file_name, 'rb') as image_file:
		content = image_file.read()
	image = types.Image(content=content)
	response = client.label_detection(image=image)
	labels = response.label_annotations
	print(index)
	with open("output.csv", "a") as f:
		writer = csv.writer(f)
		row=[]
		for label in labels:
			print(label.description)
			row.append(label.description)
		writer.writerow(row)
f.close()
