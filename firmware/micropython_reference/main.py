"""Persistent minimal reference diagnostic; no SD, radio, or usage bridge."""
from machine import Pin, SPI, PWM
import st7789py
import time
sd_cs = Pin(4, Pin.OUT, value=1)
light = PWM(Pin(22), freq=1000, duty_u16=7864)
spi = SPI(1, baudrate=1000000, polarity=0, phase=0, sck=Pin(7), mosi=Pin(6), miso=Pin(5))
tft = st7789py.ST7789(spi, 240, 320, reset=Pin(21, Pin.OUT), cs=Pin(14, Pin.OUT), dc=Pin(15, Pin.OUT), backlight=None, rotation=0)
frame = 0
while True:
    color = (65535, 0, 63488, 2016, 31)[frame % 5]
    tft.fill(color)
    print('REFERENCE_FRAME', frame, hex(color))
    frame += 1
    time.sleep(3)
