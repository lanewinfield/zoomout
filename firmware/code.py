"""
Zoom Out will send a CMD+F6 command to your computer when a switch is pulled. That's it.
"""
import time
import board
from digitalio import DigitalInOut, Direction, Pull

import adafruit_ble
from adafruit_ble.advertising import Advertisement
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.hid import HIDService
from adafruit_ble.services.standard.device_info import DeviceInfoService
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

pull_cord = DigitalInOut(board.D5)

pull_cord.direction = Direction.INPUT
pull_cord.pull = Pull.UP

hid = HIDService()

advertisement = ProvideServicesAdvertisement(hid)
advertisement.appearance = 961
scan_response = Advertisement()
scan_response.complete_name = "CircuitPython HID"

ble = adafruit_ble.BLERadio()
if not ble.connected:
	print("advertising")
	ble.start_advertising(advertisement, scan_response)
else:
	print("already connected")
	print(ble.connections)

k = Keyboard(hid.devices)
kl = KeyboardLayoutUS(k)

pressedButton = False
pulledSwitch = False

while True:
	while not ble.connected:
		pass
	print("Start typing:")

	while ble.connected:
		if pull_cord.value and not pulledSwitch: 
			k.send(Keycode.COMMAND, Keycode.F6)
			print("ENDING ZOOM CALL!!!!!!!!")
			pulledSwitch = True
			time.sleep(0.4)
		if not pull_cord.value and pulledSwitch:
			k.send(Keycode.COMMAND, Keycode.F6) 
			pulledSwitch = False
			time.sleep(0.4)

	ble.start_advertising(advertisement)
