import picamera
from picamera import PiCamera
import numpy as np
import random

cam_width = 1280
cam_height = 480

scale_ratio = 0.5

cam_width = int((cam_width+31)/32)*32
cam_height = int((cam_height+15)/16)*16
#Camera resolution: "+str(cam_width)+" x "+str(cam_height)

img_width = int (cam_width * scale_ratio)
img_height = int (cam_height * scale_ratio)
capture = np.zeros((img_height, img_width, 4), dtype=np.uint8)
#Scaled image resolution: "+str(img_width)+" x "+str(img_height)

camera = PiCamera(stereo_mode='side-by-side',stereo_decimate=False)
camera.resolution=(cam_width, cam_height)
camera.framerate = 40
image_tag = random.randint(10000000,99999999)

camera.capture("image"+str(image_tag)+".png")


   