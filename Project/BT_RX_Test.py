#!/usr/bin/env python3
# Bluetooth Receiver Test Code
import serial
import time
import Adafruit_BBIO.UART as UART
UART.setup("UART5")
# Open serial port at 9600 baud
ser = serial.Serial(port='/dev/ttyS5', baudrate=9600)

while(1):
    time.sleep(0.35)
    while(ser.inWaiting()!=0):
        print(ser.read(ser.inWaiting()).decode())
ser.close()