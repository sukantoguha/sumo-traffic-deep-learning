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
        print("inside LogicActuated.py")
        # TODO: your code here
        vNum_current_phase=0
        vNum_non_current_phase84=0 
        vNum_non_current_phase15=0
        vNum_non_current_phase37=0
        vNum_non_current_phase26=0
        heap = []
        
        ## if lad == phase, then below one should work
        ## if lad == lane, then have to see ???

        for lad in traci.areal.getIDList():
            print("lad : ", lad)
            #vNum=traci.areal.getLastStepVehicleNumber(lad)
            #print("vNum : ",vNum)

        '''
        for x in current_phases:
            print("x : ",x)
            for lad in traci.areal.getIDList(): #returns a list of object in the network.
                print("lad : ",lad)
                if lad == x:
                    vNum_current_phase += traci.areal.getLastStepVehicleNumber(lad) # lad should be the lane/phase object?? ;; returning number of vehicles in each lane/phase
                elif lad == 8 | lad == 4:
                    vNum_non_current_phase84 += traci.areal.getLastStepVehicleNumber(lad) 
                elif lad == 1 | lad == 5:
                    vNum_non_current_phase15 += traci.areal.getLastStepVehicleNumber(lad) 
                elif lad == 3 | lad == 7:
                    vNum_non_current_phase37 += traci.areal.getLastStepVehicleNumber(lad) 
                elif lad == 2 | lad == 6:
                    vNum_non_current_phase26 += traci.areal.getLastStepVehicleNumber(lad) 

        heapq.heappush(heap, vNum_non_current_phase26)
        heapq.heappush(heap, vNum_non_current_phase37)
        heapq.heappush(heap, vNum_non_current_phase15)
        heapq.heappush(heap, vNum_non_current_phase84)
        heapq.heappush(heap, vNum_current_phase)

        max_val = heapq.nlargest(1, heap)
        if max_val == vNum_non_current_phase84:
            return [8,4]
        elif max_val == vNum_non_current_phase15:
            return [1,5]
        elif max_val == vNum_non_current_phase37:
            return [3,7]
        else:
            return [2,6]
        '''
        return []
