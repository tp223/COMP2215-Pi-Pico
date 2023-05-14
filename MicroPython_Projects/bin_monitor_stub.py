# Southampton Bin Collection Notifier
import upip
import time
import os
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_P4
from pimoroni import RGBLED, Button
import network
import machine
import urequests as requests
import json
import re
import math

# Configuration for your network
ssid = 'WiFi SSID'
password = 'WiFi Password'

# Go to https://www.southampton.gov.uk/bins-recycling/bins/collections/ and select your address then paste the URL below
houseURL = "https://www.southampton.gov.uk/whereilive/waste-calendar?UPRN=..."

# Setup display
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_P4, rotate=0)

# Setup LED
led = RGBLED(6, 7, 8)

# Backlight to 50%
display.set_backlight(0.5)

# set up constants for drawing
WIDTH, HEIGHT = display.get_bounds()

# Configure colours
BLACK = display.create_pen(0, 0, 0)
WHITE = display.create_pen(255, 255, 255)
CYAN = display.create_pen(0, 255, 255)
MAGENTA = display.create_pen(255, 0, 255)
YELLOW = display.create_pen(255, 255, 0)
GREEN = display.create_pen(0, 255, 0)

# set up buttons
button_a = Button(12)
button_b = Button(13)
button_x = Button(14)
button_y = Button(15)

# Connect to WiFi
def connect():
    
def clear():
    display.set_pen(BLACK)
    display.clear()
    display.update()

# If day/mont/year1 sooner than day/month/year2 (you may find a better solution to this)
def isSooner(day1, month1, year1, day2, year2, month2, sameDayAllowed):

# If date is in the past (currentDate -> time.localtime())
def isPastEvent(day, month, year, currentDate):
    
# Returns lists of todaysEvents, nextEvent (where nextEvent is all events on next collection day)
def updateCollectionData():

def centerText(text, y, textScale):
    global display
    textWidth = display.measure_text(text, textScale, 1)
    x = math.floor((WIDTH / 2) - (textWidth / 2))
    display.text(text, x, y, scale = textScale)


while True:
    # Main loop