import time
import struct
from typing import List, Dict
from tqdm import tqdm

from mfrc630 import mfrc630
from mfrc630.mfrc630_defines import *
from mfrc630.ttnfc_opcodes import *


class TTNfc:
    def __init__(self, mfrc):
        self.mfrc = mfrc

# Start / stop functions
    def waitForSensor(self, retries=-1):
        i = 0
        print("Waiting for sensor...")
        while True:
            time.sleep(0.5)
            i += 1
            if i == retries:
                return
            if self.mfrc.PICC_IsNewCardPresent():
                if not self.mfrc.PICC_ReadCardSerial():
                    print("ERROR: not selected")
                    continue
                return self.mfrc.uid.uid

    def stop(self):
        self.mfrc.PICC_HaltA()
        self.mfrc.PCD_StopCrypto1()
        return True

    def resetField(self, timeout=0.5):
        self.mfrc.PCD_StopCrypto1()
        self.mfrc.PCD_AntennaOff()
        time.sleep(timeout)
        self.mfrc.PCD_AntennaOn()
        #TODO seleccionar directamente en lugar de esperar al sensor
        #TODO timeout waitForSensor
        rc = self.waitForSensor(retries=10)
        if not rc:
            print("No sensor found")
            return False
        print(f"Reset field")

# NFC low level functions
    def writeOp(self, op: int) -> int:
        cmd = struct.pack("<I", op)
        status = self.mfrc.MIFARE_Ultralight_Write(0x90, cmd)
        if status != STATUS_OK:
            print(f"Write op {hex(op)} failed: {self.mfrc.GetStatusCodeName(status)}")
        return status

    def write(self, reg: int, val: int) -> int:
        cmd = struct.pack("<I", val)
        status = self.mfrc.MIFARE_Ultralight_Write(0xA0 + reg, cmd)
        if status != STATUS_OK:
            print("Write failed:", self.mfrc.GetStatusCodeName(status))
        return status

    def write_raw(self, data: List[int]) -> int:
        if data is None:
            return STATUS_INVALID

        self.mfrc.PCD_WriteRegister(COMMAND_REG, IDLE_CMD)
        self.mfrc.PCD_ClearFifo()
        self.mfrc.PCD_EnableGlobalIrq()
        self.mfrc.PCD_ConfigureT0()
        self.mfrc.PCD_ClearInterrupts()

        send_data = [0xA3] + data
        rsp = self.mfrc.PCD_TransceiveData(send_data, back=False, crc=True)

        # sendData.append(0xA3) # TycheTools raw write command
        # sendData += data
        # crc = self.mfrc.PCD_CalculateCRC(sendData)
        # sendData += crc
        # resp = self.mfrc.PCD_TransceiveData(sendData, False)
        #TODO Check ACK?

        return rsp.status

    def read(self, addr: int) -> List[int]:
        rsp = self.mfrc.MIFARE_Read(0xA0 + addr)
        if rsp.status != STATUS_OK:
            print(self.mfrc.GetStatusCodeName(rsp.status))
            return None
        return rsp.data

