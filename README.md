# Py-ShellyEM-EPD2in13-RPi
Display energy readings from Shelly EM on the Waveshare 2.13" Touch eInk display 

![](https://github.com/adrianh-za/py-shellyem-epd2in13-rpi/blob/a5c6456e48d73db1748f9f3032d70bbded0e9957/assets/pics/epd2in13.png)

**eInk Display from Waveshare**

[2.13inch Touch e-Paper HAT for Raspberry Pi, 250×122, Black / White, SPI](https://www.waveshare.com/2.13inch-touch-e-paper-hat.htm)

>- 2.13" capacitive touch e-Paper display, 5-point touch, 250×122 pixels
>- Supports waken up by user-defined gesture
>- No backlight, keeps displaying last content for a long time even when power down
>- Ultra low power consumption, basically power is only required for refreshing
>- Standard Raspberry Pi 40PIN GPIO extension header, supports Raspberry Pi series boards
>- SPI interface, for connecting with controller boards like Arduino/STM32, etc.

**eInk Display with case for Raspberry Pi Zero from Waveshare**

>* Same display as above but with matching case for Raspberry Pi Zero / Zero W / Zero 2

[2.13inch Touch e-Paper HAT for Raspberry Pi, 250×122, Black / White, SPI with case](https://www.waveshare.com/2.13inch-touch-e-paper-hat-with-case.htm)

## Usage

Get the Pi ready

1) `sudo raspi-config`  (Enable I2C and SPI)
2) `sudo apt update`  (Update the OS)
3) `sudo apt install git` 	(Install GIT to clone from github.com) 
4) `sudo reboot -f`	 (Reboot the RPi)

Once rebooted

5) `sudo apt install python3 python3-pip python3-pil python3-smbus`  (Install Python and support libraries)
6) `git clone https://github.com/adrianh-za/py-shellyem-epd2in13-rpi` (Download this module)
7) `cd py-shellyem-epd2in13-rpi` (Browse to this module's location.  Could be located elsewhere)
8) run `main.py` and `main-touch.py`
9) ctrl-c to quit


## Notes

- The readings are refreshed every 10 seconds.  This can be changed in `config.py`.

- The Url/IP for your Shelly EM can be set in `config.py`.

- The module does a full display refresh after every 100 partial refresh.  Due to using partial refreshes, there are when some of the numbers
are a little garbled.  This is expected and will clear up after a few refreshes.

- You may need to change the I2C address in the module when running `main-touch.py`.  To check which I2C address the eInk display is using on your RPi,
install `sudo apt install i2c-tools` and then run `i2cdetect -y 1` to check what address is being used.  Then check the `main-touch.py` file and look for `gt = gt1151.GT1151(0x14)` and replace in input argument with your address.


## Various Resources and Info ##

[Waveshare 2.13inch Touch e-Paper HAT Manual](https://www.waveshare.com/wiki/2.13inch_Touch_e-Paper_HAT_Manual#Raspberry_Pi)

[Waveshare e-Paper (Python code)](https://github.com/waveshare/e-Paper/tree/master/RaspberryPi_JetsonNano/python)

[Touch_e-Paper_HAT (C and Python code)](https://github.com/waveshare/Touch_e-Paper_HAT)

[ePaper-Spotify-Clock (Written in Python)](https://github.com/alexthescott/ePaper-Spotify-Clock)

[Raspberry-Pi-E-Ink-Dashboard (Written in Python)](https://github.com/zoharsf/Raspberry-Pi-E-Ink-Dashboard)
