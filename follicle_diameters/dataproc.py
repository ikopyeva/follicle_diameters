#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
dataproc.py
ChE 696 project to track follicle diameters,
takes CSV files and makes plots of ovarian follicle growth
and survival

"""

import sys
import argparse
import matplotlib.pyplot as plt
import os
import pandas as pd
from pathlib import Path


def parse_cmdline(argv):
    """
    Returns the parsed argument list and return code.
    `argv` is a list of arguments, or `None` for ``sys.argv[1:]``.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="Specify Input CSV File(s)", required=True, nargs='+', action='append')
    parser.add_argument("-o", "--output", help="dir or file to save figure in", nargs=1)
    args = None
    try:
        args = parser.parse_args(argv)

    except IOError as e:
        print("Did not parse correctly: '%s'" %e, file=sys.stderr)
        parser.print_help()
        return args, 2

    vars(args)['file']=[item for sublist in vars(args)['file'] for item in sublist] #Flatten file inputs into 1 list
    for file in vars(args)['file']:
        if not os.path.isfile(file):
            print("Error: '%s' was not found" %file, file=sys.stderr)
            return args, 2

    if vars(args)['output']:
        file_path = Path(vars(args)['output'][0]).resolve()  # add $PWD if required
        if not os.path.exists(file_path.parent):
            print("Error invalid output location '%s'" %vars(args)['output'][0], file=sys.stderr)
            return args, 2
        vars(args)['output'] = file_path

    return vars(args), 0

def read_files(files):
    """
    Takes list of Paths (filenames)
    returns dict of dataframes
    """
    data = {}
    for x in files:
        sample = x.split('/')[-1][:-4]
        data[sample] = pd.read_csv(x)
        data[sample].index *= 2  # samples are taken every other day
    return data

def clean(df):
    """
    Takes a dataframe,
    checks if dead, changes dead to NaNs,
    returns dataframe without full rows of NaNs
    """
    for sample in df:
        last_row = int(df.loc[df[sample] >= df[sample].max()-1].iloc[0].name)
        df.loc[df.index > last_row, [sample]] = None

    df = df.dropna(how='all')
    return df

def main(argv):
    """
    Takes list of arguments,
    returns .png file of plots in specified location
    """
    args, ret = parse_cmdline(argv)
    if ret:
        return ret

    data = read_files(args['file'])

    fig, axs = plt.subplots(2, 1)

    #remove measurements of dead things
    for pep, df in data.items():
        df = clean(df)

        axs[0].errorbar(df.index, df.mean(axis=1), yerr=df.std(axis=1), label=pep, capsize=3, marker='o')
        alive = df.count(axis=1)/df.shape[1]*100  #percentage of alive follicles
        axs[1].plot(df.index, alive, label=pep, marker='o')

    axs[0].legend()
    axs[0].set_xlabel('Time (days)')
    axs[0].set_ylabel('Follicle Diameter ($\mu$m)')
    axs[0].set_title('Peptides and their Effect on Ovarian Follicle Growth and Survival')

    axs[1].legend()
    axs[1].set_xlabel('Time (days)')
    axs[1].set_ylabel('% Survival')
    plt.tight_layout()

    if(args['output']):
        plt.savefig(args['output'])
    plt.show()


    return 0  # success


if __name__ == "__main__":
    status = main(sys.argv[1:])
    sys.exit(status)


