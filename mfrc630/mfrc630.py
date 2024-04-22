from mfrc630.mfrc630_defines import *
import signal
import time

# Register interaction functions
def mfrc630_read_reg(reg):
    instruction_tx = [(reg << 1) | 0x01, 0]
    instruction_rx = [0, 0]
    mfrc630_SPI_select()
    mfrc630_SPI_transfer(instruction_tx, instruction_rx,2)
    mfrc630_SPI_unselect()
    return instruction_rx[1]

def mfrc630_write_reg(reg, value):
    instruction_tx = [(reg << 1) | 0x00, value]
    discard = [0, 0]
    mfrc630_SPI_select()
    mfrc630_SPI_transfer(instruction_tx, discard, 2)
    mfrc630_SPI_unselect()

def mfrc630_write_regs(reg, values, len):
    instruction_tx = bytearray([0] * (len + 1))
    discard = bytearray([0] * (len+1))
    instruction_tx[0] = (reg << 1) | 0x00
    for i in range(len):
        instruction_tx[i+1] = values[i]
    mfrc630_SPI_select()
    mfrc630_SPI_transfer(instruction_tx, discard, len+1)
    mfrc630_SPI_unselect()

def mfrc630_write_fifo(data, len):
    write_instruction = bytearray([MFRC630_REG_FIFODATA << 1] | 0)
    discard = bytearray([0] * (len+1))
    mfrc630_SPI_select()
    mfrc630_SPI_transfer(write_instruction, discard, len)
    mfrc630_SPI_unselect()

def mfrc630_read_fifo(rx, len):
    read_instruction = bytearray([MFRC630_REG_FIFODATA << 1] | 0x01)
    discard = bytearray([0] * 2)
    mfrc630_SPI_select()
    mfrc630_SPI_transfer(read_instruction, rx, 1)
    for i in range(len):
        mfrc630_SPI_transfer(read_instruction, rx[i], 1)
    mfrc630_SPI_unselect()


# Command functions

def mfrc630_cmd_read_E2(address, lenght):
    parameters = [(address >> 1) & 0xFF, address & 0xFF, lenght & 0xFF]
    mfrc630_flush_fifo()
    mfrc630_write_fifo(parameters, 3)
    mfrc630_write_reg(MFRC630_REG_COMMAND, MFRC630_CMD_READE2)

def mfrc630_cmd_load_reg(address, regaddr, lenght):
    parameters = [(address >> 8) & 0xFF, address & 0xFF, regaddr & 0xFF, lenght & 0xFF]
    mfrc630_flush_fifo()
    mfrc630_write_fifo(parameters, 4)
    mfrc630_write_reg(MFRC630_REG_COMMAND, MFRC630_CMD_LOADREG)

def mfrc630_cmd_load_protocol(rx, tx):
    parameters = [rx & 0xFF, tx & 0xFF]
    mfrc630_flush_fifo()
    mfrc630_write_fifo(parameters, 2)
    mfrc630_write_reg(MFRC630_REG_COMMAND, MFRC630_CMD_LOADPROTOCOL)

def mfrc630_cmd_transceive(data, length):
    mfrc630_cmd_idle()
    mfrc630_flush_fifo()
    mfrc630_write_fifo(data, length)
    mfrc630_write_reg(MFRC630_REG_COMMAND, MFRC630_CMD_TRANSCEIVE)

def mfrc630_cmd_idle():
    mfrc630_write_reg(MFRC630_REG_COMMAND, MFRC630_CMD_IDLE)

def mfrc630_cmd_load_key_E2(key_nr):
    parameters = [key_nr & 0xFF]
    mfrc630_flush_fifo()
    mfrc630_write_fifo(parameters, 1)
    mfrc630_write_reg(MFRC630_REG_COMMAND, MFRC630_CMD_LOADKEYE2)

