############################################
# dfa union
#
# Jude Gabriel
# Version: 11/13/2022
#############################################
import json


def getStates(dfa):
    # Pull set of states from json data
    states = []
    for i in range(len(dfa.get('states'))):
        states.append(dfa.get('states')[i].get('state'))
    return states

def getLanguage(dfa1, dfa2):
    l1 = dfa1.get('language')
    l2 = []
    print(l1)


def getTransitions(dfa):
    # Pull transition tables from json data
    transitions_table = []
    for i in range(len(dfa.get('states'))):
        state_transition = []
        keys = list(dfa.get('states')[i].keys())
        keys.pop(0)  # Pop the first key since it is just 'states'
        for key in keys:
            state_transition.append(dfa.get('states')[i].get(key))
        transitions_table.append(state_transition)
    return transitions_table


def getStartState(dfa):
    # Return the start state of the specified DFA
    return dfa.get("start-state")


def getAcceptStates(dfa):
    # Pull accept states from json data
    accept_states = []
    for i in range(len(dfa.get("accept-states"))):
        accept_states.append(dfa.get("accept-states")[i].get("state"))
    return accept_states


def getDFA():
    # Load the json data
    file_dfa1 = json.load(open("dfa1.json"))
    file_dfa2 = json.load(open("dfa2.json"))

    # Build the 5-tuples for each DFA
    dfa1_states = getStates(file_dfa1)
    dfa2_states = getStates(file_dfa2)
    language = getLanguage(file_dfa1, file_dfa2)
    dfa1_transitions = getTransitions(file_dfa1)
    dfa2_transitions = getTransitions(file_dfa2)
    dfa1_start_state = getStartState(file_dfa1)
    dfa2_start_state = getStartState(file_dfa2)
    dfa1_accept_states = getAcceptStates(file_dfa1)
    dfa2_accept_states = getAcceptStates(file_dfa2)
    dfa1 = [dfa1_states, dfa1_transitions, dfa1_start_state, dfa1_accept_states]
    dfa2 = [dfa2_states, dfa2_transitions, dfa2_start_state, dfa2_accept_states]

    # Return the two DFA 5 tuples
    return dfa1, dfa2


def generateStates(dfa1, dfa2):
    # Concatenate all dfa1 states and all dfa2 states to make new set of states
    states = ["q0r0", "q0r1", "q1r0", "q1r1", "q2r0", "q2r1"]
    return states


def addTransitions(dfa1, dfa2):
    # Go through dfa1 and dfa2 delta tables. Get all sets of transitions
    transitions = [["q1r0", "q1r1"], ["q1r0", "q1r1"], ["q2r0", "q2r1"],
                   ["q1r0", "q2r1"], ["q0r0", "q0r1"], ["q0r0", "q0r1"]]
    return transitions


def findStartState(dfa1, dfa2):
    # Return the string representing the start states from each DFA concatenated
    return "q0r0"


def findAcceptStates(dfa1_accept, dfa2_accept, union_states):
    # Find all states that contain an accept state substring
    accept_states = ["q0r0", "q0r1", "q1r1", "q2r1"]
    return accept_states


def makeUnion(dfa):
    json_obj = {'states': []}

    # Make transition tables
    for i in range(len(dfa[0])):
        json_obj['states'].append({
            "state": dfa[0][i], "a": dfa[1][i][0], "b": dfa[1][i][1]
        })

    # Add start states
    json_obj['start-states'] = dfa[2]

    # Add the accept states
    json_obj['accept-states'] = []
    for i in range(len(dfa[3])):
        json_obj['accept-states'].append(({
            "state": dfa[3][i]
        }))

    # Save to json file
    with open('union_dfa_beta.json', 'w') as jsonFile:
        json.dump(json_obj, jsonFile, indent=4)


def main():
    # Get the DFAs' 5 tuples
    dfa1, dfa2 = getDFA()
    print(dfa1, "\n\n")
    print(dfa2)

    # Build the 5-tuple for the union dfa
    union_states = generateStates(dfa1[0], dfa2[0])
    union_transitions = addTransitions(dfa1[1], dfa2[1])
    start_state = findStartState(dfa1[2], dfa2[2])
    accept_states = findAcceptStates(dfa1[3], dfa2[3], union_states)
    union_dfa = [union_states, union_transitions, start_state, accept_states]

    # Send union dfa to json format
    makeUnion(union_dfa)


if __name__ == "__main__":
    main()


