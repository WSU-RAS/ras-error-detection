#!/usr/bin/env python3

import csv

from items import Items


fh = open('estimotes.data', 'w')
fh_full = open('estimotes_full.data', 'w')

with open('full_data.csv', newline='') as csvfile:
    data = csv.reader(csvfile, delimiter=',', quotechar='|')
    prev_time = None
    prev_label = None
    head = True

    for row in data:
        if head:
            head = False
            continue

        row[0] = Items.decode[int(row[0][4:])]
        if row[3] == 'start':
           fh.write("{}   {}   {}\n".format(row[1], row[2], row[0]))

        fh_full.write("{} {} {} {}\n".format(row[1], row[2], row[0], row[3]))

fh.close()
fh_full.close()
