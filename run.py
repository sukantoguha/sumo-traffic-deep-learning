#!/usr/bin/env python


import sys
import os
import optparse
import random
import xmlparser

# Set "SUMO_HOME" as environment variable
#os.environ["SUMO_HOME"] = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
#print(os.environ["SUMO_HOME"])

# we need to import python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")
import traci  # noqa
from sumolib import checkBinary  # noqa

# Import signal timing logic classes
from Logic import Logic
from LogicFixed import LogicFixed as Fixed
from LogicActuated import LogicActuated as Actuated
from LogicRL import LogicRL as RL

left_policy = "split-protect-EW" # Left turn phase policy from {protected, protected-permissive, split-protect-NS, split-protect-EW, unrestricted}
logic = Fixed(left_policy) # Left turn phase policy from {Fixed, Actuated, RL}. All must implement: get_phase(self, current_phases)
if not issubclass(type(logic),Logic):
    raise ValueError('logic must be a sub class of Logic')

data_interval = 300 # The time interval (seconds) for each line of data in the demand file. 5 minutes in UTDOT logs (https://udottraffic.utah.gov/ATSPM)
right_on_red = True # Do we allow vehicles to turn right on red
min_phase_time = 5 # the minimal time interval between signal change (including yellow phase)


def vehicle_generator(time, demand): # time in seconds and demand as a list of entries from the demand file "State_Street_4500_South.txt"

    #Indexes for demand file
    iEL = 2 # Index for Eastbound turning left...
    iET = 3
    iETR = 4

    iWL = 6
    iWT = 7
    iWTR = 8

    iNL = 10
    iNT = 11
    iNR = 12

    iSL = 14
    iST = 15
    iSR = 16

    indexes = [iEL, iET, iETR, iWL, iWT, iWTR, iNL, iNT, iNR, iSL, iST, iSR]
    routes = ["Eastbound.L", "Eastbound.T", "Eastbound.TR", "Westbound.L", "Westbound.T", "Westbound.TR",
              "Northbound.L", "Northbound.T", "Northbound.R", "Southbound.L", "Southbound.T", "Southbound.R"]

    data = demand[int(time/data_interval)].split()  # The data entry for the current time interval is retrieved
    probabilities = []

    vehicles = []
    for x in range(len(indexes)):
        p = float(data[indexes[x]]) / data_interval  # The probability of generating a vehicle per time step for each route
        # in the current time interval
        if random.uniform(0, 1) < p:
            vehicle = [routes[x], "passenger"]
            vehicles.append(vehicle)
    return vehicles

def set_phase(indexes):

    phases = [None]*9

    # Specify the green lanes in each phase
    phases[6]=[5,6,7,8]  # phase Through, Right. Westbound
    phases[2]=[16,17,18,19]  # phase Through, Right. Eastbound
    phases[8]=[11,12,13,14]  # phase Through, Right. Northbound
    phases[4]=[0,1,2,3]  # phase Through, Right. Southbound

    phases[1]=[9,10]  # phase Left. Westbound
    phases[5]=[20,21]  # phase Left. Eastbound
    phases[3]=[15]  # phase Left. Northbound
    phases[7]=[4]  # phase Left. Southbound

    right_turns = [0,5,11,16]
    next_signals = list("rrrrrrrrrrrrrrrrrrrrrr")  # init signals

    if right_on_red:
        for x in right_turns:
            next_signals[x] = 'g'  # init right turns to green light "lower case 'g' mean that the stream has to decelerate"

    for i in indexes:
        for x in phases[i]:
            next_signals[x] = 'G'

    current_signals = list(traci.trafficlights.getRedYellowGreenState("gneJ1")) # get the currently assigned lights
    yellow_phase = False
    for x in range(len(current_signals)):
        if current_signals[x] == 'G' and next_signals[x] == 'r': # Check if a yellow phase is needed
            yellow_phase = True

    if yellow_phase:
        for x in range(len(current_signals)):
            if current_signals[x] == 'G' and next_signals[x] == 'r': # If a yellow phase is needed then find which lanes
                                                                   # should be assigned yellow
                current_signals[x] = 'y'
        traci.trafficlights.setRedYellowGreenState("gneJ1", ''.join(current_signals))
        return False
    else:
        traci.trafficlights.setRedYellowGreenState("gneJ1", ''.join(next_signals))
        return True

def run():

    with open('State_Street_4500_South.txt', 'r') as fp: # Load the demand file
        demand = fp.readlines()

    demand.pop(0)
    demand.pop(0) # The two first entries are the file header, depose them

    vehNr = 0 # Vehicles dynamic count
    N = 57600  # number of time steps (seconds) total 16 hours
    last_phase_change = 0  # The last time the signals have changed
    current_phase = [2, 6]  # currently green phases index
    yellow = False  # indicates whether the current phase is yellow

    while traci.simulation.getTime() < N + 300: # The +300 is to allow all vehicles (generated up to time N) to clear the network
        vehicles = vehicle_generator(traci.simulation.getTime(), demand)
        for v in vehicles:
            traci.vehicle.add(str(vehNr), v[0], typeID=v[1])
            vehNr += 1
        if traci.simulation.getTime() - last_phase_change >= min_phase_time:
            if yellow:
                next_phase = current_phase
            else:
                # Logic for picking the next phase
                # Next phase is a list of int representing the phases that should be assigned green next according to:
                #  6: Through, Right. Westbound
                #  2: Through, Right. Eastbound
                #  8: Through, Right. Northbound
                #  4: Through, Right. Southbound

                #  1: Left. Westbound
                #  5: Left. Eastbound
                #  3: Left. Northbound
                #  7: Left. Southbound

                # If no change is required for the current signal assignment then return -1 (instead of a list of int)
                next_phase = logic.get_phase(current_phase)
            if next_phase != -1:  # If a phase change is required
                current_phase = next_phase  # chosen phases index
                if set_phase(next_phase):  # If the chosen phases are applicable (no yellow transition is required)
                    yellow = False
                else:
                    yellow = True
                last_phase_change = traci.simulation.getTime()
        traci.simulationStep()

    traci.close()
    sys.stdout.flush()


def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options


# this is the main entry point of this script
if __name__ == "__main__":
    options = get_options()

    # this script has been called from the command line. It will start sumo as a
    # server, then connect and run
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')
    sumoBinary= checkBinary('sumo')
    xmlparser.results()
    # this is the normal way of using traci. sumo is started as a
    # subprocess and then the python script connects and runs
    traci.start([sumoBinary, "-c", "Data/State_Street_4500_South.sumocfg", "--tripinfo-output",
                                    "tripinfo.xml"]) #,  "--time-to-teleport -1"
    run()
