from fileinput import filename
from re import X
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import sys

def main():

    if len(sys.argv) <= 1:
        print('Error: Please include at least one file to analyze. Format:')
        print('$ python plot_sample.py FILE [FILE2, FILE3, ...]')
        return

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

    for sample_num in range(1, len(sys.argv)):
        file_name = sys.argv[sample_num]

        if not file_name.endswith('.csv'):
            print("Error: Filenames must all end in '.csv'")
            return

        file_name = file_name[:-4]

        df = pd.read_csv(sys.argv[sample_num])

        mu = df.mean()
        mu.index = channels

        sigma = df.std()
        sigma.index = channels
        print(sigma)

        # TODO: Figure out how to make Confidence Interval based on sigma

        sns.lineplot(data=mu, ci=2)
        plt.savefig(file_name + '.png')

        # TODO: Create csv with usable data

        # TODO: Print useful data


if __name__ == '__main__':
    main()
