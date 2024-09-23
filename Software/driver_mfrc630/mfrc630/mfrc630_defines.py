
# Registers
COMMAND_REG         = 0x00 << 1 # Starts and stops command execution
HOSTCTRL_REG        = 0x01 << 1 # Host control register
FIFOCONTROL_REG     = 0x02 << 1 # Control register of the FIFO
WATERLEVEL_REG      = 0x03 << 1 # Level of the FIFO underflow and overflow warning
FIFOLENGTH_REG      = 0x04 << 1 # Length of the FIFO
FIFODATA_REG        = 0x05 << 1 # Data In/Out exchange register of FIFO buffer
IRQ0_REG            = 0x06 << 1 # Interrupt register 0
IRQ1_REG            = 0x07 << 1 # Interrupt register 1
IRQ0EN_REG          = 0x08 << 1 # Interrupt enable register 0
IRQ1EN_REG          = 0x09 << 1 # Interrupt enable register 1
ERROR_REG           = 0x0A << 1 # Error bits showing the error status of the last command execution
STATUS_REG          = 0x0B << 1 # Contains status of the communication
RXBITCTRL_REG       = 0x0C << 1 # Control for anticoll. adjustments for bit oriented protocols
RXCOLL_REG          = 0x0D << 1 # Collision position register
TCONTROL_REG        = 0x0E << 1 # Control of Timer 0..3
T0CONTROL_REG       = 0x0F << 1 # Control of Timer0
T0RELOADHI_REG      = 0x10 << 1 # High register of the reload value of Timer0
T0RELOADLO_REG      = 0x11 << 1 # Low register of the reload value of Timer0
T0COUNTERVALHI_REG  = 0x12 << 1 # Counter value high register of Timer0
T0COUNTERVALLO_REG  = 0x13 << 1 # Counter value low register of Timer0
T1CONTROL_REG       = 0x14 << 1 # Control of Timer1
T1RELOADHI_REG      = 0x15 << 1 # High register of the reload value of Timer1
T1RELOADLO_REG      = 0x16 << 1 # Low register of the reload value of Timer1
T1COUNTERVALHI_REG  = 0x17 << 1 # Counter value high register of Timer1
T1COUNTERVALLO_REG  = 0x18 << 1 # Counter value low register of Timer1
T2CONTROL_REG       = 0x19 << 1 # Control of Timer2
T2RELOADHI_REG      = 0x1A << 1 # High byte of the reload value of Timer2
T2RELOADLO_REG      = 0x1B << 1 # Low byte of the reload value of Timer2
T2COUNTERVALHI_REG  = 0x1C << 1 # Counter value high byte of Timer2
T2COUNTERVALLO_REG  = 0x1D << 1 # Counter value low byte of Timer2
T3CONTROL_REG       = 0x1E << 1 # Control of Timer3
T3RELOADHI_REG      = 0x1F << 1 # High byte of the reload value of Timer3
T3RELOADLO_REG      = 0x20 << 1 # Low byte of the reload value of Timer3
T3COUNTERVALHI_REG  = 0x21 << 1 # Counter value high byte of Timer3
T3COUNTERVALLO_REG  = 0x22 << 1 # Counter value low byte of Timer3
T4CONTROL_REG       = 0x23 << 1 # Control of Timer4
T4RELOADHI_REG      = 0x24 << 1 # High byte of the reload value of Timer4
T4RELOADLO_REG      = 0x25 << 1 # Low byte of the reload value of Timer4
T4COUNTERVALHI_REG  = 0x26 << 1 # Counter value high byte of Timer4
T4COUNTERVALLO_REG  = 0x27 << 1 # Counter value low byte of Timer4
DRVMOD_REG          = 0x28 << 1 # Driver mode register
TXAMP_REG           = 0x29 << 1 # Transmitter amplifier register
DRVCON_REG          = 0x2A << 1 # Driver configuration register
TXL_REG             = 0x2B << 1 # Transmitter register
TXCRCPRESET_REG     = 0x2C << 1 # Transmitter CRC control register, preset value
RXCRCCON_REG        = 0x2D << 1 # Receiver CRC control register, preset value
TXDATANUM_REG       = 0x2E << 1 # Transmitter data number register
TXMODWIDTH_REG      = 0x2F << 1 # Transmitter modulation width register
TXSYM10BURSTLEN_REG = 0x30 << 1 # Transmitter symbol 1 + symbol 0 burst length register
TXWAITCTRL_REG      = 0x31 << 1 # Transmitter wait control
TXWAITLO_REG        = 0x32 << 1 # Transmitter wait low
FRAMECON_REG        = 0x33 << 1 # Transmitter frame control
RXSOFD_REG          = 0x34 << 1 # Receiver start of frame detection
RXCTRL_REG          = 0x35 << 1 # Receiver control register
RXWAIT_REG          = 0x36 << 1 # Receiver wait register
RXTHRESHOLD_REG     = 0x37 << 1 # Receiver threshold register
RCV_REG             = 0x38 << 1 # Receiver register
RXANA_REG           = 0x39 << 1 # Receiver analog register
RFU_REG             = 0x3A << 1 # (Reserved for future use)
SERIALSPEED_REG     = 0x3B << 1 # Serial speed register
LFO_TRIMM_REG       = 0x3C << 1 # Low-power oscillator trimming register
PLL_CTRL_REG        = 0x3D << 1 # IntegerN PLL control register, for mcu clock output adjustment
PLL_DIVOUT_REG      = 0x3E << 1 # IntegerN PLL control register, for mcu clock output adjustment
LPCD_QMIN_REG       = 0x3F << 1 # Low-power card detection Q channel minimum threshold
LPCD_QMAX_REG       = 0x40 << 1 # Low-power card detection Q channel maximum threshold
LPCD_IMIN_REG       = 0x41 << 1 # Low-power card detection I channel minimum threshold
LPCD_I_RESULT_REG   = 0x42 << 1 # Low-power card detection I channel result register
LPCD_Q_RESULT_REG   = 0x43 << 1 # Low-power card detection Q channel result register
PADEN_REG           = 0x44 << 1 # PIN enable register
PADOUT_REG          = 0x45 << 1 # PIN out register
PADIN_REG           = 0x46 << 1 # PIN in register
SIGOUT_REG          = 0x47 << 1 # Enables and controls the SIGOUT Pin
VERSION_REG         = 0x7F << 1 # Version and subversion register

