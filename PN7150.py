from supervisor import ticks_ms
from time import sleep
from digitalio import DigitalInOut, Pull
from busio import I2C

_TICKS_PERIOD = const(1<<29)

STATUS_OK = const(0x00)

_status = {
    # Status
    0x00: "OK",
    0x01: "REJECTED",
    0x02: "RF_FRAME_CORRUPTED",
    0x03: "FAILED",
    0x04: "NOT_INITIALIZED",
    0x05: "SYNTAX_ERROR",
    0x06: "SEMANTIC_ERROR",
    0x09: "INVALID_PARAM",
    0x0a: "MESSAGE_SIZE_EXCEEDED",
    # Discovery
    0xa0: "ALREADY_STARTED",
    0xa1: "TARGET_ACTIVATION_FAILED",
    0xa2: "TEAR_DOWN",
    # RF
    0xb0: "TRANSMISSION_ERROR",
    0xb1: "PROTOCOL_ERROR",
    0xb2: "TIMEOUT_ERROR",
}
def status(nr: int):
    return _status.get(nr, None) or "0x{:02x}".format(nr)

def dump_package(buf: bytes, end: int, prefix: str = ""):
    fst, snd = buf[0], buf[1]
    if fst & 0xe0 == 0:
        print("{}Data packet to/from {} length {}".format(prefix, buf[0] & 0x0f, buf[2]))
    elif fst == 0x20 and snd == 0x00:
        print("{}CORE_RESET_CMD({}) Reset Configuration: {}".format(prefix, end, buf[3]))
    elif fst == 0x40 and snd == 0x00:
        print("{}CORE_RESET_RSP({}) Status: {} NCI Version: 0x{:02x} Configuration Status: 0x{:02x}".format(
            prefix, end, status(buf[3]), buf[4], buf[5]))
    elif fst == 0x20 and snd == 0x01:
        print("{}CORE_INIT_CMD({})".format(prefix, end))
    elif fst == 0x40 and snd == 0x01:
        # 3    Status
        # 4    NFCC Features
        #      ..
        # 8    #RF Interfaces
        #      RF Interfaces
        # 9+n  Max Logical Connections
        # 10+n Max Routing Table
        #      ..
        # 12+n Max Control Packet Payload Size
        # 13+n Max Size for Large Parameters
        #      ..
        # 15+n Manufacturer ID
        # 16+n Manufacturer Specific Information
        n = buf[8]
        print("{}CORE_INIT_RSP({}) Status: {} #RF Interfaces: {} Max Payload Size: {}".format(
            prefix, end, status(buf[3]), n, buf[12+n]))
    elif fst == 0x60 and snd == 0x06:
        print("{}CORE_CONN_CREDITS_NTF({}) #Entries: {}".format(prefix, end, buf[3]))
    elif fst == 0x60 and snd == 0x07:
        print("{}CORE_GENERIC_ERROR_NTF({}) Status: {}".format(prefix, end, status(buf[3])))
    elif fst == 0x60 and snd == 0x08:
        print("{}CORE_INTERFACE_ERROR_NTF({}) Status: {} ConnID: {}".format(prefix, end, status(buf[3]), buf[4]))
    elif fst == 0x21 and snd == 0x00:
        print("{}RF_DISCOVER_MAP_CMD({}) #Mapping Configurations: {}".format(prefix, end, buf[3]))
    elif fst == 0x41 and snd == 0x00:
        print("{}RF_DISCOVER_MAP_RSP({}) Status: {}".format(prefix, end, status(buf[3])))
    elif fst == 0x21 and snd == 0x03:
        print("{}RF_DISCOVER_CMD({}) #Configurations: {}".format(prefix, end, buf[3]))
    elif fst == 0x41 and snd == 0x03:
        print("{}RF_DISCOVER_RSP({}) Status: {}".format(prefix, end, status(buf[3])))
    elif fst == 0x21 and snd == 0x06:
        print("{}RF_DEACTIVATE_CMD({}) Mode: {}".format(prefix, end, buf[3]))
    elif fst == 0x41 and snd == 0x06:
        print("{}RF_DEACTIVATE_RSP({}) Status: {}".format(prefix, end, status(buf[3])))
    elif fst == 0x61 and snd == 0x06:
        print("{}RF_DEACTIVATE_NTF({}) Type: {} Reason: {}".format(prefix, end, buf[3], buf[4]))
    elif fst == 0x61 and snd == 0x05:
        # 3    RF Discovery ID
        # 4    RF Interface
        # 5    RF Protocol
        # 6    Activation RF Technology and Mode
        # 7    Max Data Packet Payload Size
        # 8    Initial Number of Credits
        # 9    #RF Technology Specific Parameters
        #      RF Technology Specific Parameters
        # 10+n Data Exchange RF Technology and Mode
        # 11+n Data Exchange Transmit Bit Rate
        # 12+n Data Exchange Receive Bit Rate
        # 13+n #Activation Parameters
        #      Activation Parameters
        print("{}RF_INTF_ACTIVATED_NTF({}) ID: {} Interface: {} Protocol: {} Mode: 0x{:02x} #RFparams: {}".format(
            prefix, end, buf[3], buf[4], buf[5], buf[6], buf[9]))
    elif fst == 0x2f and snd == 0x02:
        print("{}PROPRIETARY_ACT_CMD({})".format(prefix, end))
    elif fst == 0x4f and snd == 0x02:
        print("{}PROPRIETARY_ACT_RSP({}) Status: {}".format(
            prefix, end, status(buf[3])))
    else:
        print("{}{:02x}:{:02x} {} bytes".format(prefix, buf[0], buf[1], end))