def mfrc630_cmd_auth(key_type, block_address, card_uid):
    mfrc630_cmd_idle()
    parameters = [key_type & 0xFF, block_address & 0xFF] + [uid & 0xFF for uid in card_uid[:4]]
    mfrc630_flush_fifo()
    mfrc630_write_fifo(parameters, 6)
    mfrc630_write_reg(MFRC630_REG_COMMAND, MFRC630_CMD_MFAUTHENT)

def mfrc630_cmd_load_key(key):
    mfrc630_cmd_idle()
    mfrc630_flush_fifo()
    mfrc630_write_fifo(key[:6], 6)
    mfrc630_write_reg(MFRC630_REG_COMMAND, MFRC630_CMD_LOADKEY)


# Utility functions

def mfrc630_flush_fifo():
    mfrc630_write_reg(MFRC630_REG_FIFOCONTROL, 1 << 4)

def mfrc630_fifo_length():
    return mfrc630_read_reg(MFRC630_REG_FIFOLENGTH)

def mfrc630_clear_irq0():
    mfrc630_write_reg(MFRC630_REG_IRQ0, ~(1 << 7) & 0xFF)

def mfrc630_clear_irq1():
    mfrc630_write_reg(MFRC630_REG_IRQ1, ~(1 << 7) & 0xFF)

def mfrc630_irq0():
    return mfrc630_read_reg(MFRC630_REG_IRQ0)

def mfrc630_irq1():
    return mfrc630_read_reg(MFRC630_REG_IRQ1)

def mfrc630_transfer_E2_page(dest, page):
    mfrc630_cmd_read_E2(page * 64, 64)
    res = mfrc630_fifo_length()
    mfrc630_read_fifo(dest, 64)
    return res

def mfrc630_print_block(data, len):
    for i in range(len):
        print(f"{data[i]:02X} ", end="")
    print() 


# Timer functions

def mfrc630_activate_timer(timer, active):
    mfrc630_write_reg(MFRC630_REG_TCONTROL, ((active << timer) << 4) | (1 << timer))

def mfrc630_timer_set_control(timer, value):
    mfrc630_write_reg(MFRC630_REG_T0CONTROL + (5 * timer), value)

def mfrc630_timer_set_reload(timer, value):
    mfrc630_write_reg(MFRC630_REG_T0RELOADHI + (5 * timer), (value >> 8) & 0xFF)
    mfrc630_write_reg(MFRC630_REG_T0RELOADLO + (5 * timer), value & 0xFF)

def mfrc630_timer_set_value(timer, value):
    mfrc630_write_reg(MFRC630_REG_T0COUNTERVALHI + (5 * timer), (value >> 8) & 0xFF)
    mfrc630_write_reg(MFRC630_REG_T0COUNTERVALLO + (5 * timer), value & 0xFF)

def mfrc630_timer_get_value(timer):
    value_hi = mfrc630_read_reg(MFRC630_REG_T0COUNTERVALHI + (5 * timer))
    value_lo = mfrc630_read_reg(MFRC630_REG_T0COUNTERVALLO + (5 * timer))
    return (value_hi << 8) + value_lo
             

# AN11145 functions

