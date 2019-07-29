import shutil
import os
import cv2
import glob
import numpy as np
from PIL import Image

in_dir ='/home/owais/catkin_ws/src/'
out_dir = '/home/owais/catkin_ws/src/path_planner/maps/'


files = os.listdir(in_dir)

for f in files:
    #print(f)
    images = [cv2.imread(file) for file in glob.glob(in_dir+'original.png')]
    print(images)
    resize_img = cv2.resize(images[0], (50, 50))
    cv2.imwrite(out_dir+'original_resize.png', resize_img)

