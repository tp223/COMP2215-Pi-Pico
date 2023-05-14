# Southampton Bin Collection Notifier
# Tom Pavier
# May 2022
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

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    clear()
    display.set_backlight(0.5)
    display.set_pen(WHITE)
    display.text("Connecting to WiFi...", 5, 10, scale = 2)
    display.update()
    while wlan.isconnected() == False:
        time.sleep(1)
    clear()
    display.set_backlight(0.5)
    display.set_pen(WHITE)
    display.text("Connected!", 5, 5, scale = 2)
    display.text(wlan.ifconfig()[0], 5, 20, scale = 2)
    display.update()
    
def clear():
    display.set_pen(BLACK)
    display.clear()
    display.update()
    
def isSooner(day1, month1, year1, day2, year2, month2, sameDayAllowed):
    if day1 < day2 and month1 <= month2 and year1 <= year2:
        return True
    elif sameDayAllowed and day1 <= day2 and month1 <= month2 and year1 <= year2:
        return True
    else:
        return False
    
def isPastEvent(day, month, year, currentDate):
    if currentDate[0] < year or (year == currentDate[0] and month < currentDate[1]) or (year == currentDate[0] and month == currentDate[1] and day < currentDate[2]):
        return True
    else:
        return False
    
def updateCollectionData():
    currentEvent = {}
    todaysEvents = []
    inEvent = False
    currentDate = time.localtime()
    isToday = False
    
    # Get form key -> cant submit form without this
    payload = """{
        'ddlReminder': '0',
        'btniCal': ''
    }"""

    headers = ""

    response = requests.request("GET", houseURL, headers=headers, data=str(payload))

    # Narrow down HTML
    output = None
    for line in response.text.split("\n"):
        if line.strip()[0:19] == '<input name="ufprt"':
            output = line.strip()

    # Search for key
    if output != None:
        result = output.strip()[41:393]

    # Add small delay so requests are not sent immediately after
    time.sleep(1)

    # Get iCAL data for bin collection
    body = 'ddlReminder=0&btniCal=&ufprt=' + result

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.request("POST", houseURL, headers=headers, data=body)

    currentEvent = {}
    todaysEvents = []
    nextEvent = []
    allEvents = []
    inEvent = False
    isToday = False
    
    # Parse ICAL file sent
    for line in response.text.split():
        if line == "BEGIN:VEVENT":
            inEvent = True
        elif line == "END:VEVENT":
            inEvent = False
            if not isPastEvent(currentEvent["day"], currentEvent["month"], currentEvent["year"], currentDate):
                if currentEvent["today"]:
                    todaysEvents.append(currentEvent)
                elif len(nextEvent) == 0 or isSooner(currentEvent["day"], currentEvent["month"], currentEvent["year"], nextEvent[0]["day"], nextEvent[0]["month"], nextEvent[0]["year"], False):
                    nextEvent = []
                    nextEvent.append(currentEvent)
                elif isSooner(currentEvent["day"], currentEvent["month"], currentEvent["year"], nextEvent[0]["day"], nextEvent[0]["month"], nextEvent[0]["year"], True):
                    nextEvent.append(currentEvent)
                allEvents.append(currentEvent)
            currentEvent = {}
        else:
            if inEvent:
                if "DTSTART;" in line:
                    day = int(line.split("=")[1].split(":")[1][6:8])
                    month = int(line.split("=")[1].split(":")[1][4:6])
                    year = int(line.split("=")[1].split(":")[1][0:4])
                    currentEvent["year"] = year
                    currentEvent["month"] = month
                    currentEvent["day"] = day
                    if currentDate[0] == year and currentDate[1] == month and currentDate[2] == day:
                        currentEvent["today"] = True
                    else:
                        currentEvent["today"] = False
                else:
                    parsedLine = line.split(":")
                    if parsedLine[0] == "SUMMARY":
                        currentEvent["name"] = parsedLine[1]
                    elif parsedLine[0] == "UID":
                        currentEvent["uid"] = parsedLine[1]
                    elif parsedLine[0] == "STATUS":
                        currentEvent["status"] = parsedLine[1]
    return todaysEvents, allEvents, nextEvent

def centerText(text, y, textScale):
    global display
    textWidth = display.measure_text(text, textScale, 1)
    x = math.floor((WIDTH / 2) - (textWidth / 2))
    display.text(text, x, y, scale = textScale)

led.set_rgb(0, 0, 0)

try:
    connect()
except KeyboardInterrupt:
    clear()
    display.set_backlight(0.5)
    display.set_pen(WHITE)
    display.text("Unable to connect", 5, 5, scale = 2)
    display.update()
    time.sleep(5)
    machine.reset()

clear()
display.set_backlight(0.5)
display.set_pen(WHITE)
display.text("Installing drivers...", 5, 5, scale = 2)
display.update()

upip.install('micropython-urequests')

clear()
display.set_backlight(0.5)
display.set_pen(WHITE)
display.text("Please wait...", 5, 5, scale = 2)
display.update()

todaysEvents, allEvents, nextEvent = updateCollectionData()

clear()
display.set_backlight(0.5)
display.set_pen(WHITE)
display.text("Checking dates...", 5, 5, scale = 2)
display.update()

currentDisp = -1
currentDay = time.localtime()[2]
dismissedLED = False

while True:
    if len(todaysEvents) > 0 and currentDisp != 1:
        print(todaysEvents)
        clear()
        display.set_backlight(0.5)
        display.set_pen(WHITE)
        centerText("TODAYS COLLECTION", 10, 2)
        yPos = 40
        for item in todaysEvents:
            centerText(item["name"], yPos, 3)
            yPos += 30
        display.update()
        led.set_rgb(0, 255, 0)
        dismissedLED = False
        currentDisp = 1
    elif len(todaysEvents) == 0 and currentDisp != 2:
        clear()
        display.set_backlight(0.5)
        display.set_pen(WHITE)
        centerText("NO", 10, 3)
        centerText("COLLECTION", 40, 3)
        centerText("TODAY", 70, 3)
        if len(nextEvent) > 0:
            centerText("Next Collection", 100, 1)
            centerText(str(nextEvent[0]["day"]) + "/" + str(nextEvent[0]["month"]) + "/" + str(nextEvent[0]["year"]), 110, 1)
            nextItemsRender = ""
            for event in nextEvent:
                nextItemsRender = nextItemsRender + " " + event["name"]
            centerText(nextItemsRender.strip(), 120, 1)
        display.update()
        led.set_rgb(0, 0, 0)
        dismissedLED = True
        currentDisp = 2
    if button_a.read() and dismissedLED == False:
        # Allows the user to dismiss the notification LED once the bins are placed on the kerb
        for i in range(1, 3):
            led.set_rgb(0, 255, 0)
            time.sleep(0.2)
            led.set_rgb(0, 0, 0)
            time.sleep(0.2)
        dismissedLED = True
    # Update once per day
    if (currentDay != time.localtime()[2]):
        todaysEvents, allEvents, nextEvent = updateCollectionData()
        currentDisp = -1
        currentDay = time.localtime()[2]
        