def mfrc630_AN11145_start_IQ_measurement():
    # Configurar el modo LPCD
    mfrc630_write_reg(0, 0x1F)  # Resetear CLRC663 y pasar a estado de inactividad
    # Esperar 50ms (puede omitirse en Python)
    mfrc630_write_reg(0, 0)  # Volver a 0 para finalizar el reset
    # Deshabilitar fuentes de interrupción IRQ0 y IRQ1
    mfrc630_write_reg(0x06, 0x7F)
    mfrc630_write_reg(0x07, 0x7F)
    mfrc630_write_reg(0x08, 0x00)
    mfrc630_write_reg(0x09, 0x00)
    mfrc630_write_reg(0x02, 0xB0)  # Vaciar el FIFO
    # Configuración LPCD
    mfrc630_write_reg(0x3F, 0xC0)  # Establecer registro Qmin
    mfrc630_write_reg(0x40, 0xFF)  # Establecer registro Qmax
    mfrc630_write_reg(0x41, 0xC0)  # Establecer registro Imin
    mfrc630_write_reg(0x28, 0x89)  # Establecer registro DrvMode
    # Ejecutar procedimiento de ajuste
    mfrc630_write_reg(0x1F, 0x00)  # Escribir valor de recarga T3 predeterminado alto
    mfrc630_write_reg(0x20, 0x10)  # Escribir valor de recarga T3 predeterminado bajo
    mfrc630_write_reg(0x24, 0x00)  # Escribir valor de recarga T4 mínimo alto
    mfrc630_write_reg(0x25, 0x05)  # Escribir valor de recarga T4 mínimo bajo
    mfrc630_write_reg(0x23, 0xF8)  # Configurar T4 para AutoLPCD&AutoRestart. Iniciar T4.
    mfrc630_write_reg(0x43, 0x40)  # Borrar resultado LPCD
    mfrc630_write_reg(0x38, 0x52)  # Establecer bit Rx_ADCmode
    mfrc630_write_reg(0x39, 0x03)  # Aumentar ganancia del receptor al máximo
    mfrc630_write_reg(0x00, 0x01)  # Ejecutar comando "Auto_T4" de Rc663 (detección de tarjeta de baja potencia y/o ajuste automático)

def mfrc630_AN11145_stop_IQ_measurement():
    mfrc630_write_reg(0x00, 0x00)  # Limpiar cmd y FIFO
    mfrc630_write_reg(0x02, 0xB0)
    mfrc630_write_reg(0x38, 0x12)  # Limpiar bit Rx_ADCmode

def mfrc630_AN1102_recommended_registers_skip(protocol, skip):
    if protocol == MFRC630_PROTO_ISO14443A_106_MILLER_MANCHESTER:
        buf = MFRC630_RECOM_14443A_ID1_106
    elif protocol == MFRC630_PROTO_ISO14443A_212_MILLER_BPSK:
        buf = MFRC630_RECOM_14443A_ID1_212
    elif protocol == MFRC630_PROTO_ISO14443A_424_MILLER_BPSK:
        buf = MFRC630_RECOM_14443A_ID1_424
    elif protocol == MFRC630_PROTO_ISO14443A_848_MILLER_BPSK:
        buf = MFRC630_RECOM_14443A_ID1_848
    else:
        return  # Protocolo no válido
    
    # Escribir en registros DRVMOD con desplazamiento
    mfrc630_write_regs(MFRC630_REG_DRVMOD + skip, buf[skip:], len(buf) - skip)

def mfrc630_AN1102_recommended_registers(protocol):
    mfrc630_AN1102_recommended_registers_skip(protocol, 0)

def mfrc630_AN1102_recommended_registers_no_transmitter(protocol):
    mfrc630_AN1102_recommended_registers_skip(protocol, 5)


# ISO 14443A 

def mfrc630_ISO14443A_REQA():
    return mfrc630_iso14443a_WUPA_REQA(MFRC630_ISO14443A_CMD_REQA)

def mfrc630_ISO14443A_WUPA():
    return mfrc630_iso14443a_WUPA_REQA(MFRC630_ISO14443A_CMD_WUPA)