# NFC operations
    def retart(self):
        self.writeOp(TTNfcOp.restartNode)

    def factoryReset(self):
        self.writeOp(TTNfcOp.resetNode)

    def pingToGateway(self):
        self.writeOp(TTNfcOp.pingRssi)

    def sleep(self):
        self.writeOp(TTNfcOp.sleep)

    def wake(self):
        self.writeOp(TTNfcOp.wake)

    def scd4xReset(self):
        pass
        self.writeOp(TTNfcOp.scd4xReset)

    def readUUID(self):
        self.writeOp(TTNfcOp.writeUuid)
        uuid_list = self.read(TTNfcOffset.uuid)
        if uuid_list is None:
            return None
        uuid = ""
        for i in uuid_list:
            uuid += f"{i:x}"
        return uuid

    def readFwVersion(self):
        self.writeOp(TTNfcOp.fwVersion)
        fw_list1 = self.read(TTNfcOffset.fwVersion)
        fw_list2 = self.read(TTNfcOffset.fwVersion + 4)
        fw1 = "".join(chr(i) for i in fw_list1)
        fw2 = "".join(chr(i) for i in fw_list2)
        return fw1 + fw2

    def readMac(self):
        self.writeOp(TTNfcOp.macAddr)
        mac_list = self.read(TTNfcOffset.macAddr)
        return "".join(chr(i) for i in mac_list[0:13])

    def readTel(self) -> Dict:
        self.writeOp(TTNfcOp.telTrig)
        res = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        try:
            while len(res) != 16 or res[2] != 0 or res[4] != 0 or res[9] != 0:
                status = self.writeOp(TTNfcOp.telRefresh)
                time.sleep(0.2)
                if status == STATUS_TIMEOUT:
                    print("Timeout")
                    continue
                res = self.read(TTNfcOffset.telemetry)
            temp = (res[1] << 8 | res[0]) / 100
            humd = res[3]
            pres = (res[8] << 24 | res[7] << 16 | res[6] << 8 | res[5]) / 10000
            rssi = res[10]
            batt = (res[13] << 8 | res[12]) / 1000
            status = [res[2], res[4], res[9]]
            return {"status": status, "temp": temp, "humd": humd, "press": pres, "bat": batt, "rssi": rssi}
        except Exception as e:
            print(f"Error reading telemetry: {e}")
            return None

    def setLeds(self, r, g, b):
        color = r | g << 8 | b << 16
        res = self.write(0, color)
        res = self.writeOp(TTNfcOp.leds)
        return res

    def checkSd(self):
        """
        Returns True if SoftDevice is disabled, False if is enabled, None if error.
        """
        self.writeOp(TTNfcOp.checkSd)
        res = self.read(0)
        if res is None:
            print("ERROR: checkSd: NFC communication error")
            return None
        return res[0] == 0

    def disableSd(self) -> bool:
        """
        Returns True if SoftDevice is disabled, False if is enabled, None if error.
        """
        # print("Reset field...")
        # self.resetField()
        self.writeOp(TTNfcOp.disableSd)
        time.sleep(5)
        self.resetField(3)
        sd = self.checkSd()
        return sd

    def startOta(self, startAddr, size):
        print(f"Start address: {startAddr}, size: {size}")
        rc = self.write(0, startAddr)
        if not rc:
            return False
        rc = self.write(1, size)
        if not rc:
            return False
        rc = self.writeOp(TTNfcOp.startOta)
        if not rc:
            return False
        return True

    def eraseOta(self):
        self.writeOp(TTNfcOp.eraseOta)
        self.resetField(timeout=5)
        otaStatus = self.checkOta()
        return otaStatus == 0

    def signature(self, signature):
        # Split signature in groups of 8
        sign_list = []
        for i in range(0, len(signature), 8):
            s = signature[i:i+8]
            b = bytes.fromhex(s)
            sign_list.append(struct.unpack("<I", b)[0])
        for i, s in enumerate(sign_list):
            rc = self.write(i, s)
            if not rc:
                return False
        return self.writeOp(TTNfcOp.signatureOta)

    def binData(self, hexData):
        hexDataSize = 16
        addrList = list(hexData.keys())
        addrList.sort()

        for i in tqdm(range(0, len(addrList), hexDataSize)):
            currentSize = hexDataSize
            if i + hexDataSize > len(addrList):
                currentSize = len(addrList) - i
            currentAddrs = addrList[i:i+currentSize]
            currentData = []
            for a in currentAddrs:
                currentData.append(hexData[a])
            for j in range(10):
                rc = self.write_raw(currentData)
                if rc == STATUS_OK:
                    #time.sleep(1)
                    break
                else:
                    self.resetField()
                    ret = self.addrOta(currentAddrs[0])
                    if not ret:
                        print("Address OTA error")
                        return
                    print(f"Communication error. Retry {j+1} in address {hex(currentAddrs[0])}")
            if rc != 1:
                print("Fatal communication error!")
                return None
        return True

    def installOta(self):
        rc = self.write(0, 1) # OTA type 1 = app
        if not rc:
            return False
        rc = self.writeOp(TTNfcOp.installOta)
        if not rc:
            return False
        return True

    def addrOta(self, addr):
        rc = self.write(0, addr)
        if not rc:
            return False
        rc = self.writeOp(TTNfcOp.addrOta)
        if not rc:
            return False
        return True

    # Checks the OTA status
    # Once the start address and OTA size is sent to the node, OTA status
    # can be checked. If ota_status_return is equal to 1, ota_status can be read.
    # ota_status can be NRF_ERROR_INVALID_STATE, NRF_ERROR_NO_MEM, NRF_SUCCESS
    # according to the Nordic Global Error Codes
    def checkOta(self):
        #TODO: set a number of retries
        while True: 
            self.writeOp(TTNfcOp.checkOta)
            res = self.read(0)
            if res is None:
                print("ERROR: checkOta: NFC communication error")
                return None
            otaStatusRet, otaStatus = struct.unpack("<II", bytes(res[0:8]))
            if otaStatusRet == 1:
                break
            time.sleep(0.5)
        return otaStatus