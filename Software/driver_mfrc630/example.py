import time

from mfrc630 import mfrc630
from mfrc630.mfrc630_defines import *
from mfrc630.spi import *

def loop():
    if not mfrc.PICC_IsNewCardPresent():
        return
    if not mfrc.PICC_ReadCardSerial():
        # TODO handle results
        return

    print("Card UID:", mfrc.uid.uid)

    picc_type = mfrc.PICC_GetType(mfrc.uid.sak)
    print("PICC type:",  mfrc.PICC_GetTypeName(picc_type))
    if picc_type != PICC_TYPE_MIFARE_UL:
        print("This sample only works with MIFARE Ultralight cards.")
        return

    print("Read block A(4) : the first of the sector TWO")

    resp = mfrc.MIFARE_Read(4)
    print("Resp", 4, resp)

    # Wait for debug
    print("wait")
    time.sleep(2)

    resp = mfrc.MIFARE_Read(4)
    print("Resp", 4, resp)
    
    # Wait for debug
    print("wait")
    time.sleep(2)

    return

    data = [8, 0, 0, 0]
    status = mfrc.MIFARE_Ultralight_Write(0x90, data)
    if (status != STATUS_OK):
        print("Write failed:", mfrc.GetStatusCodeName(status))


    print(mfrc.GetStatusCodeName(status))

    # Halt PICC
    # Necessary field off for select again
    mfrc.PICC_HaltA()

    # Stop encryption on PCD
    # Close session, if card present, card is selected again
    mfrc.PCD_StopCrypto1()


spi_hw = SpiHw()
# spi = SpiGpio(spi_hw, 16) #16=CS_GPIO
mfrc = mfrc630.MFRC630(spi_hw)

ver = mfrc.PCD_ReadRegister(VERSION_REG)

print("MFRC630 version", ver)

while True:
    loop()
    time.sleep(1)


