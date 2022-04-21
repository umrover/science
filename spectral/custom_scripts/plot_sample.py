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
    channels = {
        'A': 410,
        'B': 435,
        'C': 460,
        'D': 485,
        'E': 510,
        'F': 535,
        'G': 560,
        'H': 585,
        'I': 645,
        'J': 705,
        'K': 900,
        'L': 940,
        'R': 610,
        'S': 680,
        'T': 730,
        'U': 760,
        'V': 810,
        'W': 860
    }

    for sample_num in range(1, len(sys.argv)):
        file_name = sys.argv[sample_num]

        if not file_name.endswith('.csv'):
            print(f"Error: {file_name} does not end in '.csv'.")
            return

        sample_name = file_name[:-4]

        df = pd.read_csv(sys.argv[sample_num])

        wavelengths = []
        intensities = []
        for _, row in df.iterrows():
            for key, val in row.iteritems():

                wavelengths.append(channels[key.strip()])
                intensities.append(val)

        parsed_data = pd.DataFrame({'Wavelength': wavelengths, 'Intensity': intensities})

        sns.lineplot(x='Wavelength', y='Intensity', data=parsed_data)
        plt.savefig(sample_name + '.png')

        # TODO: Create csv with usable data

        # TODO: Print useful data


if __name__ == '__main__':
    main()
