############################################
# dfa union
#
# gabes
#############################################
import json


def getStates(dfa):
    # Pull set of states from json data
    states = []
    for i in range(len(dfa.get('states'))):
        states.append(dfa.get('states')[i].get('state'))
    return states


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

    # Build the 5-tuples
    dfa1_states = getStates(file_dfa1)
    dfa2_states = getStates(file_dfa2)
    dfa1_transitions = getTransitions(file_dfa1)
    dfa2_transitions = getTransitions(file_dfa2)
    dfa1_start_state = getStartState(file_dfa1)
    dfa2_start_state = getStartState(file_dfa2)
    dfa1_accept_states = getAcceptStates(file_dfa1)
    dfa2_accept_states = getAcceptStates(file_dfa2)
    dfa1 = [dfa1_states, dfa1_transitions, dfa1_start_state, dfa1_accept_states]
    dfa2 = [dfa2_states, dfa2_transitions, dfa2_start_state, dfa2_accept_states]

    return dfa1, dfa2


def generateStates(dfa1, dfa2):
    # Concatenate all dfa1 states and all dfa2 states to make new set of states
    states = []
    for i in range(len(dfa1)):
        for j in range(len(dfa2)):
            state = dfa1[i] + dfa2[j]
            states.append(state)
    return states


def addTransitions(dfa1, dfa2):
    # Go through dfa1 and dfa2 delta tables. Get all sets of transitions
    transitions = []
    for i in range(len(dfa1)):
        for j in range(len(dfa2)):
            state_transitions = []
            for k in range(len(dfa1[i])):
                state = dfa1[i][k] + dfa2[j][k]
                state_transitions.append(state)
            transitions.append(state_transitions)
    return transitions


def findStartState(dfa1, dfa2):
    return dfa1 + dfa2


def findAcceptStates(dfa1_accept, dfa2_accept, union_states):
    # Find all states that contain an accept state substring
    accept_states = []
    for i in range(len(union_states)):
        for j in range(len(dfa1_accept)):
            if union_states[i].count(dfa1_accept[j]) > 0:
                accept_states.append(union_states[i])
        for j in range(len(dfa2_accept)):
            if union_states[i].count(dfa2_accept[j]) > 0:
                accept_states.append(union_states[i])

    # Remove duplicates
    accept_states = list(dict.fromkeys(accept_states))
    return accept_states


def makeUnion(dfa):
    json_obj = {}
    json_obj['states'] = []

    # Make transition tables
    for i in range(len(dfa[0])):
        json_obj['states'].append({
            "state": dfa[0][i], "a": dfa[1][i][0], "b": dfa[1][i][1]
        })
    json_obj['start-state'] = dfa[2]
    json_obj['accept-states'] = []
    for i in range(len(dfa[3])):
        json_obj['accept-states'].append(({
            "state": dfa[3][i]
        }))

    # Save to json file
    with open('union_dfa.json', 'w') as jsonFile:
        json.dump(json_obj, jsonFile, indent=4)


def main():
    # Need to do something about the alphabets....
    # Get the dfa's
    dfa1, dfa2 = getDFA()

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


