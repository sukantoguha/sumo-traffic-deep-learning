#!/usr/bin/env python

import sys
import optparse
import subprocess
import random
import traci
from Logic import Logic


#  Fixed timing logic
class LogicFixed(Logic):

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
        if self.left_policy == "protected":
            return self.protected(current_phases)
        elif self.left_policy == "protected-permissive":
            return self.protected_permissive(current_phases)
        elif self.left_policy == "split-protect-NS":
            return self.splitNS(current_phases)
        elif self.left_policy == "split-protect-EW":
            return self.splitEW(current_phases)
        elif self.left_policy == "unrestricted":
            # Fixed time requires a defined phase sequence
            raise NotImplementedError

    def protected(self, current_phases):
        #change phases according to RnB diagram
        if current_phases==[1,5]:
            return [2,6]
        elif current_phases==[2,6]:
            return [3,7]
        elif current_phases==[3,7]:
            return [4,8]
        elif current_phases==[4,8]:
            return [1,5]

    def protected_permissive(self, current_phases):
        #change phases according to RnB diagram
        #initial phases are 2,6 so handle that
        if 2 in current_phases and 6 in current_phases:
            return [3,7]
        elif current_phases==[3,7]:
            return [3,4,7,8]
        elif current_phases==[3,4,7,8]:
            return [1,5]
        elif current_phases==[1,5]:
            return [1,2,5,6]

    def splitNS(self, current_phases):
        #in splitNS, handle initial case separately as well
        if 2 in current_phases and 6 in current_phases:
            return [2,5]
        #recurring NS starts from here
        elif current_phases==[2,5]:
            return [1,6]
        elif current_phases==[1,6]:
            return [3,7]
        elif current_phases==[3,7]:
            return [3,4,7,8]
        elif current_phases == [3,4,7,8]:
            return [2,5]

    def splitEW(self, current_phases):
        if 2 in current_phases and 6 in current_phases:
            return [4,7]
        elif current_phases==[4,7]:
            return [3,8]
        elif current_phases==[3,8]:
            return [1,5]
        elif current_phases==[1,5]:
            return [1,2,5,6]