# MT=1 GID=0 OID=0 PL=1 ResetType=1 (Reset Configuration)
NCI_CORE_RESET_CMD = b"\x20\x00\x01\x01"
# MT=1 GID=0 OID=1 PL=0
NCI_CORE_INIT_CMD  = b"\x20\x01\x00"
# MT=1 GID=f OID=2 PL=0
NCI_PROP_ACT_CMD   = b"\x2f\x02\x00"
# MT=1 GID=1 OID=0
NCI_RF_DISCOVER_MAP_RW = b"\x21\x00\x10\x05\x01\x01\x01\x02\x01\x01\x03\x01\x01\x04\x01\x02\x80\x01\x80"
# MT=1 GID=1 OID=3
NCI_RF_DISCOVER_CMD_RW = b"\x21\x03\x09\x04\x00\x01\x02\x01\x01\x01\x06\x01"
# MODE_POLL | TECH_PASSIVE_NFCA,
# MODE_POLL | TECH_PASSIVE_NFCF,
# MODE_POLL | TECH_PASSIVE_NFCB,
# MODE_POLL | TECH_PASSIVE_15693,
NCI_RF_DEACTIVATE_CMD = b"\x21\x06\x01\x00"

class Card:
    def __init__(self, buf: bytearray, end: int):
        self.id         = buf[3]
        self.interface  = buf[4]
        self.protocol   = buf[5]
        self.modetech   = buf[6]
        self.maxpayload = buf[7]
        self.credits    = buf[8]
        self.nrfparams  = buf[9]
        self.rest       = buf[10:end]

    def nfcid1(self) -> str:
        # decode NFCID1 of rfts for NFC_A_PASSIVE_POLL_MODE
        if self.modetech != 0x00:
            return None

        id_length = self.rest[2]

        return ":".join("{:02x}".format(x) for x in self.rest[3:3+id_length])

