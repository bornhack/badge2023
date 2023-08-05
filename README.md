# BornHack 2023 NFC Badges

![BornHack 2023 NFC Badges](https://github.com/bornhack/badge2023/raw/main/IMAGES/badges-back.jpg "BornHack 2023 NFC Badges")

With this years badges, we are taking a look at NFC. There will be two badges, one that is a tag (using the NXP NTAG I2C Plus chip), and another with an NFC reader (using NXP PN7150), that can also do card emulation.

The reader badge sports an RP2040 dual core Cortex M0+ microcontroller from Raspberry Pi and 16MB of Quad SPI flash for code and data files, to handle USB connection and general application control.

The reader badge will come with [CircuitPython](https://circuitpython.org/) preloaded, for a very low barrier of entry, all you need is a USB-C cable, and your favorite text editor and you're ready for NFC hacking.

## CircuitPython restore file

If you flash the board with something else and want to get back to CircuitPython:
Bring the badge into the UF2 bootloader. This is done by holding the BOOT button and pressing RESET or by holding BOOT while powering on.
The badge will then show up as a mass storage device called something like RP2-?. This is the built in bootloader.
Then simply copy [firmware.uf2](https://github.com/bornhack/badge2023/raw/main/firmware.uf2) from the root of this repository.
The badge will reboot, and you are then back to CircuitPython.

CircuitPython supported with this board is found in the [circuitpython branch](https://github.com/bornhack/badge2023/tree/circuitpython)

The original python files that was on the badge when handed out are in the [cp-init branch](https://github.com/bornhack/badge2023/tree/cp-init)

## Designed in KiCad v7

To open the project, you will need to install a recent release version or one of the nightly builds, KiCad v5 or v6 won't open this design. The [reader schematic as a PDF](https://github.com/bornhack/badge2023/raw/main/nfc_reader/nfc_reader_schematics.pdf) and the [tag schematic as a PDF](https://github.com/bornhack/badge2023/raw/main/nfc_card_emulation_large/nfc_card_emulation_large_schematics.pdf) are included for reference.

Main Components:

- [Raspberry Pi SoC RP2040 - low-cost, high-performance microcontroller device](https://www.raspberrypi.com/documentation/microcontrollers/rp2040.html)
    - [datasheet](https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf)
    - [RP2040 SDK Manuel](https://www.raspberrypi.com/documentation/microcontrollers/c_sdk.html#sdk-setup)
    - [RP2040 SDK git repository](https://github.com/raspberrypi/pico-sdk)
- [NXP PN7150 - High-Performance NFC Controller with Integrated Firmware](https://www.nxp.com/products/rfid-nfc/nfc-hf/nfc-readers/high-performance-nfc-controller-with-integrated-firmware-for-smart-devices:PN7150)
    - [Datasheet](https://www.nxp.com/docs/en/data-sheet/PN7150.pdf)
    - [User Manual](https://www.nxp.com/docs/en/user-guide/UM10936.pdf)
- [W25Q128JV - 128M-bit Serial Flash Memory with uniform 4KB sectors and Dual/Quad SPI](https://www.winbond.com/hq/product/code-storage-flash-memory/serial-nor-flash/?__locale=en&partNo=W25Q128JV)
    - [datasheet](https://www.winbond.com/hq/support/documentation/downloadV2022.jsp?__locale=en&xmlPath=/support/resources/.content/item/DA00-W25Q128JV.html&level=1)
- [NXP NT3H2211W0FTT - NTAG I2C plus 2K, NFC Forum Type 2 Tag with I2C interface](https://www.nxp.com/part/NT3H2211W0FTT#/)
    - [datasheet](https://www.nxp.com/docs/en/data-sheet/NT3H2111_2211.pdf)

## Projects running on the badge

Feel free to submit a PR adding on to this list with your project that runs on the badge.

- _project name and link to more info_

## License

The hardware design of the `main` branch of this repository is released under the following license:

* the "Creative Commons Attribution-ShareAlike 4.0 International License"
  (CC BY-SA 4.0) full text of this license is included in the LICENSE file
  and a copy can also be found at
  [http://creativecommons.org/licenses/by-sa/4.0/](http://creativecommons.org/licenses/by-sa/4.0/)

The CircuitPython firmware of the `circuitpython` branch is released under the MIT license with smaller dependencies under other licenses as detailed in [its LICENSE](https://github.com/bornhack/badge2023/blob/circuitpython/LICENSE) and [LICENSE_MicroPython](https://github.com/bornhack/badge2023/blob/circuitpython/LICENSE_MicroPython) files.

The Python NFC demonstration application of the `cp-init` branch is released under the MIT license as detailed in its [LICENSE file](https://github.com/bornhack/badge2023/blob/cp-init/LICENSE).
