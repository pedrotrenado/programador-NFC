import time
import json
import re
import zipfile
from packaging import version
from typing import Dict, Tuple
import RPi.GPIO as GPIO

from mfrc630.ttnfc import *
from mfrc630.spi import *
from nfzeus_board import *


def loop():
    ttnfc.waitForSensor()
    print(f"Sensor found")
    # rc = ttnfc.setLeds(255, 255, 255)
    # print(f"LEDs set: {rc}")
    uuid = ttnfc.readUUID()
    print(f"  UUID: {uuid}")
    fw_ver = ttnfc.readFwVersion()
    print(f"  FW version: {fw_ver}")
    mac = ttnfc.readMac()
    print(f"  MAC: {mac}")
    tel = ttnfc.readTel()
    temp, humd, press, bat, rssi = _get_tel(tel)
    print(f"  Telemetry: {temp} ºC, {humd} %rH, {press} hPa, {bat} V, {rssi} dBm")
    print("Performing OTA...")
    rc = performOta()
    if rc != True:
        print("ERROR performing OTA")
        return False
    uid = ttnfc.waitForSensor()
    print(f"Wait for sensor")
    rc = ttnfc.stop()
    print(f"Stop: {rc}")
    return True

def _get_tel(tel):
    if tel is None:
        return [None] * 5
    temp = tel["temp"]
    humd = tel["humd"]
    press = tel["press"]
    bat = tel["bat"]
    rssi = tel["rssi"]
    return temp, humd, press, bat, rssi

def performOta():
    rc = ttnfc.disableSd()
    print(f"SoftDevice disabled: {rc}")
    if rc != True:
        return False
    rc = ttnfc.startOta(data["start_address"], data["size"])
    if rc != True:
        return False
    print(f"Start OTA: {rc}")
    rc = ttnfc.eraseOta()
    if rc != True:
        return False
    print(f"Erase OTA: {rc}")
    rc = ttnfc.signature(data["sign"])
    if rc != True:
        return False
    print(f"Signature: {rc}")
    rc = ttnfc.binData(hex_data)
    if rc != True:
        return False
    print(f"Send data: {rc}")
    rc = ttnfc.installOta()
    if rc != True:
        return False
    print(f"Install OTA: {rc}")
    time.sleep(3) # Para que no lo pille el waitForSensor antes de que se reinicie
    return True
    # ttnfc.waitForSensor(retries=10)
    #TODO: Dejar sensor puesto y que pida estado de la OTA (resultOta = 0x1D)

def hex_load(hex_raw_data: str) -> Dict[int, int]:
    hex_data = {}

    address_prefix = 0
    next_address = 0
    trailing_address = 0

    for line in hex_raw_data.splitlines():
        if line[7:9] == "02":
            address_prefix = int(line[9:13], base=16) << 4
        elif line[7:9] == "04":
            address_prefix = int(line[9:13], base=16) << 16
        elif line[7:9] == "00":
            address_base = int(line[3:7], base=16)
            address = address_prefix + address_base
            if (next_address != address and next_address):
                break
            line_data = bytes.fromhex(line[9:-2])
            for i in range(len(line_data)):
                hex_data[address+i] = line_data[i]
                if line_data[i] != 0xFF:
                    trailing_address = address+i
            next_address = address + len(line_data)

    key_list = list(hex_data.keys())
    for key in key_list:
        if key > trailing_address:
            del hex_data[key]

    return hex_data

def load_ota(ota_zip: str) -> Tuple[Dict, Dict]:
    hex_file = "app.hex"
    sign_field = "app_sign"

    with zipfile.ZipFile(ota_zip, 'r') as archive:
        ota_data = json.loads(archive.read("ota_data.json"))
        app_hex = archive.read(hex_file).decode()

    hex_data = hex_load(app_hex)

    data = {}
    data["sign"] = ota_data[sign_field]
    addresses = list(hex_data.keys())
    addresses.sort()
    data["start_address"] = addresses[0]
    data["size"] = len(hex_data)
    m = re.match("^[0-9.]+-?\w*\.?\d*", ota_data["app_version"])

    if m:
        ota_ver = version.parse(m[0])
    else:
        ota_ver = version.parse("0.0.0")

    data["major"] = ota_ver.major
    data["minor"] = ota_ver.minor
    data["fix"] = ota_ver.micro
    data["board_id"] = ota_data["board"]
    data["sd_version"] = int(ota_data["softdevice_version"], 16)

    return data, hex_data

# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(pin_rst, GPIO.OUT)
# GPIO.output(pin_rst, 1)

spi_hw = SpiHw()
# spi = SpiGpio(spi_hw, 16) #16=CS_GPIO
mfrc = mfrc630.MFRC630(spi_hw)
ttnfc = TTNfc(mfrc)

ver = mfrc.PCD_ReadRegister(VERSION_REG)
print("MFRC630 version", ver)

data, hex_data = load_ota("/home/pi/ota_data.zip")

while True:
    rc = loop()
    if rc != True:
        exit()