# Comands
IDLE_CMD         = 0x00 # (no arguments) ; no action, cancels current command execution.
LPCD_CMD         = 0x01 # (no arguments) ; low-power card detection.
LOADKEY_CMD      = 0x02 # (keybyte1), (keybyte2), (keybyte3), (keybyte4), (keybyte5), (keybyte6); reads a MIFARE key (size of 6 bytes) from FIFO buffer and puts it into Key buffer. 
MFAUTHENT_CMD    = 0x03 # 60h or 61h, (block address), (card serial number byte0), (card serial number byte1), (card serial number byte2), (card serial number byte3); performs the MIFARE standard authentication. 
RECEIVE_CMD      = 0x05 # (no arguments) ; activates the receive circuit.
TRANSMIT_CMD     = 0x06 # bytes to send: byte1, byte2, ...;  transmits data from the FIFO buffer. 
TRANSCEIVE_CMD   = 0x07 # bytes to send: byte1, byte2, ....;  transmits data from the FIFO buffer and automatically activates the receiver after transmission finished. 
WRITEE2_CMD      = 0x08 # addressH, addressL, data; gets one byte from FIFO buffer and writes it to the internal EEPROM.*/
WRITEE2PAGE_CMD  = 0x09 # (page Address), data0, [data1..data63]; gets up to 64 bytes (one EEPROM page) from the FIFO buffer and writes it to the EEPROM. 
READE2_CMD       = 0x0A # addressH, address L, length; reads data from the EEPROM and copies it into the FIFO buffer. 
LOADREG_CMD      = 0x0C # (EEPROM addressH), (EEPROM addressL), RegAdr, (number of Register to be copied); reads data from the internal EEPROM and initializes the MFRC630 registers. EEPROM address needs to be within EEPROM sector 2. 
LOADPROTOCOL_CMD = 0x0D # (Protocol number RX), (Protocol number TX); reads data from the internal EEPROM and initializes the MFRC630 registers needed for a Protocol change.*/
LOADKEYE2_CMD    = 0x0E # KeyNr; copies a key from the EEPROM into the key buffer.
STOREKEYE2_CMD   = 0x0F # KeyNr, byte1, byte2, byte3, byte4, byte5, byte6; stores a MIFARE key (size of 6 bytes) into the EEPROM.*/
READRNR_CMD      = 0x1C # (no arguments) ; Copies bytes from the Random Number generator into the FIFO until the FiFo is full.
SOFTRESET_CMD    = 0x1F # (no arguments) ; resets the MFRC630.

