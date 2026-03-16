from machine import Pin, I2C
import time

# ESP32 I2C pins
SCL_PIN = 32
SDA_PIN = 33

# Hiwonder 8-ch Line Follower I2C address
SENSOR_ADDR = 0x5D

# Registers
REG_STATE = 5
REG_ANALOG_START = 6
REG_THRESH_START = 22

# Init I2C
i2c = I2C(0, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN), freq=400000)

def read_u8(reg):
    data = i2c.readfrom_mem(SENSOR_ADDR, reg, 1)
    return data[0]

def read_u16_le(reg):
    data = i2c.readfrom_mem(SENSOR_ADDR, reg, 2)
    return data[0] | (data[1] << 8)

def get_digital_states():
    state_byte = read_u8(REG_STATE)
    states = []
    for ch in range(8):
        states.append((state_byte >> ch) & 0x01)
    return state_byte, states

def get_analog_values():
    values = []
    for ch in range(8):
        reg = REG_ANALOG_START + ch * 2
        values.append(read_u16_le(reg))
    return values

def get_threshold_values():
    values = []
    for ch in range(8):
        reg = REG_THRESH_START + ch * 2
        values.append(read_u16_le(reg))
    return values

# Check sensor
devices = i2c.scan()
print("I2C devices found:", [hex(d) for d in devices])

if SENSOR_ADDR not in devices:
    print("Sensor 0x5D not found. Check wiring and power.")
else:
    print("Hiwonder 8CH line follower detected at", hex(SENSOR_ADDR))

    while True:
        try:
            state_byte, states = get_digital_states()
            analogs = get_analog_values()
            thresholds = get_threshold_values()

            binary_str = bin(state_byte)[2:]
            binary_str = "0" * (8 - len(binary_str)) + binary_str

            print("----------------------------------------")
            print("Digital byte:", state_byte, " binary:", binary_str)
            print("Digital states CH1->CH8:", states)
            print("Analog values  CH1->CH8:", analogs)
            print("Thresholds     CH1->CH8:", thresholds)

        except Exception as e:
            print("Read error:", e)

        time.sleep(0.2)
