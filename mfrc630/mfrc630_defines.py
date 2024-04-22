# Based on code Ivor Wanders 2016 

# MFRC630 Register definitions
MFRC630_REG_COMMAND = 0x00              # Starts and stops command execution
MFRC630_REG_HOSTCTRL = 0x01             # Host control register             
MFRC630_REG_FIFOCONTROL = 0x02          # Control register of the FIFO buffer
MFRC630_REG_WATERLEVEL = 0x03           # Level of the FIFO buffer
MFRC630_REG_FIFOLENGTH = 0x04           # Length of the FIFO buffer
MFRC630_REG_FIFODATA = 0x05             # Data in the FIFO buffer
MFRC630_REG_IRQ0 = 0x06                 # Interrupt register 0
MFRC630_REG_IRQ1 = 0x07                 # Interrupt register 1
MFRC630_REG_IRQ0EN = 0x08               # Interrupt enable register 0
MFRC630_REG_IRQ1EN = 0x09               # Interrupt enable register 1
MFRC630_REG_ERROR = 0x0A                # Error bits showing the error status of the last command executed
MFRC630_REG_STATUS = 0x0B               # Contains the status of the last command executed
MFRC630_REG_RXBITCTRL = 0x0C            # Control register for anticollision adjustments
MFRC630_REG_RXCOLL = 0x0D               # Collision position register
MFRC630_REG_TCONTROL = 0x0E             # Control register for timer settings
MFRC630_REG_T0CONTROL = 0x0F            # Control register for timer 0
MFRC630_REG_T0RELOADHI = 0x10           # High byte of the reload value of timer 0
MFRC630_REG_T0RELOADLO = 0x11           # Low byte of the reload value of timer 0
MFRC630_REG_T0COUNTERVALHI = 0x12       # High byte of the counter value of timer 0
MFRC630_REG_T0COUNTERVALLO = 0x13       # Low byte of the counter value of timer 0
MFRC630_REG_T1CONTROL = 0x14            # Control register for timer 1
MFRC630_REG_T1RELOADHI = 0x15           # High byte of the reload value of timer 1
MFRC630_REG_T1RELOADLO = 0x16           # Low byte of the reload value of timer 1
MFRC630_REG_T1COUNTERVALHI = 0x17       # High byte of the counter value of timer 1
MFRC630_REG_T1COUNTERVALLO = 0x18       # Low byte of the counter value of timer 1
MFRC630_REG_T2CONTROL = 0x19            # Control register for timer 2
MFRC630_REG_T2RELOADHI = 0x1A           # High byte of the reload value of timer 2
MFRC630_REG_T2RELOADLO = 0x1B           # Low byte of the reload value of timer 2
MFRC630_REG_T2COUNTERVALHI = 0x1C       # High byte of the counter value of timer 2
MFRC630_REG_T2COUNTERVALLO = 0x1D       # Low byte of the counter value of timer 2
MFRC630_REG_T3CONTROL = 0x1E            # Control register for timer 3
MFRC630_REG_T3RELOADHI = 0x1F           # High byte of the reload value of timer 3
MFRC630_REG_T3RELOADLO = 0x20           # Low byte of the reload value of timer 3
MFRC630_REG_T3COUNTERVALHI = 0x21       # High byte of the counter value of timer 3
MFRC630_REG_T3COUNTERVALLO = 0x22       # Low byte of the counter value of timer 3
MFRC630_REG_T4CONTROL = 0x23            # Control register for timer 4
MFRC630_REG_T4RELOADHI = 0x24           # High byte of the reload value of timer 4
MFRC630_REG_T4RELOADLO = 0x25           # Low byte of the reload value of timer 4
MFRC630_REG_T4COUNTERVALHI = 0x26       # High byte of the counter value of timer 4
MFRC630_REG_T4COUNTERVALLO = 0x27       # Low byte of the counter value of timer 4
MFRC630_REG_DRVMOD = 0x28               # Driver mode register
MFRC630_REG_TXAMP = 0x29                # Transmitter amplifier register
MFRC630_REG_DRVCON = 0x2A               # Driver configuration register
MFRC630_REG_TXL = 0x2B                  # Transmitter register
MFRC630_REG_TXCRCPRESET = 0x2C          # Transmitter CRC control register
MFRC630_REG_RXCRCCON = 0x2D             # Receiver CRC control register
MFRC630_REG_TXDATANUM = 0x2E            # Transmitter data number register
MFRC630_REG_TXMODWIDTH = 0x2F           # Transmitter modulation width register
MFRC630_REG_TXSYM10BURSTLEN = 0x30      # Transmitter symbol 1 and 0 burst length register
MFRC630_REG_TXWAITCTRL = 0x31           # Transmitter wait control register
MFRC630_REG_TXWAITLO = 0x32             # Transmitter wait low register
MFRC630_REG_FRAMECON = 0x33             # Frame control register
MFRC630_REG_RXSOFD = 0x34               # Start of frame delimiter register
MFRC630_REG_RXCTRL = 0x35               # Receiver control register
MFRC630_REG_RXWAIT = 0x36               # Receiver wait register
MFRC630_REG_RXTHRESHOLD = 0x37          # Receiver threshold register
MFRC630_REG_RCV = 0x38                  # Receiver register
MFRC630_REG_RXANA = 0x39                # Receiver analog register
MFRC630_REG_RFU = 0x3A                  # Reserved for future use
MFRC630_REG_SERIALSPEED = 0x3B          # Serial speed register
MFRC630_REG_LFO_TRIMM = 0x3C            # Low-power oscillator trimm register   
MFRC630_REG_PLL_CTRL = 0x3D             # PLL control register
MFRC630_REG_PLL_DIVOUT = 0x3E           # PLL divider output register
MFRC630_REG_LPCD_QMIN = 0x3F            # Low-power card detection Qmin register
MFRC630_REG_LPCD_QMAX = 0x40            # Low-power card detection Qmax register
MFRC630_REG_LPCD_IMIN = 0x41            # Low-power card detection Imin register
MFRC630_REG_LPCD_I_RESULT = 0x42        # Low-power card detection I result register
MFRC630_REG_LPCD_Q_RESULT = 0x43        # Low-power card detection Q result register
MFRC630_REG_PADEN = 0x44                # PIN enable register
MFRC630_REG_PADOUT = 0x45               # PIN out register
MFRC630_REG_PADIN = 0x46                # PIN in register
MFRC630_REG_SIGOUT = 0x47               # Enables and controls the signal out pin
MFRC630_REG_VERSION = 0x7F              # Contains the product number and the version of the MFRC630