# Status
STATE_IDLE           = 0b000  # Status register; Idle
STATE_TXWAIT         = 0b001  # Status register; Tx wait
STATE_TRANSMITTING   = 0b011  # Status register; Transmitting.
STATE_RXWAIT         = 0b101  # Status register; Rx wait.
STATE_WAIT_FOR_DATA  = 0b110  # Status register; Waiting for data.
STATE_RECEIVING      = 0b111  # Status register; Receiving data.
STATE_NOT_USED       = 0b100  # Status register; Not used.
CRYPTO1_ON           = (1<<5) # Status register; Crypto1 (MIFARE authentication) is on.

# Timer

# If set, the timer stops after receiving the first 4 bits. If cleared, the timer is not stopped automatically.
TCONTROL_STOPRX         = (1<<7)
# Do not start automatically.
TCONTROL_START_NOT      = (0b00<<4)
# Start automatically at the end of transmission.
TCONTROL_START_TX_END   = (0b01<<4)
# Timer is used for LFO trimming without underflow.
TCONTROL_START_LFO_WO   = (0b10<<4)
# Timer is used for LFO trimming with underflow.
TCONTROL_START_LFO_WITH = (0b11<<4)
# Automatically restart from the reload value when an underflow is reached.
TCONTROL_AUTO_RESTART   = (0b1<<3)
# results in 7.69e-08 ~ 76 nSec ticks.
TCONTROL_CLK_13MHZ      = (0b00)
# results in 4.52e-06 ~ 5 uSec ticks.
TCONTROL_CLK_211KHZ     = (0b01)
# The timer ticks based on alternate source 1, check datasheet.
TCONTROL_CLK_UF_TA1     = (0b10)
# The timer ticks based on alternate source 2, check datasheet.
TCONTROL_CLK_UF_TA2     = (0b11)


