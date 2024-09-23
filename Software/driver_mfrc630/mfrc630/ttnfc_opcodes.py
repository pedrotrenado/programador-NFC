class TTNfcOp:
    fieldOff = 0x00
    autoProv = 0x01
    writeUuid = 0x02
    resetNode = 0x03
    pingRssi = 0x04
    isProv = 0x05
    sleep = 0x06
    wake = 0x07
    scd4xReset = 0x08
    macAddr = 0x09
    fwVersion = 0x0A
    telTrig = 0x0B
    telRefresh = 0x0C
    co2Trig = 0x0D
    co2Refresh = 0x0E
    pwmtTrig = 0x0F
    pwmtRefresh = 0x10
    restartNode = 0x11
    disableSd = 0x12
    enableSd = 0x13
    checkSd = 0x14
    startOta = 0x15
    checkOta = 0x16
    binOta = 0x17
    signatureOta = 0x18
    installOta = 0x19
    eraseOta = 0x1A
    pwmtCal = 0x1B
    leds = 0x1C
    resultOta = 0x1D
    addrOta = 0x1E


class TTNfcOffset:
    nk = 0x00
    dk = 0x04
    uaddr = 0x08
    uuid = 0x0C
    provStatus = 0x0C
    macAddr = 0x00
    fwVersion = 0x00
    telemetry = 0x00
    co2 = 0x04
    pwmt = 0x00
    otaStatusRet = 0x00
    otaStatus = 0x04