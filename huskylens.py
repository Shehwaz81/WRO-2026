
### Setup pupremote code
from pupremote import  PUPRemoteSensor, SPIKE_ULTRASONIC
from time import ticks_ms, sleep_ms
from pyhuskylens import HuskyLens
from machine import SoftI2C, Pin

# Connect huskylens to LMS-ESP32 like this: 
# 5V (red line)
# GND (black line)
# IO2 (blue line)
# IO26 (green line)

# Initialize i2c. Timeout is 2000 microseconds, because PUPremote balks if a
# function hangs much longer.
i2c = SoftI2C(scl=Pin(2), sda=Pin(26), timeout=2000)

hlens = HuskyLens(i2c)

def hl(*argv):
    global hlens
    if argv:
        # Pybricks tries to set a mode. Let's pass it on with set_alg()
        if not hlens.set_alg(argv[0]):
            # There was a problem setting the mode. Return id -1
            return (0,0,0,0,-1)
            
    else:
        # No mode asked, just get identified blocks.
        blocks = hlens.get_blocks()
        if blocks and len(blocks) == 12:
            ypos = []
            for block in blocks 
                ypos.append([block.y, block.x, block.ID]) # store y position and then block ID

            ypos = sorted(ypos, key=lambda y: y[0], reverse=True)

            grid=[]
            # add the rows to the grid (not sorted by x pos)
            for i in range(3):
                start_idx = i * 4
                row = []
                for j in range(4):
                    idx = start_idx + j
                    row.append((ypos[idx][1], ypos[idx][2]))
                grid.append(row)
                
            # sort code by x pos
            for i in range(3):
                grid[i] = sorted(grid[i], key=lambda x : x[0]) # sort by x in acending order
           
           flat_grid = []
           for row in grid:
               for x, color in rows:
                   flat_grid.append(color)

            return tuple(flat_grid)

        else:
            # No blocks found, return all zeroes.
            return tuple(0,) * 12

p=PUPRemoteSensor(sensor_id=SPIKE_ULTRASONIC, power=False)
p.add_command('hl',from_hub_fmt="b", to_hub_fmt="BBBBBBBBBBBB")
### End of pupremote setup code

### Main loop
while(True):
    connected=p.process()

