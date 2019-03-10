#-*- coding: utf-8 -*-

#How to run: python producer_consumer_fsm.py

import random
import time
import pickle # To provide loose coupling by facilitating load and save config data from file
import threading

###########################################################################################################
# Configurations can be saved into or loaded from a separate file via pickle :-)  

# Transitions config
transitions = [
    { 'trigger': 'fulfillOrder', 'src': 'Null', 'dst': 'Created' },
    { 'trigger': 'activate', 'src': 'Created', 'dst': 'Activated' },
    { 'trigger': 'cancel', 'src': 'Created', 'dst': 'Cancelled' },
    { 'trigger': 'cancel', 'src': 'Activated', 'dst': 'Cancelled' },
    { 'trigger': 'makeProgress', 'src': 'Activated', 'dst': 'In_Progress' },
    { 'trigger': 'cancel', 'src': 'In_Progress', 'dst': 'Cancelled' },
    { 'trigger': 'complete', 'src': 'In_Progress', 'dst': 'Completed' }
]
# States config
states=['Null', 'Created', 'Activated', 'InProgress', 'Completed', 'Cancelled']

# The initial state config
initial = 'Null'

# The final states config
finals = ['Completed', 'Cancelled']

###########################################################################################################

# Utility function for dumping config data into pickle file
def dump_data():
    with open('states.pickle', 'wb') as handle:
        pickle.dump(states, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open('transitions.pickle', 'wb') as handle:
        pickle.dump(transitions, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open('initial.pickle', 'wb') as handle:
        pickle.dump(initial, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open('finals.pickle', 'wb') as handle:
        pickle.dump(finals, handle, protocol=pickle.HIGHEST_PROTOCOL)



# Utility function for loading config data from pickle file
def load_data():
    with open('states.pickle', 'rb') as handle:
        states = pickle.load(handle)

    with open('transitions.pickle', 'rb') as handle:
        transitions = pickle.load(handle)

    with open('initial.pickle', 'rb') as handle:
        initial = pickle.load(handle)

    with open('finals.pickle', 'rb') as handle:
        finals = pickle.load(handle)

###########################################################################################################

# Generic Finite State Machine

class FSM:
    def __init__(self, initialState=None, finalStates=[], states=[], transitions=[], machine_id=None):
        self.name = machine_id      # machine id

        if not initialState:
            raise InvalidMachineError('No initial state defined')

        self.state = initialState   # current state
        self.finals = finalStates   # accepting states
        
        if not states:
            raise InvalidMachineError('There are no states')

        self.states = states        # list of states
        self.callbacks = {}         # dict of callbacks
        self.events = {}            # collection of transitions
        
        if not transitions:
            raise InvalidMachineError('There are no transitions')

        for t in transitions:       # modifying event as a hashmap of transitions
            key=t['trigger']
            if key not in self.events.keys():
                self.events[key]={}
            pair = [val for val in t.values() if val not in key]
            self.events[key][pair[0]] = pair[1]
        print "Building finite state machine " + self.name+ " done."

    def setCallback(self, state, fn):
        self.callbacks[state] = [fn, state]
        print "Setting callback on " + state + " state for machine " + self.name + " done."


    def trigger(self, event):
        if event not in self.events:                # event could not be triggered due to INVALID_TANSITION
            print "State not changed for "+self.name + " : Invalid Transition " + event
            return False

        transitions = self.events[event]            # fetch transitions from hashmap

        if self.state not in transitions:           # event could not be triggered due to INVALID_STATE
            print "State not changed for "+self.name + " : Invalid state " + self.state
            return False

        self.state = transitions[self.state]        # process and update state

        for state in ["any", self.state]:     # specific and global post-transit callbacks for state change 
            if state in self.callbacks:
                func = self.callbacks[state]
                func[0](func[1], event, self.name)  # calling associated fn function from callbacks dict

        return True                                 # event triggered succesfully 

###########################################################################################################

# Exception Handling

class FSMError(Exception):
    pass

class InvalidMachineError(FSMError):
    def __init__(self, msg):
        print "Exception occured while building FSM : " + msg

###########################################################################################################
#                                       MAIN STARTS FROM HERE                                             #
###########################################################################################################

# Build FSM

num_of_machines = 2 #No. of FSM 
debug = False

FSM1 = FSM(initial, finals, states, transitions, "FSM1")
FSM2 = FSM(initial, finals, states, transitions, "FSM2")

# Bind callbacks to FSM

def notify_on_specific_state(state, event=None, machine_id=None):
    if not machine_id:
        machine_id = ""
    print "Notify " + machine_id + " subscribers => State reached to " + state

def notify_on_any_state(state, event=None, machine_id=None):
    if not machine_id:
        machine_id = ""
    print "Notify " + machine_id + " subscribers => Event " + event + " triggered!"

FSM1.setCallback("Activated", notify_on_specific_state) # state specific callback for FSM1
FSM1.setCallback("any", notify_on_any_state) # "any" state callback for FSM1
FSM2.setCallback("Cancelled", notify_on_specific_state) # state specific callback for FSM2

# Build Queue to take machine specific events from producer then process via FSM and send appropriate notifications to subscribers using callback

queue = [
        ("FSM1","fulfillOrder"), ("FSM1","activate"), ("FSM1","activate"), ("FSM1","makeProgress"),
        ("FSM2","fulfillOrder"), ("FSM2","fulfillOrder"), ("FSM2","cancel"), ("FSM2","makeProgress")
]

# Normal Runner function

def run_without_producer_consumer(queue):
    print "Starting Finite State Machine in non producer consumer mode"
    for transaction in queue:
        machine_id = transaction[0]
        event_name = transaction[1]
        trigger_event_func = machine_id + '.trigger(' + '"' + event_name + '"' + ')'
        #print machine_id
        if eval(trigger_event_func):
            print machine_id+" processed "+ event_name +" event and reached to" + eval(machine_id+".state")

###########################################################################################################

# Settting up Producer-Consumer Environment

class FSM_ProducerThread(threading.Thread):
    def run(self):
        global queue
        global debug
        global num_of_machines
        nums = range(1,num_of_machines+1)
        choice_of_operations = ["fulfillOrder","activate", "cancel", "makeProgress", "complete"] 
        while len(queue)<20:
            machine_id = "FSM"+str(random.choice(nums))
            event = random.choice(choice_of_operations)
            queue.insert(len(queue),(machine_id, event))
            if debug:
                print len(queue), machine_id, event    #### debug mode
            else:
                print "Producer has put event " + event + " for machine " + machine_id + " in the queue"    
            time.sleep(0.1)
        if debug:
            debug=False


class FSM_ConsumerThread(threading.Thread):
    def run(self):
        global queue
        global debug
        while len(queue)>0:
            transaction = queue.pop(0)
            machine_id = transaction[0]
            event = transaction[1]
            if debug:
                print len(queue), machine_id, event     #### debug mode
            else:
                trigger_event_func = machine_id + '.trigger(' + '"' + event + '"' + ')'
                eval(trigger_event_func)
                print "consumer consumed", event, machine_id
            time.sleep(0.1)
        if debug:
            debug=False

        

##############################################################################################

#Thread Runner and Tester functions

def run_with_producer_consumer():
    print "Starting Finite State Machine in producer consumer mode"

    print "Starting Producer Thread"
    FSM_ProducerThread().start()

    print "Starting Consumer Thread"
    FSM_ConsumerThread().start()

def test_producer_thread():
    print "Running Producer Thread in Debug mode"
    global debug
    debug = True
    FSM_ProducerThread().start()

def test_consumer_thread():
    print "Running Consumer Thread in Debug mode"
    global debug
    debug = True
    FSM_ConsumerThread().start()

################################################################################################

############# Runs

# Run with Producer consumer
#run_with_producer_consumer()

# Run without Producer consumer
run_without_producer_consumer(queue)

################################################################################################

############# Tests 

# Test Producer Thread in Debug mode
#test_producer_thread()

# Test Consumer Thread in Debug mode
#test_consumer_thread()

################################################################################################

# Developed by:
#
#   /\ "-.\ \   /\ \   /\__  _\ /\ \   /\ "-.\ \      /\ "-./  \   /\ \   /\  ___\   /\ \_\ \   /\  == \   /\  __ \   
#   \ \ \-.  \  \ \ \  \/_/\ \/ \ \ \  \ \ \-.  \     \ \ \-./\ \  \ \ \  \ \___  \  \ \  __ \  \ \  __<   \ \  __ \  
#    \ \_\\"\_\  \ \_\    \ \_\  \ \_\  \ \_\\"\_\     \ \_\ \ \_\  \ \_\  \/\_____\  \ \_\ \_\  \ \_\ \_\  \ \_\ \_\ 
#     \/_/ \/_/   \/_/     \/_/   \/_/   \/_/ \/_/      \/_/  \/_/   \/_/   \/_____/   \/_/\/_/   \/_/ /_/   \/_/\/_/ 
#
# on 10th March 2019
