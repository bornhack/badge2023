import board
from time import sleep
from busio import I2C
from PN7150 import PN7150

if True:
    # Fast 400KHz I2C
    i2c = I2C(board.SCL, board.SDA, frequency = 400000)
else:
    # Regular 100kHz I2C
    i2c = board.I2C()

nfc = PN7150(i2c, board.IRQ, board.VEN)

assert nfc.connect()
print("Connected.")

assert nfc.modeRW()
print("Switched to read/write mode.")

while True:
    assert nfc.startDiscoveryRW()

    print("Waiting for card..")
    card = nfc.waitForCard()

    assert nfc.stopDiscovery()

    print("ID: {}".format(card.nfcid1()))

    sleep(0.5)
