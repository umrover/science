from calendar import c
import serial
import numpy as np 
from scipy.interpolate import Rbf
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pynput.keyboard import Key, Listener
from datetime import datetime
import time

# IMPORTANT!!! Replace with the serial port the arduino is plugged into
ser = serial.Serial('COM12',115200)
logfile = 'log.txt'
figdir = 'science/spectral/images' # folder to save figures

channels = np.array([\
410, # A
435, # B
460, # C
485, # D
510, # E
535, # F
560, # G
585, # H
645, # I
705, # J
900, # K
940, # L
610, # R
680, # S
730, # T
760, # U
810, # V
860 # W
])

# calibration values, SUBJECT TO CHANGE 
raw_calib = "3495.30,1061.12,1924.57,690.48,929.63,1123.68,478.35,495.40,1473.11,249.47,362.42,71.99,99.08,77.44,226.75,477.91,148.85,80.99"
# This function is from https://www.noah.org/wiki/Wavelength_to_RGB_in_Python
def wavelength_to_rgb(wavelength, gamma=0.8):

    '''This converts a given wavelength of light to an 
    approximate RGB color value. The wavelength must be given
    in nanometers in the range from 380 nm through 750 nm
    (789 THz through 400 THz).

    Based on code by Dan Bruton
    http://www.physics.sfasu.edu/astro/color/spectra.html
    '''

    wavelength = float(wavelength)
    if wavelength >= 380 and wavelength <= 440:
        attenuation = 0.3 + 0.7 * (wavelength - 380) / (440 - 380)
        R = ((-(wavelength - 440) / (440 - 380)) * attenuation) ** gamma
        G = 0.0
        B = (1.0 * attenuation) ** gamma
    elif wavelength >= 440 and wavelength <= 490:
        R = 0.0
        G = ((wavelength - 440) / (490 - 440)) ** gamma
        B = 1.0
    elif wavelength >= 490 and wavelength <= 510:
        R = 0.0
        G = 1.0
        B = (-(wavelength - 510) / (510 - 490)) ** gamma
    elif wavelength >= 510 and wavelength <= 580:
        R = ((wavelength - 510) / (580 - 510)) ** gamma
        G = 1.0
        B = 0.0
    elif wavelength >= 580 and wavelength <= 645:
        R = 1.0
        G = (-(wavelength - 645) / (645 - 580)) ** gamma
        B = 0.0
    elif wavelength >= 645 and wavelength <= 750:
        attenuation = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)
        R = (1.0 * attenuation) ** gamma
        G = 0.0
        B = 0.0
    else:
        R = 0.0
        G = 0.0
        B = 0.0

    return (R, G, B)


# https://cdn.sparkfun.com/assets/learn_tutorials/8/3/0/AS7265x_Datasheet.pdf
FWHM=20 

#https://en.wikipedia.org/wiki/Full_width_at_half_maximum
sig=FWHM/(2*np.sqrt(2*np.log(2))) 

# Gaussian function
def g(x,mu):
    return np.exp(-(x-mu)**2/(2*sig**2))

x = np.linspace(350,1000,10000)
colors=[wavelength_to_rgb(wx) for wx in x]

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

space_pressed = 0
is_space_pressed = 0

def on_press(key):
    if key==Key.space:
        global space_pressed
        space_pressed+=1

def calibrate(measurements):
    calibration = np.array(raw_calib.split(',').copy()).astype(float)
    # import pdb; pdb.set_trace()
    return measurements/calibration

def animate(i):
    try:
        # Read from the serial port 
        time.sleep(.1)
        ser_str = ser.readline().decode().rstrip()
        ser_lst = ser_str.split(',')
        ser_lst = ser_lst[:-1]
        measurements = np.array(ser_lst.copy()).astype(float)
        with open('out.txt', 'a') as f:
            for item in measurements:
                f.write("%s," % item)
            f.write('\n')
        measurements = calibrate(measurements)

        # Sort data in the order of increasing wavelengths
        data = np.hstack((channels[:,np.newaxis],measurements[:,np.newaxis]))
        data=data[data[:,0].argsort()]

        wl = data[:,0].astype(float) # wavelengths
        A = data[:,1].astype(float)  # amplitudes

        # Interpolate the measurements using radial basis functions
        f = Rbf(wl, A, function='multiquadric', epsilon=np.sqrt(2.0)*sig)
        y = f(x)
        y = np.where(y<0, 0.0*y, y)
        y = np.where(x <= wl[0], A[0]*g(x,wl[0]), y)
        y = np.where(x > wl[-1], A[-1]*g(x,wl[-1]), y)

        i_max = np.argmax(y)
        
        # Plot the spectrum
        ax1.clear()
        ax1.scatter(x, y, color=colors,s=1)
        print("plotted:", i)

        ax1.grid()
        
        global is_space_pressed 
            
        if (space_pressed>is_space_pressed):
            is_space_pressed = space_pressed
            timenow = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

            with open(logfile, "a") as myfile:
                myfile.write(timenow+'\n')
                myfile.write(ser_str+'\n')
                myfile.write('Max peak at '+str(x[i_max])+'\n\n')
            
            figname = 'spectrum_'+timenow+'.png'
            plt.savefig(figdir+'/'+ figname, format='png', dpi=150)
            print(figname+ ' saved')

        ax1.set_xticks(wl)
    except Exception as e:
        print("exception:", e)    


with Listener(on_press=on_press) as listener:
    print("SPACE PRESSED")
    ani=animation.FuncAnimation(fig, animate, interval=500)
    plt.show()
  