from django.shortcuts import render, HttpResponse
import keras
from PIL import Image
import numpy as np
import os
from django.core.files.storage import FileSystemStorage

# Load the model
model = keras.models.load_model('savedModel/model.h5')



