#!/usr/bin/env python

import sys
import os
import optparse
import subprocess
import random
import traci
from Logic import Logic
import heapq
from heapq import heappush, heappop


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
        
        vNum_phase_s1=0 
        vNum_phase_s2=0
        vNum_phase_s3=0
        vNum_phase_s4=0
        
        vNum_phase_w0=0
        vNum_phase_w1=0 
        vNum_phase_w2=0
        vNum_phase_w3=0
        vNum_phase_w4=0
        
        vNum_phase_n1=0
        vNum_phase_n2=0
        vNum_phase_n3=0
        vNum_phase_n4=0
        
        vNum_phase_e1=0
        vNum_phase_e2=0
        vNum_phase_e3=0
        vNum_phase_e4=0
        vNum_phase_e0=0
        sum26=0
        sum37=0
        sum15=0
        sum48=0
        heap = []
        
        for lad in traci.areal.getIDList():
            #print("lad : ", lad)
            lane_id = lad.split(".")[1]
            #print("lane_id : ", lane_id)            
            if(lane_id == 'S1' or lane_id == 'S2' or lane_id == 'S3' or lane_id == 'N1' or lane_id == 'N2' or lane_id == 'N3'):
                sum48+=traci.areal.getLastStepVehicleNumber(lad)
            elif(lane_id == 'N4' or lane_id == 'S4'):
                sum37+=traci.areal.getLastStepVehicleNumber(lad)
            elif(lane_id == 'E0' or lane_id == 'E1' or lane_id == 'E2' or lane_id == 'W0' or lane_id == 'W1' or lane_id == 'W2'):
                sum26+=traci.areal.getLastStepVehicleNumber(lad)                
            elif(lane_id == 'E4' or lane_id == 'E3' or lane_id == 'W3' or lane_id == 'W4'):
                sum15+=traci.areal.getLastStepVehicleNumber(lad)
        
        heapq.heappush(heap, sum26)
        heapq.heappush(heap, sum37)
        heapq.heappush(heap, sum15)
        heapq.heappush(heap, sum48)

        max_val = heapq.nlargest(1, heap)
        
        if max_val[0] == sum26:
            sum26=0
            return [2,6]
        elif max_val[0] == sum37:
            sum37=0
            return [3,7]
        elif max_val[0] == sum15:
            sum15=0
            return [1,5]
        elif max_val[0] == sum48:
            sum48=0
            return [4,8]
        
        '''     
        ## Applying Protected-permissive here ##  
        if 2 in current_phases and 6 in current_phases:
            sum26 = vNum_phase_e17 + vNum_phase_e18 + vNum_phase_e19 + vNum_phase_w6 + vNum_phase_w7 + vNum_phase_w8
            sum37 = vNum_phase_n15 + vNum_phase_s4                      
            if(sum26 > sum37):
                return [2,6]
            else:
                return [3,7]
        elif current_phases==[3,7]:
            sum37 = vNum_phase_n15 + vNum_phase_s4                      
            sum3478 = vNum_phase_n15 + vNum_phase_s1 + vNum_phase_s2 + vNum_phase_s3 + vNum_phase_s4 + vNum_phase_n12 + vNum_phase_n13 + vNum_phase_n14
            if sum37 > sum3478:
                return [3,7]
            else:
                return [3,4,7,8]                
        elif current_phases==[3,4,7,8]:
            sum3478 = vNum_phase_n15 + vNum_phase_s1 + vNum_phase_s2 + vNum_phase_s3 + vNum_phase_s4 + vNum_phase_n12 + vNum_phase_n13 + vNum_phase_n14
            sum15 = vNum_phase_w10 + vNum_phase_w9 + vNum_phase_e20 + vNum_phase_e21            
            if sum3478 > sum15:
                return [3,4,7,8]
            else:
                return [1,5]
        elif current_phases==[1,5]:
            sum15 = vNum_phase_w10 + vNum_phase_w9 + vNum_phase_e20 + vNum_phase_e21            
            sum1256 = vNum_phase_w10 + vNum_phase_w9 + vNum_phase_e17 + vNum_phase_e18 + vNum_phase_e19 + vNum_phase_e20 + vNum_phase_e21 + vNum_phase_w6 + vNum_phase_w7 + vNum_phase_w8
            if sum15 > sum1256:
                return [1,5]
            else:
                return [1,2,5,6]                
        '''         
