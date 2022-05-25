import os
from PIL import Image


def read_dictionary(folder):
    images = []
    for fileName in os.listdir(folder):
        image = Image.open(folder + "/" + fileName)
        images.append(image)
    return images
