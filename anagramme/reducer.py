#!/usr/bin/env python

from collections import defaultdict
import sys

grouped_values = defaultdict(list)
def recude_dic(dic):
    for key, values in grouped_values.items():
        if len(values) > 1:
            print('\t'.join(map(str,values)))

for input in sys.stdin:
    key,value=input.strip().split('\t')
    grouped_values[key].append(value)

recude_dic(grouped_values)