# MFRC630 Commands
MFRC630_CMD_IDLE = 0x00             # No action; cancels current command execution 
MFRC630_CMD_LPCD = 0x01             # Low-power card detection
MFRC630_CMD_LOADKEY = 0x02          # Reads a key from the FIFO buffer
MFRC630_CMD_MFAUTHENT = 0x03        # Performs the MIFARE standard authentication as a reader
MFRC630_CMD_RECEIVE = 0x05          # Activates the receiver circuits
MFRC630_CMD_TRANSMIT = 0x06         # Transmits data from the FIFO buffer
MFRC630_CMD_TRANSCEIVE = 0x07       # Transmits data from the FIFO buffer and automatically activates the receiver after transmission
MFRC630_CMD_WRITEE2 = 0x08          # Writes a byte of data to the EEPROM
MFRC630_CMD_WRITEE2PAGE = 0x09      # Writes a page of data to the EEPROM
MFRC630_CMD_READE2 = 0x0A           # Reads a byte of data from the EEPROM
MFRC630_CMD_LOADREG = 0x0C          # Reads a register from the FIFO buffer
MFRC630_CMD_LOADPROTOCOL = 0x0D     # Reads the protocol settings from the EEPROM
MFRC630_CMD_LOADKEYE2 = 0x0E        # Copies a key from the EEPROM into the key buffer
MFRC630_CMD_STOREKEYE2 = 0x0F       # Stores a key in the EEPROM
MFRC630_CMD_READRNR = 0x1C          # Copies the random number generator to the FIFO buffer
MFRC630_CMD_SOFTRESET = 0x1F        # Resets the MFRC630

# MFRC630 REGISTER STATUS
MFRC630_STATUS_STATE_IDLE = 0b000           # The MFRC630 is in idle state
MFRC630_STATUS_STATE_TXWAIT = 0b001         # The MFRC630 is waiting for data to transmit
MFRC630_STATUS_STATE_TRANSMITTING = 0b011   # The MFRC630 is transmitting data
MFRC630_STATUS_STATE_RXWAIT = 0b101         # The MFRC630 is waiting for data to receive
MFRC630_STATUS_STATE_WAIT_FOR_DATA = 0b110  # The MFRC630 is waiting for data
MFRC630_STATUS_STATE_RECEIVING = 0b111      # The MFRC630 is receiving data
MFRC630_STATUS_STATE_NOT_USED = 0b100       # The MFRC630 is not used
MFRC630_STATUS_CRYPTO1_ON = (1 << 5)        # Crypto1 is enabled

