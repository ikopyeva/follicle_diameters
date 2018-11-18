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

bmb_data = pd.read_csv("data/BMB.csv", header=None)
bmb_data.columns = bmb_data.iloc[0,0:]
bmb_data.index = ['samples', 'day 0', 'day 2', 'day 4', 'day 6', 'day 8', 'day 10', 'day 12']
bmb = bmb_data.drop(['samples'])
bmb = bmb.apply(pd.to_numeric)

hbp_data = pd.read_csv("data/HBP.csv", header=None)
hbp_data.columns = bmb_data.iloc[0,0:]
hbp_data.index = ['samples', 'day 0', 'day 2', 'day 4', 'day 6', 'day 8', 'day 10', 'day 12']
hbp = hbp_data.drop(['samples'])
hbp = hbp.apply(pd.to_numeric)

rgd_data = pd.read_csv("data/RGD.csv", header=None)
rgd_data.columns = rgd_data.iloc[0,0:]
rgd_data.index = ['samples', 'day 0', 'day 2', 'day 4', 'day 6', 'day 8', 'day 10', 'day 12']
rgd = rgd_data.drop(['samples'])
rgd = rgd.apply(pd.to_numeric)# converting from object to int

bmb_avg = np.zeros(shape=(len(bmb.index)))
bmb_std = np.zeros(shape=(len(bmb.index)))

hbp_avg = np.zeros(shape=(len(hbp.index)))
hbp_std = np.zeros(shape=(len(hbp.index)))

rgd_avg = np.zeros(shape=(len(rgd.index)))
rgd_std = np.zeros(shape=(len(rgd.index)))

bmb_count = np.zeros(shape=(len(bmb.index)))
hbp_count = np.zeros(shape=(len(hbp.index)))
rgd_count = np.zeros(shape=(len(rgd.index)))

data_avg = np.zeros(shape=(7, 3))
data_std = np.zeros(shape=(7, 3))

for j in range(len(bmb.columns)): # compares previous row to current row and determines whether follicle is dead
    for i in range(len(bmb.index)):
        if i == 0:
            bmb_count[i] += 1
        elif 1 < (bmb.iloc[i, j] - bmb.iloc[i-1, j]):
            bmb_count[i] += 1
        else:
            bmb_count[i] += 0
            bmb.iloc[i, j] = np.nan #if follicle is dead, puts NaN
bmb_count = np.true_divide(bmb_count, 7/100)

for x in range(len(bmb.index)):
    bmb_avg[x] = np.nanmean(bmb.iloc[x])
    bmb_std[x] = np.nanstd(bmb.iloc[x])

data = np.vstack((bmb_avg.T, hbp_avg.T, rgd_avg.T))
std = np.vstack((bmb_std.T, hbp_std.T, rgd_std.T))
data = data.T
std = std.T

df = pd.DataFrame.from_records(data)
std_df = pd.DataFrame.from_records(std)
df.columns = ['BMB', 'HBP', 'RGD']
df.index = ['day 0', 'day 2', 'day 4', 'day 6', 'day 8', 'day 10', 'day 12']
std_df.columns = ['BMB', 'HBP', 'RGD']
std_df.index = ['day 0', 'day 2', 'day 4', 'day 6', 'day 8', 'day 10', 'day 12']

ax = df.plot(yerr=std_df, fmt='o-', capsize=3)

#plot error bars
#ax = df.plot(figsize=(12, 8), yerr=std_df, capsize=3, legend=False)
#reset color cycle so that the marker colors match
#ax.set_prop_cycle(None)
#plot the markers
#df.plot(figsize=(12, 8), style=['^-', 'o-', 'x-'], markersize=10, ax=ax, legend=True)

ax.set_xticks(range(len(df.index)))
ax.set_xticklabels(df.index, rotation=90)
ax.legend(title=None)
ax.set_xlabel('Time (days)')
ax.set_ylabel('Follicle Diameter ($\mu$m)')
ax.set_title('Peptides and their Effect on Follicle Growth')
plt.show()
plt.interactive(False)





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