def mfrc630_iso14443a_WUPA_REQA(instruction):
    mfrc630_cmd_idle()
    mfrc630_flush_fifo()

    mfrc630_write_reg(MFRC630_REG_TXDATANUM, 7 | MFRC630_TXDATANUM_DATAEN)
    mfrc630_write_reg(MFRC630_REG_TXCRCPRESET, MFRC630_RECOM_14443A_CRC | MFRC630_CRC_OFF)
    mfrc630_write_reg(MFRC630_REG_RXCRCCON, MFRC630_RECOM_14443A_CRC | MFRC630_CRC_OFF)
    mfrc630_write_reg(MFRC630_REG_RXBITCTRL, 0)

    send_req = [instruction]

    mfrc630_clear_irq0()
    mfrc630_clear_irq1()
    mfrc630_write_reg(MFRC630_REG_IRQ0EN, MFRC630_IRQ0EN_RX_IRQEN | MFRC630_IRQ0EN_ERR_IRQEN)
    mfrc630_write_reg(MFRC630_REG_IRQ1EN, MFRC630_IRQ1EN_TIMER0_IRQEN)

    timer_for_timeout = 0
    mfrc630_timer_set_control(timer_for_timeout, MFRC630_TCONTROL_CLK_211KHZ | MFRC630_TCONTROL_START_TX_END)
    mfrc630_timer_set_reload(timer_for_timeout, 1000)
    mfrc630_timer_set_value(timer_for_timeout, 1000)

    mfrc630_cmd_transceive(send_req, 1)

    irq1_value = 0
    while not (irq1_value & (1 << timer_for_timeout)):
        irq1_value = mfrc630_irq1()
        if irq1_value & MFRC630_IRQ1_GLOBAL_IRQ:
            break

    mfrc630_cmd_idle()

    irq0 = mfrc630_irq0()
    if not (irq0 & MFRC630_IRQ0_RX_IRQ) or (irq0 & MFRC630_IRQ0_ERR_IRQ):
        return 0

    rx_len = mfrc630_fifo_length()
    res = 0
    if rx_len == 2:
        res = mfrc630_read_fifo(rx_len)
    return res

