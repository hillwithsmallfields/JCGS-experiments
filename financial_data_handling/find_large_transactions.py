#!/usr/bin/env python3

"""Program to look through my bank statements for large transactions.

The code is specific to Handelsbanken UK but should be easy to adapt."""

import argparse
import collections
import csv
import glob
import os

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", type=float, default=1000)
    return vars(parser.parse_args())

def find_large_transactions(size):
    """Scan through a collection of bank statements,
    looking for transactions above a given size."""
    transactions = collections.defaultdict(list)
    for filename in glob.glob(os.path.expanduser("~/Downloads/Transactions*.csv")):
        with open(filename) as instream:
            for row in csv.DictReader(instream):
                try:
                    if ((float(row["Cr Amount"]) >= size)
                        or (float(row["Dr Amount"]) >= size)):
                        transactions[row["Value Date"]].append((filename, row))
                except ValueError:
                    pass
    for date in sorted(transactions.keys()):
        print(date)
        for tr in transactions[date]:
            print("  ", tr)

if __name__ == "__main__":
    find_large_transactions(**get_args())
