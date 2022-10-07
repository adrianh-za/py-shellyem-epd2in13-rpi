#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import time
from datetime import datetime, timedelta
import logging
import requests
from PIL import Image,ImageDraw,ImageFont

import config

# Files for the WaveShare can be found at https://github.com/waveshare/e-Paper
# This repo (above) currently has newer files than the repo of https://github.com/waveshare/Touch_e-Paper_HAT.
# Also, the exmaples in the "newer" repo also doesn't have examples for touchscreen.
#
# Regardless of which repo used, the below two files can just be copied from the chosen repo
#
#   epdconfig.py
#   epd2in13_V3.py
#
from lib import epd2in13_V3     # eInk display stuff
from lib import gt1151          # eInk touch stuff

fontdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'assets/fonts')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)


#Info for the Shelly EM can be found at.  
# https://shelly-api-docs.shelly.cloud/gen1/#shelly-em
class EMeter:
    power = 0
    voltage = 0
    current = 0

    def __init__(self, power, voltage):
        self.power = power
        self.voltage = voltage
        self.current = self.power / self.voltage

try:
    # Init the touch screen (uses SPI)
    epd = epd2in13_V3.EPD()
    #For older repo : epd.init(epd.FULL_UPDATE)
    epd.init()
    epd.Clear(0xFF)

    font38 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 38)

    refreshCounter = 0  #Track the number of partial refreshes.  After set number, a full refresh is performed
    nextRefresh = datetime.now()   #Immediately refresh on first run

    while (1):

        # Display energy usage from Shelly
        if (nextRefresh < datetime.now()):
        
            nextRefresh = nextRefresh + timedelta(seconds=config.SHELLY_POLL_DELAY)
        
            shelly = config.SHELLY_URI
            response: requests.Response = requests.get(shelly + "emeter/0")

            if response.ok:
                statusJson = response.json()
                eMeter = EMeter(statusJson["power"], statusJson["voltage"])
                
                # Store values in text vars.  All values rounded down to 1 decimal point.
                powerText = f"{round(eMeter.power, 1)}"
                voltageText = f"{round(eMeter.voltage, 1)}"
                currentText = f"{round(eMeter.current, 1)}"

                # Pad the left of the text using below
                # text length = rjust length
                # 6 = 6
                # 5 = 7
                # 4 = 8
                # 3 = 9
                powerTextLength = (6 - (len(powerText))) + 6
                voltageTextLength =(6 - (len(voltageText))) + 6
                currentTextLength = (6 - (len(currentText))) + 6

                #Create the canvas and write text
                canvas = Image.new('1', (epd2in13_V3.EPD_HEIGHT, epd2in13_V3.EPD_WIDTH), 255)
                draw_black = ImageDraw.Draw(canvas)
                draw_black.text((6,0), "Power:", font=font38, fill=0)
                draw_black.text((6,38), "Volt:", font=font38, fill=0)
                draw_black.text((6,76), "Amp:", font=font38, fill=0)
                draw_black.text((130,0), powerText.rjust(powerTextLength), font=font38, fill=0)
                draw_black.text((130,38), voltageText.rjust(voltageTextLength), font=font38, fill=0)
                draw_black.text((130,76), currentText.rjust(currentTextLength), font=font38, fill=0)

                #Refresh display.  Either a FULL or PARTIAL
                if (refreshCounter == 0):
                    #For older repo : epd.init(epd.FULL_UPDATE)
                    epd.display(epd.getbuffer(canvas))
                else:
                    #For older repo : epd.init(epd.PART_UPDATE)
                    epd.displayPartial(epd.getbuffer(canvas))

                # If the max number of PARTIAL updates have been performed, refresh so a FULL update is performed
                refreshCounter+=1
                if (refreshCounter == config.PARTIAL_UPDATE_COUNT):
                    refreshCounter = 0

                #Send to console
                print("==========================")
                print(f"Counter = {refreshCounter}")
                print(f"Power = {powerText}")
                print(f"Voltage = {voltageText}")
                print(f"Current = {currentText}")
                print("==========================")
                

        time.sleep(0.05)    #50 ms to not flatline CPU
        
            

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    checkForTouch = 0   #Indicates the touch IRQ thread should exit
    epd.sleep()
    time.sleep(2)
    epd.exit()
    exit()

