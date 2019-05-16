#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from directory import Directory

if __name__ == '__main__':
	directory = Directory()()