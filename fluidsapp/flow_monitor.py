#!/usr/bin/env python

import itertools
import time
from flask import Flask, Response, redirect, request, url_for
from random import gauss
import threading

# Generate streaming data and calculate statistics from it
class FlowMonitor(object):
    def __init__(self):
        self.sum   = 0
        self.count = 0
    @property
    def mu(self):
        try:
            outv = self.sum/self.count
        except:
            outv = 0
        return outv
    
    def generate_values(self):
        while True:
            time.sleep(.1)  # an artificial delay
            yield gauss(0,1)

    def monitor(self, report_interval=1):
        print ("Starting data stream...")
        for x in self.generate_values():
            self.sum   += x
            self.count += 1

flowstream = FlowMonitor()
