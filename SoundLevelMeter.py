import serial
import struct

#import matplotlib
#matplotlib.use('QtAgg') 

import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

VERBOSE = True
PLOT = True

#ser = serial.Serial('/dev/ttyUSB0')
ser = serial.Serial('COM7')
ser.reset_input_buffer()

dateTimeObj = datetime.now()
plot_window = 10 * 60 # one hour window
if PLOT:    
    x_var = np.array([dateTimeObj - timedelta(seconds=i) for i in range(plot_window)], dtype='datetime64')
    x_var = np.flip(x_var)
    y_var1 = np.array(np.zeros([plot_window]))
    plt.ion()
    fig, ax = plt.subplots()
    line1, = ax.plot(x_var, y_var1, label="Sound Level [dB]")
    #ax.legend()
    #ax.minorticks_on()
    #ax.grid(True, which='major', linestyle='-')
    #ax.grid(True, which='minor', linestyle='--', alpha=0.4)

# open output file
timestampStr = dateTimeObj.strftime("%d-%b-%Y_%H%M%S_%f")
data_file = 'data_' + timestampStr + '.csv'
print(f"Writing to file {data_file}")
with open(data_file, 'w') as fih:
    # write header
    fih.write("TIME,SOUNDLEVEL\n")

    try:
        while True:
            # read from sensor
            ser.reset_input_buffer()
            ser_values = ser.readline()

            # get current time and encode as string
            dateTimeObj = datetime.now()
            timestampStr = dateTimeObj.strftime("%d-%b-%Y %H:%M:%S.%f")

            # parse data received from sensor
            try:
                value = float(ser_values) * 100
            except:
                continue
                
            if value > 180 or value == 0:
                continue

            # write to file
            fih.write(f"{timestampStr},{value}\n")
            fih.flush()

            if VERBOSE:
                print("")
                print(timestampStr)
                print(f'{value}')

                if PLOT:
                    x_var = np.append(x_var, dateTimeObj)
                    x_var = x_var[1:plot_window+1]

                    y_var1 = np.append(y_var1, value)
                    y_var1 = y_var1[1:plot_window+1]

                    line1.set_xdata(x_var)
                    line1.set_ydata(y_var1)

                    ax.relim()
                    ax.autoscale_view()

                    fig.canvas.draw()
                    fig.canvas.flush_events()

    except KeyboardInterrupt:
        pass      