# Recommended register values from register 0x28 down.
# From AN11022: CLRC663 Quickstart Guide
# All the other protocols are also in there....
# Correct settings for the CRC registers for ISO14443A data frames.
RECOM_14443A_CRC = 0x18
# Recommended register values for ISO1443A at 106 kbit/s with Miller / Manchester modulation.
RECOM_14443A_ID1_106 = [0x8A, 0x08, 0x21, 0x1A, 0x18, 0x18, 0x0F, 0x27, 0x00, 0xC0, 0x12, 0xCF, 0x00, 0x04, 0x90, 0x32, 0x12, 0x0A]
# Recommended register values for ISO1443A at 212 kbit/s with Miller / BPSK modulation.
RECOM_14443A_ID1_212 = [0x8E, 0x12, 0x11, 0x06, 0x18, 0x18, 0x0F, 0x10, 0x00, 0xC0, 0x12, 0xCF, 0x00, 0x05, 0x90, 0x3F, 0x12, 0x02]
# Recommended register values for ISO1443A at 424 kbit/s with Miller / BPSK modulation.
RECOM_14443A_ID1_424 = [0x8E, 0x12, 0x11, 0x06, 0x18, 0x18, 0x0F, 0x08, 0x00, 0xC0, 0x12, 0xCF, 0x00, 0x06, 0x90, 0x3F, 0x12, 0x0A]
# Recommended register values for ISO1443A at 848  kbit/s with Miller / BPSK modulation.
RECOM_14443A_ID1_848 = [0x8F, 0xDB, 0x11, 0x06, 0x18, 0x18, 0x0F, 0x02, 0x00, 0xC0, 0x12, 0xCF, 0x00, 0x07, 0x90, 0x3F, 0x12, 0x02]

# Defines from PICC
PICC_CMD_REQA    = 0x26 # request (idle -> ready)
PICC_CMD_WUPA    = 0x52 # wake up type a (idle / halt -> ready)
PICC_CAS_LEVEL_1 = 0x93 # Cascade level 1 for select.
PICC_CAS_LEVEL_2 = 0x95 # Cascade level 2 for select.
PICC_CAS_LEVEL_3 = 0x97 # Cascade level 3 for select.
PICC_CMD_HLTA    = 0x50 # HALT command, Type A. Instructs an ACTIVE PICC to go to state HALT.

# Defines for MIFARE
MF_AUTH_KEY_A    = 0x60 # A key_type for mifare auth.
MF_AUTH_KEY_B    = 0x61 # A key_type for mifare auth.
MF_CMD_READ      = 0x30 # To read a block from mifare card.
MF_CMD_WRITE     = 0xA0 # To write a block to a mifare card.
MF_CMD_UL_WRITE  = 0xA2 # To write a block to a mifare ultralight card.
MF_ACK           = 0x0A # Sent by cards to acknowledge an operation.

# Return codes from the functions in this class. Remember to update GetStatusCodeName() if you add more.
STATUS_OK               = 1     # Success
STATUS_ERROR            = 2     # Error in communication
STATUS_COLLISION        = 3     # Collission detected
STATUS_TIMEOUT          = 4     # Timeout in communication.
STATUS_NO_ROOM          = 5     # A buffer is not big enough.
STATUS_INTERNAL_ERROR   = 6     # Internal error in the code. Should not happen ;-)
STATUS_INVALID          = 7     # Invalid argument.
STATUS_CRC_WRONG        = 8     # The CRC_A does not match
STATUS_MIFARE_NACK      = 9     # A MIFARE PICC responded with NAK.

# PICC types we can detect. Remember to update PICC_GetTypeName() if you add more.
PICC_TYPE_UNKNOWN       = 0
PICC_TYPE_ISO_14443_4   = 1     # PICC compliant with ISO/IEC 14443-4
PICC_TYPE_ISO_18092     = 2     # PICC compliant with ISO/IEC 18092 (NFC)
PICC_TYPE_MIFARE_MINI   = 3     # MIFARE Classic protocol, 320 bytes
PICC_TYPE_MIFARE_1K     = 4     # MIFARE Classic protocol, 1KB
PICC_TYPE_MIFARE_4K     = 5     # MIFARE Classic protocol, 4KB
PICC_TYPE_MIFARE_UL     = 6     # MIFARE Ultralight or Ultralight C
PICC_TYPE_MIFARE_PLUS   = 7     # MIFARE Plus
PICC_TYPE_TNP3XXX       = 8     # Only mentioned in NXP AN 10833 MIFARE Type Identification Procedure
PICC_TYPE_NOT_COMPLETE  = 255   # SAK indicates UID is not complete.


# Size of the MFRC630 FIFO
FIFO_SIZE = 512;     # The FIFO is 512 bytes.