def mfrc630_iso14443a_select(uid, sak):
    mfrc630_cmd_idle()
    mfrc630_flush_fifo()

    mfrc630_write_reg(MFRC630_REG_IRQ0EN, MFRC630_IRQ0EN_RX_IRQEN | MFRC630_IRQ0EN_ERR_IRQEN)
    mfrc630_write_reg(MFRC630_REG_IRQ1EN, MFRC630_IRQ1EN_TIMER0_IRQEN)

    timer_for_timeout = 0
    mfrc630_timer_set_control(timer_for_timeout, MFRC630_TCONTROL_CLK_211KHZ | MFRC630_TCONTROL_START_TX_END)
    mfrc630_timer_set_reload(timer_for_timeout, 1000)
    mfrc630_timer_set_value(timer_for_timeout, 1000)

    cascade_level = 1
    while cascade_level <= 3:
        cmd = 0
        known_bits = 0
        send_req = [0] * 7
        uid_this_level = send_req[2:]

        if cascade_level == 1:
            cmd = MFRC630_ISO14443A_CAS_LEVEL_1
        elif cascade_level == 2:
            cmd = MFRC630_ISO14443A_CAS_LEVEL_2
        elif cascade_level == 3:
            cmd = MFRC630_ISO14443A_CAS_LEVEL_3

        mfrc630_write_reg(MFRC630_REG_TXCRCPRESET, MFRC630_RECOM_14443A_CRC | MFRC630_CRC_OFF)
        mfrc630_write_reg(MFRC630_REG_RXCRCCON, MFRC630_RECOM_14443A_CRC | MFRC630_CRC_OFF)

        collision_n = 0
        while collision_n < 32:
            mfrc630_clear_irq0()
            mfrc630_clear_irq1()

            send_req[0] = cmd
            send_req[1] = 0x20 + known_bits

            message_length = (known_bits // 8) + 2

            mfrc630_write_reg(MFRC630_REG_TXDATANUM, (known_bits % 8) | MFRC630_TXDATANUM_DATAEN)
            rxalign = known_bits % 8
            mfrc630_write_reg(MFRC630_REG_RXBITCTRL, (0 << 7) | (rxalign << 4))

            mfrc630_cmd_transceive(send_req, message_length)

            irq1_value = 0
            while not (irq1_value & (1 << timer_for_timeout)):
                irq1_value = mfrc630_irq1()
                if irq1_value & MFRC630_IRQ1_GLOBAL_IRQ:
                    break

            mfrc630_cmd_idle()

            irq0 = mfrc630_irq0()
            error = mfrc630_read_reg(MFRC630_REG_ERROR)
            coll = mfrc630_read_reg(MFRC630_REG_RXCOLL)

            if irq0 & MFRC630_IRQ0_ERR_IRQ:
                if error & MFRC630_ERROR_COLLDET:
                    if coll & (1 << 7):
                        collision_pos = coll & (~(1 << 7))
                        choice_pos = known_bits + collision_pos
                        selection = (uid[choice_pos + (cascade_level - 1) * 3 // 8] >> ((choice_pos) % 8)) & 1

                        uid_this_level[choice_pos // 8] |= (selection << (choice_pos % 8))
                        known_bits = known_bits + 1
                    else:
                        collision_pos = 0x20 - known_bits
                else:
                    collision_pos = 0x20 - known_bits
            elif irq0 & MFRC630_IRQ0_RX_IRQ:
                collision_pos = 0x20 - known_bits
            else:
                # No response or card present
                return 0

            rx_len = mfrc630_fifo_length()
            buf = mfrc630_read_fifo(rx_len if rx_len < 5 else 5)

            for rbx in range(rx_len):
                uid_this_level[(known_bits // 8) + rbx] |= buf[rbx]
            known_bits += collision_pos

            if known_bits >= 32:
                break

        bcc_value = uid_this_level[4]
        bcc_calc = uid_this_level[0] ^ uid_this_level[1] ^ uid_this_level[2] ^ uid_this_level[3]
        
        if bcc_value != bcc_calc:
            return 0
        mfrc630_clear_irq0()
        mfrc630_clear_irq1()

        send_req[0] = cmd
        send_req[1] = 0x70
        #send_req[2, 3, 4, 5] contain the CT, UID[0-2] or UID[0-3]
        send_req[6] = bcc_calc
        message_length = 7

        mfrc630_write_reg(MFRC630_REG_TXCRCPRESET,MFRC630_RECOM_14443A_CRC | MFRC630_CRC_ON)
        mfrc630_write_reg(MFRC630_REG_RXCRCCON,MFRC630_RECOM_14443A_CRC | MFRC630_CRC_ON)

        mfrc630_write_reg(MFRC630_REG_TXDATANUM, (known_bits % 8) | MFRC630_TXDATANUM_DATAEN)
        rxalign = 0
        mfrc630_write_reg(MFRC630_REG_RXBITCTRL, (0 << 7) | (rxalign << 4))

        mfrc630_cmd_transceive(send_req, message_length)

        irq1_value = 0
        while not (irq1_value & (1 << timer_for_timeout)):
            irq1_value = mfrc630_irq1()
            if irq1_value & MFRC630_IRQ1_GLOBAL_IRQ:
                break
        
        mfrc630_cmd_idle()

        irq0_value = mfrc630_irq0()
        if irq0_value & MFRC630_IRQ0_ERR_IRQ:
            error = mfrc630_read_reg(MFRC630_REG_ERROR)
            if error & MFRC630_ERROR_COLLDET:
                  return 0
            
        sak_len = mfrc630_fifo_length()
        if sak_len != 1:
            return 0
        
        sak_value = bytearray(1)
        mfrc630_read_fifo(sak_value, sak_len)

        if sak_value[0] & (1 <<2):
            for UIDn in range(3):
                uid[(cascade_level - 1)*3 + UIDn] = uid_this_level[UIDn+1] 

        else:
            for UIDn in range(4):
                uid[(cascade_level - 1)*3 + UIDn] = uid_this_level[UIDn]

            sak[0] = sak_value[0]
            return cascade_level * 3 + 1

        return 0 
    
        
        collision_n += 1

        cascade_level += 1

    return 0


# MIFARE

def mfrc630_MF_auth(uid, key_type, block):
    # Simulación de configuración de interrupciones y temporizador
    timer_for_timeout = 0
    mfrc630_write_reg(MFRC630_REG_IRQ0EN, MFRC630_IRQ0EN_IDLE_IRQEN | MFRC630_IRQ0EN_ERR_IRQEN)
    mfrc630_write_reg(MFRC630_REG_IRQ1EN, MFRC630_IRQ1EN_TIMER0_IRQEN)       # Only trigger on timer for irq1  
    mfrc630_timer_set_control(timer_for_timeout, MFRC630_TCONTROL_CLK_211KHZ | MFRC630_TCONTROL_START_TX_END)
    mfrc630_timer_set_reload(timer_for_timeout, 2000)
    mfrc630_timer_set_value(timer_for_timeout, 2000)

    irq1_value = 0

    mfrc630_clear_irq0()
    mfrc630_clear_irq1()

    # Start the authentication process
    mfrc630_cmd_auth(key_type, block, uid)

    # Block until we are done
    while not (irq1_value & (1 << timer_for_timeout)):
        irq1_value = mfrc630_irq1()
        if irq1_value & MFRC630_IRQ1_GLOBAL_IRQ: 
            break # Stop polling irq1 and quit timeout loop
    
    if (irq1_value & (1 << timer_for_timeout)):
        print("Timeout occurred. Authentication failed.")
        return 0
    
    status = mfrc630_read_reg(MFRC630_REG_STATUS)
    return (status & MFRC630_STATUS_CRYPTO1_ON)

def mfrc630_MF_read_block(block_address, dest):

    mfrc630_flush_fifo()
    mfrc630_write_reg(MFRC630_REG_TXCRCPRESET, MFRC630_RECOM_14443A_CRC | MFRC630_CRC_ON)
    mfrc630_write_reg(MFRC630_REG_RXCRCCON, MFRC630_RECOM_14443A_CRC | MFRC630_CRC_ON)

    send_req = [MFRC630_MF_CMD_READ, block_address]

    timer_for_timeout = 0

    mfrc630_write_reg(MFRC630_REG_IRQ0EN, MFRC630_IRQ0EN_IDLE_IRQEN | MFRC630_IRQ0EN_ERR_IRQEN)
    mfrc630_write_reg(MFRC630_REG_IRQ1EN, MFRC630_IRQ1EN_TIMER0_IRQEN)

    mfrc630_timer_set_control(timer_for_timeout, MFRC630_TCONTROL_CLK_211KHZ | MFRC630_TCONTROL_START_TX_END)

    mfrc630_timer_set_reload(timer_for_timeout, 2000)
    mfrc630_timer_set_value(timer_for_timeout, 2000)

    irq1_value = 0
    irq0_value = 0

    mfrc630_clear_irq0()
    mfrc630_clear_irq1()

    mfrc630_cmd_transceive(send_req, 2)

    while not (irq1_value & (1 << timer_for_timeout)):
        irq1_value = mfrc630_irq1()
        if irq1_value & MFRC630_IRQ1_GLOBAL_IRQ:
            break

    mfrc630_cmd_idle()

    if irq1_value & (1 << timer_for_timeout):
        print("Timeout occurred. Reading failed.")
        return 0
    
    irq0 = mfrc630_irq0()
    if (irq0_value & MFRC630_IRQ0_ERR_IRQ):
        print("Error occurred during read.")
        return 0
    
    buffer_length = mfrc630_fifo_length()
    rx_len = buffer_length if buffer_length <= 16 else 16
    mfrc630_read_fifo(dest, rx_len)
    return rx_len

def mfrc630_MF_write_block(block_address, source):
    mfrc630_flush_fifo()

    mfrc630_write_reg(MFRC630_REG_TXCRCPRESET, MFRC630_RECOM_14443A_CRC | MFRC630_CRC_ON)
    mfrc630_write_reg(MFRC630_REG_RXCRCCON, MFRC630_RECOM_14443A_CRC | MFRC630_CRC_OFF)

    timer_for_timeout = 0

    mfrc630_write_reg(MFRC630_REG_IRQ0EN, MFRC630_IRQ0EN_IDLE_IRQEN | MFRC630_IRQ0EN_ERR_IRQEN)
    mfrc630_write_reg(MFRC630_REG_IRQ1EN, MFRC630_IRQ1EN_TIMER0_IRQEN)

    mfrc630_timer_set_control(timer_for_timeout, MFRC630_TCONTROL_CLK_211KHZ | MFRC630_TCONTROL_START_TX_END)

    mfrc630_timer_set_reload(timer_for_timeout, 2000)
    mfrc630_timer_set_value(timer_for_timeout, 2000)

    irq1_value = 0
    irq0_value = 0

    res = [0]

    send_req = [MFRC630_MF_CMD_WRITE, block_address]

    mfrc630_clear_irq0()
    mfrc630_clear_irq1()

    mfrc630_cmd_transceive(send_req, 2)

    while not (irq1_value & (1 << timer_for_timeout)):
        irq1_value = mfrc630_irq1()
        if irq1_value & MFRC630_IRQ1_GLOBAL_IRQ:
            break

    mfrc630_cmd_idle()

    if irq1_value & (1 << timer_for_timeout):
        print("Timeout occurred. Writing failed.")
        return 0
    
    irq0 = mfrc630_irq0()

    if (irq0_value & MFRC630_IRQ0_ERR_IRQ):
        print("Error occurred during write.")
        return 0
    
    buffer_length = mfrc630_fifo_length()

    if buffer_length != 1:
        print("Error occurred during write.")
        return 0
    
    mfrc630_read_fifo(res, 1)
        
    if res[0] != MFRC630_MF_ACK:
        print("Error occurred during write.")
        return 0
    
    mfrc630_clear_irq0()
    mfrc630_clear_irq1()

    # Go for the second stage
    mfrc630_cmd_transceive(source, 16)

    while not (irq1_value & (1 << timer_for_timeout)):
        irq1_value = mfrc630_irq1()
        if irq1_value & MFRC630_IRQ1_GLOBAL_IRQ:
            break

    mfrc630_cmd_idle()

    if irq1_value & (1 << timer_for_timeout):
        print("Timeout occurred. Writing failed.")
        return 0
    
    irq0_value = mfrc630_irq0()

    if (irq0_value & MFRC630_IRQ0_ERR_IRQ):
        print("Error occurred during write.")
        return 0
    
    buffer_length = mfrc630_fifo_length()

    if buffer_length != 1:
        print("Error occurred during write.")
        return 0    
    
    mfrc630_read_fifo(res, 1)

    if res[0] != MFRC630_MF_ACK:
        print("Error occurred during write.")
        return 16
        
    return 0

def mfrc630_MF_deauth():
    mfrc630_write_reg(MFRC630_REG_STATUS, 0)

def mfrc630_MF_example_dump():
    atqa = mfrc630_ISO14443A_REQA()
    if atqa != 0:
        sak = 0
        uid = [0] * 10
        uid_len = mfrc630_iso14443a_select(uid, sak)

        if uid_len != 0:
            print(f"UID of {uid_len} bytes (SAK: 0x{hex(sak)[2:]}): ", end="")
            mfrc630_print_block(uid, uid_len)
            print()
        
            FFkey = [0xFF] * 6
            mfrc630_cmd_load_key(FFkey)

            if mfrc630_MF_auth(uid, MFRC630_MF_AUTH_KEY_A, 0):
                print("Authentication successful")
                
                for b in range(4):
                    readbuf = [0] * 4
                    len = mfrc630_MF_read_block(b, readbuf)
                    print(f"Read block 0x{b:02X}: ", end="")
                    mfrc630_print_block(readbuf, len)
                    print()
                    
                mfrc630_MF_deauth()
            
            else:
                print("Authentication failed")
        else:
            print("Could not determine UID, perhaps the card is not a MIFARE card")
    else:
        print("No card detected")


    
    
    
    



