print("Test Started")

import tensorflow as tf
import cv2
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import flask
import boto3
import importlib.metadata as md

print("TensorFlow version:", tf.__version__)
print("OpenCV version:", cv2.__version__)
print("pandas version:", pd.__version__)
print("Matplotlib version:", matplotlib.__version__)
print("Flask version:", md.version("flask"))
print("boto3 version:", boto3.__version__)

print("Test Completed Successfully")