class PN7150:
    def __init__(self, i2c: I2C, irq: Pin, ven: Pin, addr: int = 0x28, debug: bool = False):
        self._i2c = i2c
        self._irq = DigitalInOut(irq)
        self._ven = DigitalInOut(ven)
        self._addr = addr
        self._debug = debug
        self._buf = bytearray(3 + 255)
        self._ven.switch_to_output(False)
        self._irq.switch_to_input(Pull.DOWN)

    def off(self):
        self._ven.value = 0

    def reset(self):
        self._ven.value = 0
        sleep(.001)
        self._ven.value = 1
        sleep(.003)

    def __read(self):
        self._i2c.readfrom_into(self._addr, self._buf, start=0, end=3);
        end = 3 + self._buf[2]
        if end > 3:
            self._i2c.readfrom_into(self._addr, self._buf, start=3, end=end)
        if self._debug:
            dump_package(self._buf, end, prefix="< ")
        return end

    def _read(self, timeout: int = 5):
        base = _TICKS_PERIOD - ticks_ms()
        while self._irq.value == 0:
            if (base + ticks_ms()) % _TICKS_PERIOD >= timeout:
                return 0
        return self.__read()

    def _write(self, cmd: bytes, end: int = 0):
        # discard incoming messages
        while self._irq.value == 1:
            self.__read()
        if not end:
            end = len(cmd)
        if self._debug:
            dump_package(cmd, end, prefix="> ")
        return self._i2c.writeto(self._addr, cmd, end=end)

    def _connect(self):
        self.reset()
        self._write(NCI_CORE_RESET_CMD)
        end = self._read(15)
        if (end < 6 or self._buf[0] != 0x40 or self._buf[1] != 0x00
                or self._buf[3] != STATUS_OK or self._buf[5] != 0x01):
            return False
        self._write(NCI_CORE_INIT_CMD)
        end = self._read()
        if end < 20 or self._buf[0] != 0x40 or self._buf[1] != 0x01 or self._buf[3] != STATUS_OK:
            return False

        nRFInt = self._buf[8]
        self.fw_version = self._buf[17 + nRFInt:20 + nRFInt]
        #print("Firmware version: 0x{:02x} 0x{:02x} 0x{:02x}".format(
        #    self.fw_version[0], self.fw_version[1], self.fw_version[2]))

        self._write(NCI_PROP_ACT_CMD)
        end = self._read()
        if end < 4 or self._buf[0] != 0x4F or self._buf[1] != 0x02 or self._buf[3] != STATUS_OK:
            return False

        #print("FW_Build_Number:", self._buf[4:8])

        return True

    def connect(self):
        assert self._i2c.try_lock()
        try:
            ok = self._connect()
        finally:
            self._i2c.unlock()
        return ok

    def modeRW(self):
        assert self._i2c.try_lock()
        self._write(NCI_RF_DISCOVER_MAP_RW)
        end = self._read(10)
        self._i2c.unlock()
        return end >= 4 and self._buf[0] == 0x41 and self._buf[1] == 0x00 and self._buf[3] == STATUS_OK

    def startDiscoveryRW(self):
        assert self._i2c.try_lock()
        self._write(NCI_RF_DISCOVER_CMD_RW)
        end = self._read()
        self._i2c.unlock()
        return end >= 4 and self._buf[0] == 0x41 and self._buf[1] == 0x03 and self._buf[3] == STATUS_OK

    def stopDiscovery(self):
        assert self._i2c.try_lock()
        self._write(NCI_RF_DEACTIVATE_CMD)
        end = self._read()
        self._i2c.unlock()
        return end >= 4 and self._buf[0] == 0x41 and self._buf[1] == 0x06 and self._buf[3] == STATUS_OK

    def waitForCard(self):
        assert self._i2c.try_lock()
        while True:
            end = 0
            while end == 0:
                end = self._read()
            if self._buf[0] == 0x61 and self._buf[1] == 0x05:
                break
        self._i2c.unlock()

        return Card(self._buf, end)

    def tagCmd(self, cmd: bytes, connID: int = 0):
        assert self._i2c.try_lock()
        self._buf[0] = connID
        self._buf[1] = 0x00
        self._buf[2] = len(cmd)
        end = 3 + len(cmd)
        self._buf[3:end] = cmd
        self._write(self._buf, end=end)

        while True:
            end = self._read()
            if self._buf[0] & 0xe0 == 0x00:
                break

        self._i2c.unlock()
        return self._buf[3:end]
