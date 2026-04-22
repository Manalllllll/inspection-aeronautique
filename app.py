import streamlit as st
from ultralytics import YOLO
from PIL import Image
from gtts import gTTS
import os
import base64
from io import BytesIO
import re
import datetime
import gdown

# Speech recognition optionnel
try:
    import speech_recognition as sr
    MICRO_DISPONIBLE = True
except:
    MICRO_DISPONIBLE = False
