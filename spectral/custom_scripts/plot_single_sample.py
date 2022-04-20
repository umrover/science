import numpy as np
import seaborn as sns

import sys
import csv

def main():

    # https://learn.sparkfun.com/tutorials/spectral-triad-as7265x-hookup-guide
    channels = np.array([
        410,  # A
        435,  # B
        460,  # C
        485,  # D
        510,  # E
        535,  # F
        560,  # G
        585,  # H
        645,  # I
        705,  # J
        900,  # K
        940,  # L
        610,  # R
        680,  # S
        730,  # T
        760,  # U
        810,  # V
        860   # W
    ])

    input_file_name = sys.argv[1]
    with open(input_file_name) as f:
        header_row = True

        mu = np.array()

        for row in csv.reader(f):

            print(row)

if __name__ == '__main__':
    main()
