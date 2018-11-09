#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ikopyeva.py
ChE 696 project to track follicle diameters

Handles the primary functions
"""

import sys
import argparse
import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np
from pandas import DataFrame


data = pd.read_csv("data/follicle_data_2.csv", header=None) #reading in csv file
data.columns = data.iloc[0, 0:]

data.index = ['samples', 'day 0', 'day 2', 'day 4', 'day 6', 'day 8', 'day 10', 'day 12']
df = data.drop(['samples'])
df = df.apply(pd.to_numeric) #converting from object to int


# ax = df.plot(kind='line')
# ax.set_xticks(range(len(df.index)))
# ax.set_xticklabels(df.index, rotation=90)
# ax.legend(title=None)
# ax.set_xlabel('Time (days)')
# ax.set_ylabel('Follicle Diameter ($\mu$m)')
# ax.set_title('Peptides and their Effect on Follicle Growth')
# plt.show()
# plt.interactive(False)

dead = np.zeros(shape=(len(df.index), len(df.columns)))



#os.path.isdir/file to check if it made the actual file??

# def warning(*objs):
#     """Writes a message to stderr."""
#     print("WARNING: ", *objs, file=sys.stderr)
#
#
# def canvas(with_attribution=True):
#     """
#     Placeholder function to show example docstring (NumPy format)
#
#     Replace this function and doc string for your own project
#
#     Parameters
#     ----------
#     with_attribution : bool, Optional, default: True
#         Set whether or not to display who the quote is from
#
#     Returns
#     -------
#     quote : str
#         Compiled string including quote and optional attribution
#     """
#
#     quote = "The code is but a canvas to our imagination."
#     if with_attribution:
#         quote += "\n\t- Adapted from Henry David Thoreau"
#     return quote
#
#
# def parse_cmdline(argv):
#     """
#     Returns the parsed argument list and return code.
#     `argv` is a list of arguments, or `None` for ``sys.argv[1:]``.
#     """
#     if argv is None:
#         argv = sys.argv[1:]
#
#     # initialize the parser object:
#     parser = argparse.ArgumentParser()
#     # parser.add_argument("-i", "--input_rates", help="The location of the input rates file",
#     #                     default=DEF_IRATE_FILE, type=read_input_rates)
#     parser.add_argument("-n", "--no_attribution", help="Whether to include attribution",
#                         action='store_false')
#     args = None
#     try:
#         args = parser.parse_args(argv)
#     except IOError as e:
#         warning("Problems reading file:", e)
#         parser.print_help()
#         return args, 2
#
#     return args, 0
#
#
# def main(argv=None):
#     args, ret = parse_cmdline(argv)
#     if ret != 0:
#         return ret
#     print(canvas(args.no_attribution))
#     return 0  # success
#
#
# if __name__ == "__main__":
#     status = main()
#     sys.exit(status)


