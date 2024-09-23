import time
from typing import List

from mfrc630.mfrc630_defines import *

# PCD: Proximity coupling device (MFRC)
# PICC: Proximity Integrated Circuit Card (Card / Iris)

class PICC_Response:
    def __init__(self, status):
        self.status = status
        self.data = None
        self.valid_bits = None


class Uid:
    def __init__(self):
        self.uid = []
        self.sak = None

class MFRC630:
    def __init__(self, spi):
        self.spi = spi
        self.PCD_Init()
        self.uid = None

    # Basic interface functions for communicating with the MFRC630
    def PCD_WriteRegister(self, reg: int, values: List[int]) -> None:
        # LSB == 0 is for writing
        self.spi.adquire()
        if isinstance(values, list):
            self.spi.xfer([reg & 0xFE] + values)
        else:
            self.spi.xfer([reg & 0xFE, values])
        self.spi.release()

    def PCD_ReadRegister(self, reg: int) -> int:
        self.spi.adquire()
        rsp = self.spi.xfer([(reg & 0xFE) | 0x01, 0])[1]
        self.spi.release()
        return rsp

    def PCD_ReadRegisterMult(self, reg: int, count: int = 1) -> List[int]:
        data = []
        for _ in range(count):
            val = self.PCD_ReadRegister(reg)
            data.append(val)
        return data

    # Functions for manipulating the MFRC630
    def PCD_Init(self) -> None:
        #TODO toggle reset power down pin for a hard reset
        # delay(50);

        self.PCD_Reset()
        self.PCD_ConfigRadio()
        self.PCD_WriteRegister(COMMAND_REG, IDLE_CMD)

        # When communicating with a PICC we need a timeout if something goes wrong.
        # f_timer = 13.56 MHz / (2 * TPreScaler + 1)
        # where TPreScaler = [TPrescaler_Hi:TPrescaler_Lo].

        # TPrescaler_Hi are the four low bits in TModeReg.
        # TPrescaler_Lo is TPrescalerReg.

        # TAuto = 1; timer starts automatically at the end of the transmission
        # in all communication modes at all speeds
        # self.PCD_WriteRegister(TMODE_REG, 0x80)

        # TPreScaler = TModeReg[3..0]
        # TPrescalerReg, ie 0x0A9 = 169 => f_timer=40kHz, ie a timer period of 25us.
        # self.PCD_WriteRegister(TPRESCALER_REG, 0xA9)

        # Reload timer with 0x3E8 = 1000, ie 25ms before timeout.
        # self.PCD_WriteRegister(TRELOAD_REGH, 0xFF)
        # self.PCD_WriteRegister(TRELOAD_REGL, 0xFF)

        # Default 0x00. Force a 100 % ASK modulation independent of the ModGsPReg
        # register setting
        # self.PCD_WriteRegister(TX_ASK_REG, 0x40)

        # Default 0x3F. Set the preset value for the CRC coprocessor for the
        # CalcCRC command to 0x6363 (ISO 14443-3 part 6.2.4)
        # self.PCD_WriteRegister(MODE_REG, 0x3D)

        # Enable the antenna driver pins TX1 and TX2
        # (they were disabled by the reset)
        # self.PCD_AntennaOn()

    def PICC_HaltA(self) -> None:
        # The standard says:
        # If the PICC responds with any modulation during a period of 1 ms after
        # the end of the frame containing the HLTA command, this response shall
        # be interpreted as 'not acknowledge'.
        # We interpret that this way: Only STATUS_TIMEOUT is an success.


        self.PCD_WriteRegister(COMMAND_REG, IDLE_CMD)
        self.PCD_ClearFifo()
        self.PCD_EnableGlobalIrq()
        self.PCD_ConfigureT0()
        self.PCD_ClearInterrupts()

        resp = self.PCD_TransceiveData([PICC_CMD_HLTA, 0], back=False, crc=True)
        if resp.status == STATUS_TIMEOUT:
            return STATUS_OK
        if resp.status == STATUS_OK:
            return STATUS_ERROR
        return resp.status

    def PCD_StopCrypto1(self) -> None:
        tmp = self.PCD_ReadRegister(STATUS_REG)
        self.PCD_WriteRegister(STATUS_REG, tmp & ~(1<<5))

    def PCD_AntennaOn(self) -> None:
        value = self.PCD_ReadRegister(DRVMOD_REG)
        self.PCD_WriteRegister(DRVMOD_REG, value | (1<<3))

    def PCD_AntennaOff(self) -> None:
        tmp = self.PCD_ReadRegister(DRVMOD_REG)
        self.PCD_WriteRegister(DRVMOD_REG, tmp & ~(1<<3))

    def PCD_GetAntennaGain(self) -> int:
        pass

    def PCD_SetAntennaGain(self, mask: int) -> None:
        pass

    def PCD_Reset(self) -> None:
        self.PCD_WriteRegister(COMMAND_REG, SOFTRESET_CMD)
        time.sleep(0.050)
        # TODO: performed in 522
        # Wait for the PowerDown bit in CommandReg to be cleared
        # while self.PCD_ReadRegister(COMMAND_REG) & (1<<4):
        #     pass # PCD still restarting - unlikely after waiting 50ms,

    def PCD_ConfigRadio(self) -> None:
        config = [0x8E, 0x12, 0x39, 0x0A, 0x18, 0x18, 0x0F, 0x21, 0x00, 0xC0, 0x12, 0xCF, 0x00, 0x04, 0x90, 0x5C, 0x12, 0x0A]
        self.PCD_WriteRegister(DRVMOD_REG, config)

    def PCD_ClearFifo(self) -> None:
        reg = self.PCD_ReadRegister(FIFOCONTROL_REG)
        self.PCD_WriteRegister(FIFOCONTROL_REG, reg | 0x10)

    def PCD_ReadFifoLen(self) -> int:
        hi = self.PCD_ReadRegister(FIFOCONTROL_REG)
        lo = self.PCD_ReadRegister(FIFOLENGTH_REG)
        if hi & 0x80:
            return lo
        else:
            return ((hi & 0x3) << 8) | lo

    def PCD_ClearInterrupts(self) -> None:
        self.PCD_WriteRegister(IRQ0_REG, 0x7F)
        self.PCD_WriteRegister(IRQ1_REG, 0x3F)

    def PCD_EnableGlobalIrq(self) -> None:
        """Enable the global IRQ for Rx done and Errors."""
        # Allow the receiver and Error IRQs to be propagated to the GlobalIRQ.
        self.PCD_WriteRegister(IRQ0EN_REG, 0x06)
        # Allow Timer0 IRQ to be propagated to the GlobalIRQ.
        self.PCD_WriteRegister(IRQ1EN_REG, 0x01)

    def PCD_ConfigureT0(self, timeout=100) -> None:
        """Configure the frame wait timeout using T0."""
        if timeout >= 300:
            timeout = 300
            print("ERROR: timeout must be < 300")
        counter = int(timeout / 0.00472) # Each tick = 4.72 us (1/211,875kHz)
        self.PCD_WriteRegister(T0CONTROL_REG, 0b10001)
        self.PCD_WriteRegister(T0RELOADHI_REG, (counter >> 8) & 0xFF)
        self.PCD_WriteRegister(T0RELOADLO_REG, counter & 0xFF)
        self.PCD_WriteRegister(T0COUNTERVALHI_REG, (counter >> 8) & 0xFF)
        self.PCD_WriteRegister(T0COUNTERVALLO_REG, counter & 0xFF)

    # Functions for communicating with PICCs:
    def PCD_TransceiveData(self, send_data: List[int], back: bool = False,
            valid_bits: int = 0, crc: bool = True) -> PICC_Response:
        return self.PCD_CommunicateWithPICC(TRANSCEIVE_CMD, send_data, back,
            valid_bits, crc)

    def PCD_CommunicateWithPICC(self, command: int, send_data: List[int],
            back: bool = False, valid_bits = 0, crc: bool = True) -> PICC_Response:
        """ Transfers data to the MFRC522 FIFO, executes a commend, waits for
        completion and transfers data back from the FIFO.

        :param command: The command to execute. One of the PCD_Command enums.
        :param send_data: List with the data to transfer to the FIFO.
        :param back: Indicates if data should be read back after executing the
            command.
        :param valid_bits: The number of valid bits in the last byte.
            0 for 8 valid bits.
        :param crc: Enables CRC.

        :return STATUS_OK on success, STATUS_??? otherwise and List with
            back data or None if back is False
        """

        if crc:
            self.PCD_WriteRegister(TXCRCPRESET_REG, 0x18 | 1)
            self.PCD_WriteRegister(RXCRCCON_REG, 0x18 | back)
        else:
            self.PCD_WriteRegister(TXCRCPRESET_REG, 0x18 | 0)
            self.PCD_WriteRegister(RXCRCCON_REG, 0x18 | 0)

        # if valid_bits is not None:
        #     tx_last_bits = valid_bits
        # else:
        #     tx_last_bits = 0

        # rx_align = BitFramingReg[6..4]. TxLastBits = BitFramingReg[2..0]
        # bit_framing = (rx_align << 4) + tx_last_bits

        self.PCD_WriteRegister(TXDATANUM_REG, (1 << 3) | valid_bits)

        # ValuesAfterColl: If cleared, every received bit after a collision is
        # replaced by a zero. This function is needed for ISO/IEC14443
        # anticollision (0<<7). We want to shift the bits with RxAlign
        self.PCD_WriteRegister(RXBITCTRL_REG, (0 << 7))

        # Stop any active command.
        self.PCD_WriteRegister(COMMAND_REG, IDLE_CMD)

        # Flush FIFO
        self.PCD_ClearFifo()

        # # Clear all seven interrupt request bits
        # self.PCD_WriteRegister(COM_IRQ_REG, 0x7F)

        # # FlushBuffer = 1, FIFO initialization
        # self.PCD_SetRegisterBitMask(FIFO_LEVEL_REG, 0x80) 

        # Write send_data to the FIFO
        self.PCD_WriteRegister(FIFODATA_REG, send_data)

        # # Bit adjustments
        # self.PCD_WriteRegister(BIT_FRAMING_REG, bit_framing)

        # Execute the command
        self.PCD_WriteRegister(COMMAND_REG, command)

        # if command == TRANSCEIVE_CMD:
        #     # StartSend=1, transmission of data starts
        #     self.PCD_SetRegisterBitMask(BIT_FRAMING_REG, 0x80)

        # Wait for the command to complete.
        # In PCD_Init() we set the TAuto flag in TModeReg.
        # This means the timer automatically starts when the PCD stops
        # transmitting.

        while True:
            # ComIrqReg[7..0] bits are:
            # Set1 TxIRq RxIRq IdleIRq HiAlertIRq LoAlertIRq ErrIRq TimerIRq
            #       1                                 1
            #       1             1                   1
            irq1 = self.PCD_ReadRegister(IRQ1_REG)


            # TODO: wait_irq
            if irq1 & 0x40: # Global IRQ (error or RX)
                break
            if irq1 & 0x01:  # Timer interrupt - nothing received in 5ms
                break
                # return PICC_Response(STATUS_TIMEOUT)

            #TODO: The emergency break.
            # If all other condions fail we will eventually terminate (timeout)

        self.PCD_WriteRegister(COMMAND_REG, IDLE_CMD)

        error_reg = self.PCD_ReadRegister(ERROR_REG)
        if error_reg:
            print(f"Error: {error_reg:02x}")
            return PICC_Response(STATUS_ERROR)

        irq0 = self.PCD_ReadRegister(IRQ0_REG)

        if irq0 & 2: # Error
            print("Transcieve data error")
            return PICC_Response(STATUS_ERROR)
        elif not irq0 & 4: # Timeout
            print("Transcieve data timeout")
            return PICC_Response(STATUS_TIMEOUT)

        #TODO read error type
        # # Stop now if any errors except collisions were detected.
        # # ErrorReg[7..0] bits are:
        # # WrErr TempErr reserved BufferOvfl CollErr CRCErr ParityErr ProtocolErr
        error_reg = self.PCD_ReadRegister(ERROR_REG)

        # # BufferOvfl ParityErr ProtocolErr
        if error_reg:
            print(f"Error: {error_reg:02x}")
            return PICC_Response(STATUS_ERROR)

        # # Tell about collisions
        # if error_reg_value & 0x08: # CollErr
        #     return PICC_Response(STATUS_COLLISION)

        back_data = None
        # back_valid_bits = None
        # If the caller wants data back, get it from the MFRC522.
        if back:
            fifo_len = self.PCD_ReadFifoLen()

            # Get received data from FIFO
            back_data = self.PCD_ReadRegisterMult(FIFODATA_REG, fifo_len)

            # RxLastBits[2:0] indicates the number of valid bits in the last
            # received byte. If this value is 000b, the whole byte is valid.
            # back_valid_bits = self.PCD_ReadRegister(CONTROL_REG) & 0x07

        #TODO check crc

        resp = PICC_Response(STATUS_OK)
        resp.data = back_data
        # resp.valid_bits = back_valid_bits
        return resp

    def PICC_ReadCardSerial(self) -> bool:
        ret = self.PICC_Select()
        return ret == STATUS_OK

    def PICC_IsNewCardPresent(self, ) -> bool:
        resp = self.PICC_RequestA()
        return resp.status == STATUS_OK or resp.status == STATUS_COLLISION

    def PICC_RequestA(self) -> PICC_Response:
        return self.PICC_REQA_or_WUPA(PICC_CMD_REQA)
    
    def PICC_REQA_or_WUPA(self, command: int) -> PICC_Response:
        self.PCD_WriteRegister(COMMAND_REG, IDLE_CMD)
        self.PCD_ClearFifo()
        self.PCD_ClearInterrupts()
        self.PCD_EnableGlobalIrq()
        self.PCD_ConfigureT0() # TODO: Configure in init

        # 7 bits of the last (and only) byte. TxLastBits = BitFramingReg[2..0]
        resp = self.PCD_TransceiveData([command], back=True, valid_bits=7,
            crc=False)
        if resp.status != STATUS_OK:
            return resp

        # ATQA must be exactly 16 bits.
        if resp.data is None or len(resp.data) != 2: #TODO: or resp.valid_bits != 0:
            return PICC_Response(STATUS_ERROR)

        return resp

    def PICC_Select(self) -> int:
        self.PCD_WriteRegister(COMMAND_REG, IDLE_CMD)
        self.PCD_ClearFifo()
        self.PCD_EnableGlobalIrq()
        self.PCD_ConfigureT0() # TODO: Configure in init

        uid = Uid()
        for cascade_lvl in range(1, 4):
            if cascade_lvl == 1:
                cmd = PICC_CAS_LEVEL_1
            elif cascade_lvl == 2:
                cmd = PICC_CAS_LEVEL_2
            elif cascade_lvl == 3:
                cmd = PICC_CAS_LEVEL_3
            else:
                return STATUS_INTERNAL_ERROR

            self.PCD_ClearInterrupts()
            send_req = [cmd, 0x20] # 0x20 = 32
            rsp = self.PCD_TransceiveData(send_req, back=True, crc=False)
            if rsp.status != STATUS_OK:
                return rsp.status

            uid_this_level = rsp.data
            bcc_val = uid_this_level[4]
            bcc_calc = uid_this_level[0] ^ uid_this_level[1] ^ uid_this_level[2] ^ uid_this_level[3]
            if bcc_val != bcc_calc:
                print("ERROR: BCC mismatch")
                return STATUS_ERROR

            uid.uid += uid_this_level[:4]

            self.PCD_ClearInterrupts()
            send_req = [cmd, 0x70] + uid_this_level
            rsp = self.PCD_TransceiveData(send_req, back=True, crc=True)
            if rsp.status != STATUS_OK:
                return rsp.status

            uid.sak = rsp.data[0]

            if not uid.sak & (1 << 2):
                self.uid = uid
                return STATUS_OK
        print("Exiting cascade loop ")

    def PICC_GetType(self, sak: int) -> int:
        if sak & 0x04:
            return PICC_TYPE_NOT_COMPLETE

        type_dict = {
            0x09: PICC_TYPE_MIFARE_MINI,
            0x08: PICC_TYPE_MIFARE_1K,
            0x18: PICC_TYPE_MIFARE_4K,
            0x00: PICC_TYPE_MIFARE_UL,
            0x10: PICC_TYPE_MIFARE_PLUS,
            0x11: PICC_TYPE_MIFARE_PLUS,
            0x01: PICC_TYPE_TNP3XXX,
        }
        if sak in type_dict:
            return type_dict[sak]
        if sak & 0x20:
            return PICC_TYPE_ISO_14443_4
        if sak & 0x40:
            return PICC_TYPE_ISO_18092

        return PICC_TYPE_UNKNOWN

    #TODO: change to enum
    def PICC_GetTypeName(self, picctype: int) -> str:
        type_name = {
            PICC_TYPE_ISO_14443_4:  "PICC compliant with ISO/IEC 14443-4",
            PICC_TYPE_ISO_18092:    "PICC compliant with ISO/IEC 18092 (NFC)",
            PICC_TYPE_MIFARE_MINI:  "MIFARE Mini, 320 bytes",
            PICC_TYPE_MIFARE_1K:    "MIFARE 1KB",
            PICC_TYPE_MIFARE_4K:    "MIFARE 4KB",
            PICC_TYPE_MIFARE_UL:    "MIFARE Ultralight or Ultralight C",
            PICC_TYPE_MIFARE_PLUS:  "MIFARE Plus",
            PICC_TYPE_TNP3XXX:      "MIFARE TNP3XXX",
            PICC_TYPE_NOT_COMPLETE: "SAK indicates UID is not complete.",
            PICC_TYPE_UNKNOWN:      "Unknown type",
        }

        if picctype in type_name:
            return type_name[picctype]

        return type_name[PICC_TYPE_UNKNOWN]

    #TODO: change to enum
    def GetStatusCodeName(self,code: int) -> str:
        status_name = {
            STATUS_OK:              "Success.",
            STATUS_ERROR:           "Error in communication.",
            STATUS_COLLISION:       "Collission detected.",
            STATUS_TIMEOUT:         "Timeout in communication.",
            STATUS_NO_ROOM:         "A buffer is not big enough.",
            STATUS_INTERNAL_ERROR:  "Internal error in the code. Should not happen.",
            STATUS_INVALID:         "Invalid argument.",
            STATUS_CRC_WRONG:       "The CRC_A does not match.",
            STATUS_MIFARE_NACK:     "A MIFARE PICC responded with NAK.",
        }

        if code in status_name:
            return status_name[code]

        return "Unknown error"

    def MIFARE_Read(self, block_addr: int) -> PICC_Response:
        self.PCD_WriteRegister(COMMAND_REG, IDLE_CMD)
        self.PCD_ClearFifo()
        self.PCD_EnableGlobalIrq()
        self.PCD_ConfigureT0()
        self.PCD_ClearInterrupts()

        send_req = [MF_CMD_READ, block_addr]
        return self.PCD_TransceiveData(send_req, back=True, crc=True)


    def MIFARE_Ultralight_Write(self, page: int, data: List[int]) -> int:
        if data is None or len(data) < 4:
            return STATUS_INVALID

        self.PCD_WriteRegister(COMMAND_REG, IDLE_CMD)
        self.PCD_ClearFifo()
        self.PCD_EnableGlobalIrq()
        self.PCD_ConfigureT0()
        self.PCD_ClearInterrupts()

        send_data = [MF_CMD_UL_WRITE, page] + list(data)
        rsp = self.PCD_TransceiveData(send_data, back=False, crc=True)
        return rsp.status
