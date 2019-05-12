import logging
from itertools import product
import numpy as np
import sys
from PIL import Image

import pydicom as dicom
import os
import cv2



logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

COLOR_MAPS = ("COLORMAP_BONE", "COLORMAP_JET", "COLORMAP_WINTER", "COLORMAP_RAINBOW",
    "COLORMAP_OCEAN", "COLORMAP_HOT", "COLORMAP_HSV")

def export_to_png(path, dic_ds):
    # make it True if you want in PNG format
    image = ""
    # Specify the .dcm folder path
    for n, ds in enumerate(dic_ds):
        pixel_array_numpy = ds.pixel_array
        image = str(n) + ".png"
        cv2.imwrite(os.path.join(path, image), pixel_array_numpy)
        imgray = cv2.imread(os.path.join(path, image))

        for cmap in COLOR_MAPS:
            im_color = cv2.applyColorMap(imgray, getattr(cv2, cmap))
            cv2.imwrite(os.path.join(path, "{}{}.png".format(n, cmap)), im_color)

    # imageShape = (voxels.shape[0], voxels.shape[1])
    # img = Image.new("I", imageShape)
    # pixels = img.load()
    
    # interestingKValues = []
    # current_k = 0
    
    # max_values = _get_maximum_values(voxels)
    
    # for k, i, j in product(range(voxels.shape[2]), range(voxels.shape[0]), range(voxels.shape[1])):
        
    #     # initialize every time k changes
    #     if current_k != k:
    #         _save_image("{}/{}.png".format(path, current_k), img)
    #         img = Image.new("L", imageShape)
    #         pixels = img.load()
    #         current_k = k
            
    #     # Rescaling grey scale between 0-255
    #     pixels[i,j] = int((float(voxels[i,j,k]) / float(max_values[k])) * 250.0)

    # print("PIXELS: ", pixels[0, 0], pixels[1, 1])

    # _save_image("{}/{}.png".format(path, k), img)

def _get_maximum_values(voxels):
    max_values = []
    max_value = sys.maxsize*-1
    current_k = 0
    
    for k, i, j in product(range(voxels.shape[2]), range(voxels.shape[0]), range(voxels.shape[1])):
        if current_k != k:
            max_values.append(max_value)
            max_value = sys.maxsize*-1
            current_k = k
            
        if voxels[i,j,k] > max_value:
            max_value = voxels[i,j,k]
            
    max_values.append(max_value)
    
    return max_values

def _save_image(filepath, image):
    try:
        image.save(filepath, "PNG")
    except (KeyError, IOError):
        msg = 'Cannot create images for file: {}'
        logger.info(msg.format(filepath))
        