print("Test Started")
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import flask
import boto3
import importlib.metadata as md
import tensorflow as tf
import cv2
import numpy as np
from pathlib import Path
import random
import numpy as np

from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import io
from pathlib import Path
import threading
import time
import os
import traceback


print("TensorFlow version:", tf.__version__)
print("pandas version:", pd.__version__)
print("OpenCV version:", cv2.__version__)
print("Matplotlib version:", matplotlib.__version__)
print("Flask version:", md.version("flask"))
print("boto3 version:", boto3.__version__)

print("Test Completed Successfully")