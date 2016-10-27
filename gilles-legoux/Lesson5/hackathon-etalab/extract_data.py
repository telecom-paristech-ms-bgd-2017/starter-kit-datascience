#!/usr/bin/env python3

# standard library imports
import sys

# related third party imports
import pandas as pd

# local application/library specific imports
from clean_data import *

if __name__ == "__main__":

    args = sys.argv[1:]
    if len(args) == 0:
        sys.stderr.write('usage: missing argument filename\n')
        sys.exit(1)

    # './data/R2015/R201501-utf8-unix-summary.CSV'
    filename = args[0]

    df = pd.read_csv(filename,
                     sep=';',
                     usecols=['region', 'dep_mon', 'exe_spe'])

    df.rename(columns={'region': 'area_id',
                       'dep_mon': 'extra_fees',
                       'exe_spe': 'speciality_id'}, inplace=True)

    df['area_id'] = df['area_id'].astype(int)
    df['extra_fees'] = df['extra_fees'].apply(get_number)
    df['speciality_id'] = df['speciality_id'].astype(int)

    print(df.groupby(['speciality_id', 'area_id']).agg({
        'extra_fees': 'sum'}))

    print(df['area_id'].unique())
    print(df['speciality_id'].unique())
