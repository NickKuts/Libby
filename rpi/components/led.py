from gpiozero import LED
from time import sleep

# Replace with the actual pin
pin = 18

led = LED(pin)

# Turn led on
led.on()

# Turn led off
led.off()

while True:
    led.on()
    sleep(1)
    led.off()
    sleep(1)