# MFRC630 TIMER CONTROL
MFRC630_TCONTROL_STOPRX = (1 << 7)                  # Stops the receiver
MFRC630_TCONTROL_START_NOT = (0b00<<4)              # Do not start automatically
MFRC630_TCONTROL_START_TX_END = (0b01<<4)           # Start automatically end of transmission
MFRC630_TCONTROL_START_LFO_WO = (0b10<<4)           # Timer is used for LFO trimming without underflow
MFRC630_TCONTROL_START_LFO_W = (0b11<<4)            # Timer is used for LFO trimming with underflow
MFRC630_TCONTROL_AUTO_RESTART = (0B1 << 3)          # Automatically restart  from the reload value when an underflow is reached
MFRC630_TCONTROL_CLK_13MHZ = (0b00)                 # 13.56 MHz
MFRC630_TCONTROL_CLK_211KHZ = (0b01)                # 211 kHz
MFRC630_TCONTROL_CLK_UF_TA1 = (0b10)                # Underflow TA1
MFRC630_TCONTROL_CLK_UF_TA2 = (0b11)                # Underflow TA2

# MFRC630 IRQ0 REGISTER FIELDS
MFRC630_IRQ0_SET = (1 << 7)                         # Set bit
MFRC630_IRQ0_HIALERT_IRQ = (1 << 6)                 # High alert
MFRC630_IRQ0_LOALERT_IRQ = (1 << 5)                 # Low alert
MFRC630_IRQ0_IDLE_IRQ = (1 << 4)                    # Idle
MFRC630_IRQ0_TX_IRQ = (1 << 3)                      # Transmit
MFRC630_IRQ0_RX_IRQ = (1 << 2)                      # Receive
MFRC630_IRQ0_ERR_IRQ = (1 << 1)                     # Error
MFRC630_IRQ0_RXSOF_IRQ = (1 << 0)                   # Start of frame

# MFRC630 IRQ1 REGISTER FIELDS
MFRC630_IRQ1_SET = (1 << 7)                         # Set bit
MFRC630_IRQ1_GLOBAL_IRQ = (1 << 6)                  # Global IRQ
MFRC630_IRQ1_LPCD_IRQ = (1 << 5)                    # Low-power card detection
MFRC630_IRQ1_TIMER4_IRQ = (1 << 4)                  # Timer 4
MFRC630_IRQ1_TIMER3_IRQ = (1 << 3)                  # Timer 3
MFRC630_IRQ1_TIMER2_IRQ = (1 << 2)                  # Timer 2
MFRC630_IRQ1_TIMER1_IRQ = (1 << 1)                  # Timer 1
MFRC630_IRQ1_TIMER0_IRQ = (1 << 0)                  # Timer 0

# MFRC630 IRQ0EN REGISTER FIELDS
# If set, the signal on the IRQ pin is inverted
MFRC630_IRQ0EN_IRQ_INV = (1 << 7)                   # Invert IRQ
MFRC630_IRQ0EN_HIALERT_IRQEN = (1 << 6)             # High alert
MFRC630_IRQ0EN_LOALERT_IRQEN = (1 << 5)             # Low alert
MFRC630_IRQ0EN_IDLE_IRQEN = (1 << 4)                # Idle
MFRC630_IRQ0EN_TX_IRQEN = (1 << 3)                  # Transmit
MFRC630_IRQ0EN_RX_IRQEN = (1 << 2)                  # Receive
MFRC630_IRQ0EN_ERR_IRQEN = (1 << 1)                 # Error
MFRC630_IRQ0EN_RXSOF_IRQEN = (1 << 0)               # Start of frame

# MFRC630 IRQ1EN REGISTER FIELDS
MFRC630_IRQ1EN_IRQ_PP = (1 << 7)                    # Set to 1 Push-pull otherwise open-drain
MFRC630_IRQ1EN_IRQ_PINEN = (1 << 6)                 # Global IRQ
MFRC630_IRQ1EN_LPCD_IRQEN = (1 << 5)                # Low-power card detection
MFRC630_IRQ1EN_TIMER4_IRQEN = (1 << 4)              # Timer 4
MFRC630_IRQ1EN_TIMER3_IRQEN = (1 << 3)              # Timer 3
MFRC630_IRQ1EN_TIMER2_IRQEN = (1 << 2)              # Timer 2
MFRC630_IRQ1EN_TIMER1_IRQEN = (1 << 1)              # Timer 1
MFRC630_IRQ1EN_TIMER0_IRQEN = (1 << 0)              # Timer 0

