# /*****************************************************************************
# Heavily reduced and edited from https://github.com/waveshare/Touch_e-Paper_HAT/blob/main/python/lib/TP_lib/epdconfig.py
#
# This is now a separate config just for the touch part of the eInk touch screen
# /*****************************************************************************

import RPi.GPIO as GPIO
import time
from smbus import SMBus
import spidev
import ctypes
import logging

# TP
TRST_PIN    = 22
INT_PIN     = 27


address = 0x0
# address = 0x14
# address = 0x48
bus     = SMBus(1)

def digital_write(pin, value):
    GPIO.output(pin, value)

def digital_read(pin):
    return GPIO.input(pin)

def delay_ms(delaytime):
    time.sleep(delaytime / 1000.0)

def i2c_writebyte(reg, value):
    bus.write_word_data(address, (reg>>8) & 0xff, (reg & 0xff) | ((value & 0xff) << 8))

def i2c_write(reg):
    bus.write_byte_data(address, (reg>>8) & 0xff, reg & 0xff)

def i2c_readbyte(reg, len):
    i2c_write(reg)
    rbuf = []
    for i in range(len):
        rbuf.append(int(bus.read_byte(address)))
    return rbuf

def module_init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(TRST_PIN, GPIO.OUT)
    GPIO.setup(INT_PIN, GPIO.IN)
    
    return 0

def module_exit():
    bus.close()
        
    logging.debug("close 5V, Module enters 0 power consumption ...")
    GPIO.output(TRST_PIN, 0)
    
    GPIO.cleanup([TRST_PIN, INT_PIN])


### END OF FILE ###