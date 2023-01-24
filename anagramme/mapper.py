#!/usr/bin/env python3
# coding: utf-8


import sys

def map(line):
    for word in line.split():
        return ''.join(sorted(word)), word

print(map(sys.stdin))