# MFRC630 ERROR REGISTER FIELDS
MFRC630_ERROR_EE_ERR = (1 << 7)                     # EEPROM error
MFRC630_ERROR_FIFOWRERR = (1 << 6)                  # FIFO write error
MFRC630_ERROR_FIFOOVL = (1 << 5)                    # FIFO overflow
MFRC630_ERROR_MINFRAMEERR = (1 << 4)                # Minimum frame error
MFRC630_ERROR_NODATAERR = (1 << 3)                  # No data error
MFRC630_ERROR_COLLDET = (1 << 2)                    # Collision error
MFRC630_ERROR_PROTERR = (1 << 1)                    # Protocol error
MFRC630_ERROR_INTEGERR = (1 << 0)                   # Integrity error

# CRC Register
MFRC630_CRC_ON = 1                         # Enable CRC
MFRC630_CRC_OFF = 0                        # Disable CRC

# MFRC630 TX DATANUM REGISTER
MFRC630_TXDATANUM_DATAEN = (1 << 3)           # If set, data is sent, if cleared it is possible to send a single symbol pattern.

# PROTOCOL NUMBERS
MFRC630_PROTO_ISO14443A_106_MILLER_MANCHESTER = 0
MFRC630_PROTO_ISO14443A_212_MILLER_BPSK = 1
MFRC630_PROTO_ISO14443A_424_MILLER_BPSK = 2
MFRC630_PROTO_ISO14443A_848_MILLER_BPSK = 3
MFRC630_PROTO_ISO14443B_106_NRZ_BPSK = 4
MFRC630_PROTO_ISO14443B_212_NRZ_BPSK = 5
MFRC630_PROTO_ISO14443B_424_NRZ_BPSK = 6
MFRC630_PROTO_ISO14443B_848_NRZ_BPSK = 7
MFRC630_PROTO_FELICA_212_MANCHESTER_MANCHESTER = 8
MFRC630_PROTO_FELICA_424_MANCHESTER_MANCHESTER = 9
MFRC630_PROTO_ISO15693_1OF4_SSC = 10
MFRC630_PROTO_ISO15693_1OF4_DSC = 11
MFRC630_PROTO_ISO15693_1OF256_SSC = 12
MFRC630_PROTO_EPC_UID_UNITRAY_SSC = 13
MFRC630_PROTO_ISO18000_MODE3 = 14

# RECOMMENDED VALUES
MFRC630_RECOM_14443A_CRC = 0x18
MFRC630_RECOM_14443A_ID1_106 = [ 0x8A, 0x08, 0x21, 0x1A, 0x18, 0x18, 0x0F, 0x27, 
                                0x00, 0xC0, 0x12, 0xCF, 0x00, 0x04, 0x90, 0x32, 
                                0x12, 0x0A]
MFRC630_RECOM_14443A_ID1_212 = [ 0x8E, 0x12, 0x11, 0x06, 0x18, 0x18, 0x0F, 0x10,
                                0x00, 0xC0, 0x12, 0xCF, 0x00, 0x05, 0x90, 0x3F,
                                0x12, 0x02]
MFRC630_RECOM_14443A_ID1_424 = [ 0x8E, 0x12, 0x11, 0x06, 0x18, 0x18, 0x0F, 0x08,
                                0x00, 0xC0, 0x12, 0xCF, 0x00, 0x06, 0x90, 0x3F,
                                0x12, 0x0A]
MFRC630_RECOM_14443A_ID1_848 = [ 0x8F, 0xDB, 0x11, 0x06, 0x18, 0x18, 0x0F, 0x02,
                                0x00, 0xC0, 0x12, 0xCF, 0x00, 0x07, 0x90, 0x3F,
                                0x12, 0x02]

# ISO14443A
MFRC630_ISO14443A_CMD_REQA = 0x26           # Request command
MFRC630_ISO14443A_CMD_WUPA = 0x52           # Wake-up command
MFRC630_ISO14443A_CAS_LEVEL_1 = 0x93        # Select cascade level 1
MFRC630_ISO14443A_CAS_LEVEL_2 = 0x95        # Select cascade level 2
MFRC630_ISO14443A_CAS_LEVEL_3 = 0x97        # Select cascade level 3

# MIFARE
MFRC630_MF_AUTH_KEY_A = 0x60            # Authenticate key A
MFRC630_MF_AUTH_KEY_B = 0x61            # Authenticate key B
MFRC630_MF_CMD_READ = 0x30              # Read command
MFRC630_MF_CMD_WRITE = 0xA0             # Write command
MFRC630_MF_ACK = 0x0A                   # Acknowledge









