#!/usr/bin/env python

import sys
import os
import optparse
import subprocess
import random
import traci
from Logic import Logic


#  Actuated timing logic
class LogicActuated(Logic):

    # get_phase: return a list of phase indices (to be set to green) or -1 if no change is required
    #  6: Through, Right. Westbound
    #  2: Through, Right. Eastbound
    #  8: Through, Right. Northbound
    #  4: Through, Right. Southbound

    #  1: Left. Westbound
    #  5: Left. Eastbound
    #  3: Left. Northbound
    #  7: Left. Southbound
    def get_phase(self, current_phases):
        # TODO: your code here
        return []


