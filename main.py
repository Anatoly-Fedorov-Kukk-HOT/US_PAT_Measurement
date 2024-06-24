import socket
import time
from pylablib.devices import Thorlabs
from time import sleep
import logging 
from datetime import datetime
from termcolor import colored

# Constants
N = 30  # Must be an even number, matching buffersize in the Verasonics script file
STEP_SIZE = 200  # in micrometers, try to avoid going over 8 mm in total range (N*STEP_SIZE)
WAVELENGTH = [430, 530, 630]  # len(WAVELENGTH) must match PA frames in the Verasonics script
DELAY = 1.2  # in seconds, range 1.0 - 2.5 useful
SIGN = 1  # direction of motion, 1 for towards the fiber bundle, -1 for backwards
SIGN /= abs(SIGN)  # Ensure SIGN is ±1

# Safety check for total range
if N * STEP_SIZE > 8500:
    raise RuntimeError("Distance over 8.5 mm, abort to avoid collisions")

# Logging setup
filename_today = datetime.today().strftime('%Y-%m-%d') + '.log'
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', 
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=filename_today,
                    level=logging.DEBUG)

logging.info('=== start ===')

# Stage connection
if 'stage' not in locals():
    stage = Thorlabs.KinesisMotor("27259352", scale="MTS25-Z8")  # Connect to the stage
    print('Stage connected!')

units = stage.get_scale_units()
print(f'Units are {units}.')

# Check stage homing status
if stage.is_homed():
    print('Stage is homed!')
else:
    print('Stage is not homed!')

# Get and print current position
if units == 'm':
    pos = 1000 * stage.get_position()
    print(f'Position is {pos} mm.')
else:
    pos = stage.get_position()
    print(f'Position is {pos} {units}.')

print(colored('Camera photo taken?', 'green'))

# Log initial parameters
logging.info(f'n_steps: {N}, stepsize(1E-6m): {STEP_SIZE}, delay(s): {DELAY}, wavelength(nm): {WAVELENGTH}')
if any(w > 532 for w in WAVELENGTH):
    print(colored('Wavelength above 532 nm used! Correct safety goggles?', 'red'))

print('Shutter?')

# Move stage to starting position
stage.move_to(0E-3)
sleep(1)
start_pos = stage.get_position()
logging.info(f'Starting position(m):{start_pos:2.5f}')

print('Shutter?')

# OPO connection
IP = "192.168.12.223"
PORT = 1025  # Remote client port

if 'client' not in locals():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket created')
    except socket.error as e:
        print(f'Failed to create socket: {e}')
        sys.exit()
    client.connect((IP, PORT))
    print('Connected to the laser!')

# Configure OPO settings
def send_msg(msg):
    client.send(msg.encode('ascii'))
    print(msg.strip())

send_msg(f'SET_WAVELENGTH={WAVELENGTH[0]}\r\n')
send_msg('SET_POCKELSCELL_SHOT_MODE=2\r\n')
send_msg('SET_MULTISHOT_COUNT=4\r\n')
send_msg('FLASHLAMP_ON\r\n')
sleep(0.5)
send_msg('SET_SHUTTER_STATE=OPEN\r\n')

# Initial delay
for i in range(4):
    print(i)
    sleep(1)

logging.info('Start of measurement')

# Measurement loop
for i in range(N):
    target_pos = start_pos + SIGN * i * STEP_SIZE * 1e-6
    stage.move_to(target_pos)
    pos = stage.get_position() * 1e6
    print(f'\n({i+1}/{N}) Moved to {pos:.2f} micrometers!')
    sleep(DELAY)
    
    if len(WAVELENGTH) > 1:
        for wl in WAVELENGTH:
            send_msg(f'SET_WAVELENGTH={wl}\r\n')
            sleep(0.2)
            send_msg('START_MULTISHOT\r\n')
            sleep(0.2)
    else:
        send_msg('START_MULTISHOT\r\n')
        sleep(DELAY)

print('Done!')
sleep(DELAY)
send_msg('SET_SHUTTER_STATE=CLOSE\r\n')
sleep(0.2)
send_msg('FLASHLAMP_OFF\r\n')
logging.info('end of measurement')

# Return stage to initial position
stage.move_to(0E-3)
while stage.is_moving():
    sleep(0.2)
pos = stage.get_position() * 1e6
print(f'Moved back to {pos:.2f} micrometers!')

logging.info('=== end ===\n')
