#!/usr/bin/env python

import sys
import os
import optparse
import subprocess
import random
import traci
from Logic import Logic
from DeepLearningPython35 import network
import numpy as np
#from network import Network

#  Learning agent timing logic
class LogicRL(Logic):

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
        if self.left_policy == "protected-permissive":
            np.seterr(all='raise')

            sum15=0
            sum3478=0
            sum37=0
            sum48=0
            sum26=0
            sum1256=0
            active_traffic=0
            waiting_traffic=0
            cumulative_waiting_time=0

            #computing traffic flow in all non-clashing phases
            for lad in traci.areal.getIDList():
                lane_id = lad.split(".")[1]
                if(lane_id == 'N4' or lane_id == 'S4' or lane_id == 'N1' or lane_id == 'N2' or lane_id == 'N3' or lane_id == 'S1' or lane_id == 'S2' or lane_id == 'S3'):
                    sum3478+=traci.areal.getLastStepVehicleNumber(lad)
                if(lane_id == 'N4' or lane_id == 'S4'):
                    sum37+=traci.areal.getLastStepVehicleNumber(lad)
                if(lane_id == 'E0' or lane_id == 'E1' or lane_id == 'E2' or lane_id == 'E3' or lane_id == 'E4' or lane_id == 'W0' or lane_id == 'W1' or lane_id == 'W2' or lane_id == 'W3' or lane_id == 'W4'):
                    sum1256+=traci.areal.getLastStepVehicleNumber(lad)                
                if(lane_id == 'E4' or lane_id == 'E3' or lane_id == 'W3' or lane_id == 'W4'):
                    sum15+=traci.areal.getLastStepVehicleNumber(lad)
                if(lane_id == 'S1' or lane_id == 'S2' or lane_id == 'S3' or lane_id == 'N1' or lane_id == 'N2' or lane_id == 'N3'):
                    sum48+=traci.areal.getLastStepVehicleNumber(lad)
                if(lane_id == 'E0' or lane_id == 'E1' or lane_id == 'E2' or lane_id == 'W0' or lane_id == 'W1' or lane_id == 'W2'):
                    sum26+=traci.areal.getLastStepVehicleNumber(lad)       

            '''
            print("sum26 : ", sum26)
            print("sum15 : ", sum15)
            print("sum37 : ", sum37)
            print("sum48 : ", sum48)
            print("sum1256 : ", sum1256)
            print("sum3478 : ", sum3478)
            '''

            if sum15 ==0 or sum26 ==0 or sum37==0 or sum48==0 or sum1256==0 or sum3478==0:
                return current_phases
            else:
                #Computing flowing and not-flowing traffic  through
                if 2 in current_phases and 6 in current_phases:
                    active_traffic = sum26
                    waiting_traffic = sum15 + sum3478
                elif current_phases==[3,7]:
                    active_traffic = sum37
                    waiting_traffic = sum1256 + sum48
                elif current_phases==[3,4,7,8]: 
                    active_traffic = sum3478
                    waiting_traffic = sum1256
                elif current_phases==[1,5]:
                    active_traffic = sum15
                    waiting_traffic = sum1256 

            #print("active_traffic : ", active_traffic)
            #print("waiting_traffic : ", waiting_traffic)

            #Creating a list of active vs non-active traffic
            training_data = [active_traffic, waiting_traffic]
            #print("training_data : ", training_data)

            net = network.Network([20, 30, 2]) 
            outputs = [(np.argmax(net.feedforward(x)))
                       for x in training_data]
            #print("outputs : ", outputs)

            max_output = max(outputs)
            #print("max_output : ", max_output)
        
            #Computing waiting time/reward
            vehicle_waiting_times = {}
            lane_ids = traci.areal.getIDList()
            for lane_id in lane_ids:
                vehicles = traci.areal.getLastStepVehicleIDs(lane_id)
                for vehicle in vehicles:
                    w_time = traci.vehicle.getWaitingTime(vehicle)
                    if vehicle in vehicle_waiting_times: #cumulative_waiting_time over a phase this function is executed for                             #every simulation step
                        cumulative_waiting_time += w_time - vehicle_waiting_times[vehicle+":"+lane_id]
                    else:
                        cumulative_waiting_time += w_time
                    vehicle_waiting_times[vehicle+":"+lane_id] = w_time

            #print("cumulative_waiting_time : ", cumulative_waiting_time)

            mini_batch = [training_data,cumulative_waiting_time]
            #print("mini_batch : ", mini_batch)

            #Checking whether the max_output belongs to active or waiting traffic to decide whether to change the phase or not.
            if max_output == training_data[0]:
                if training_data[0] == sum26:
                    #print("1")
                    net.update_mini_batch(mini_batch, 0.1)
                    return [2,6]
                elif training_data[0] == sum37:
                    #print("2")
                    net.update_mini_batch(mini_batch, 0.1)
                    return [3,7]
                elif training_data[0] == sum3478:
                    #print("3")
                    net.update_mini_batch(mini_batch, 0.1)
                    return [3,4,7,8]
                elif training_data[0] == sum15:
                    #print("4")
                    net.update_mini_batch(mini_batch, 0.1)
                    return [1,5]
                elif training_data[0] == sum48:
                    #print("5")
                    net.update_mini_batch(mini_batch, 0.1)
                    return [4,8]
                elif training_data[0] == sum1256:
                    #print("6")
                    net.update_mini_batch(mini_batch, 0.1)
                    return [1,2,5,6]
            elif max_output == training_data[1]:
                if training_data[0] == sum26:
                    #print("7")
                    net.update_mini_batch(mini_batch, 0.1)
                    return [3,7]
                elif training_data[0] == sum37:
                    #print("8")
                    net.update_mini_batch(mini_batch, 0.1)
                    return [3,4,7,8]
                elif training_data[0] == sum3478:
                    #print("9")
                    net.update_mini_batch(mini_batch, 0.1)
                    return [1,5]
                elif training_data[0] == sum15:
                    #print("10")
                    net.update_mini_batch(mini_batch, 0.1)
                    return [1,2,5,6]

        else:
            raise NotImplementedError
