#!/usr/bin/env python3

"""Program to look through my bank statements for large transactions.

The code is specific to Handelsbanken UK but should be easy to adapt."""

import argparse
import collections
import csv
import glob
import json
import os

from frozendict import frozendict

OUTPUT_HEADERS = ['Date', 'Account', 'Value Date', 'Narrative', 'Dr Amount', 'Cr Amount', 'Balance', 'Files']

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", type=float, default=1000)
    parser.add_argument("--output", "-o", help="""Output filename""")
    parser.add_argument("--ignore", "-i", help="""Ignore rows that have this string in their Narrative.""")
    return vars(parser.parse_args())

def find_large_transactions(size, output, ignore):
    """Scan through a collection of bank statements,
    looking for transactions above a given size."""
    transactions = collections.defaultdict(lambda:collections.defaultdict(set))
    for filename in glob.glob(os.path.expanduser("~/Downloads/Transactions*.csv")):
        with open(filename) as instream:
            for row in csv.DictReader(instream):
                try:
                    if (((float(row["Cr Amount"]) >= size)
                         or (float(row["Dr Amount"]) >= size))
                        and ((not ignore)
                             or (not ignore in row['Narrative']))):
                        frozen_row = frozendict(row)
                        # transactions[row["Value Date"]].append((filename, frozen_row))
                        transactions[row["Value Date"]][frozen_row].add(filename)
                except ValueError:
                    pass
    with open(output, 'w') as outstream:
        writer = csv.DictWriter(outstream, OUTPUT_HEADERS)
        writer.writeheader()
        for date in sorted(transactions.keys()):
            x = transactions[date]
            for tr in sorted(x.keys(), key=lambda a: a['Account']):
                writer.writerow(tr | {'Date': date, 'Files': ';'. join(sorted(x[tr]))})

if __name__ == "__main__":
    find_large_transactions(**get_args())
