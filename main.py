############################################
# main.py
#
#
# Does the json parsing to get DFAs
# has all logic to perform DFA union
#
# Author: Jude Gabriel
#############################################
import json
import errorChecker


# Pull set of states from json data
def getStates(dfa):
    states = []
    for i in range(len(dfa.get('states'))):
        states.append(dfa.get('states')[i].get('state'))
    return states


# Get the alphabets from each DFA
def getAlphabet(dfa1, dfa2):
    l1 = dfa1.get('alphabet')
    l2 = dfa2.get('alphabet')
    errorChecker.checkAlphabets(l1, l2)
    return l1


# Pull transition tables from json data
def getTransitions(dfa, alphabet, states):
    transitions_table = []
    for i in range(len(dfa.get('states'))):
        state_transition = []
        keys = list(dfa.get('states')[i].keys())
        keys.pop(0)                                              # Pop the first key since it is just 'states'
        errorChecker.checkKeys(keys, alphabet)                   # Check there is a key for each alphabet char
        for j in range(len(keys)):
            errorChecker.checkTransitions(keys[j], alphabet[j])  # Check for a transition for each char in alphabet
            state_transition.append(dfa.get('states')[i].get(keys[j]))
        transitions_table.append(state_transition)
    errorChecker.checkValidStates(transitions_table, states)     # Check all transitions go to valid states
    return transitions_table


# Get the start state from the json file
def getStartState(dfa, states):
    start = dfa.get("start-state")
    errorChecker.checkValidStates(start, states)
    return start


# Pull accept states from json data
def getAcceptStates(dfa, states):
    accept_states = []
    for i in range(len(dfa.get("accept-states"))):
        accept_states.append(dfa.get("accept-states")[i].get("state"))
    errorChecker.checkValidStates(accept_states, states)
    return accept_states


# Get the 5 tuples for the DFAs
def getDFA():
    # Load the json data
    file_dfa1 = json.load(open("dfa1.json"))
    file_dfa2 = json.load(open("dfa2.json"))

    # Get the states for each dfa. Check that at least one has states
    dfa1_states = getStates(file_dfa1)
    dfa2_states = getStates(file_dfa2)
    errorChecker.checkEmptyDFAs(dfa1_states, dfa2_states)
    errorChecker.checkDifferentStateChars(dfa1_states, dfa2_states)

    # Get the alphabet (Assumed to be common)
    alphabet = getAlphabet(file_dfa1, file_dfa2)

    # Get the transitions for each dfa
    dfa1_transitions = getTransitions(file_dfa1, alphabet, dfa1_states)
    dfa2_transitions = getTransitions(file_dfa2, alphabet, dfa2_states)

    # Get start state for each dfa
    dfa1_start_state = getStartState(file_dfa1, dfa1_states)
    dfa2_start_state = getStartState(file_dfa2, dfa2_states)

    # Get the accept states for each dfa
    dfa1_accept_states = getAcceptStates(file_dfa1, dfa1_states)
    dfa2_accept_states = getAcceptStates(file_dfa2, dfa2_states)

    # Create 5-tuple (alphabet not included)
    dfa1 = [dfa1_states, dfa1_transitions, dfa1_start_state, dfa1_accept_states]
    dfa2 = [dfa2_states, dfa2_transitions, dfa2_start_state, dfa2_accept_states]
    return dfa1, dfa2, alphabet


# Generates the set of states for the union DFA
def generateStates(dfa1, dfa2):
    # Concatenate all dfa1 states and all dfa2 states to make new set of states
    states = []
    for i in range(len(dfa1)):
        for j in range(len(dfa2)):
            state = dfa1[i] + dfa2[j]
            states.append(state)
    return states


# Creates the transitions in the DFA union
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


# Gets the start in the DFA union
def findStartState(dfa1, dfa2):
    return dfa1 + dfa2


# Gets the set of accept states in the union DFA
def findAcceptStates(dfa1_accept, dfa2_accept, union_states):
    # Find all states that contain an accept state substring
    accept_states = []

    # If neither DFA accepts return empty for set of accept states
    if dfa1_accept == [''] and dfa2_accept == ['']:
        return ['']

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


# Generates the union DFA json file
def makeUnion(dfa, alphabet):
    json_obj = {'states': []}

    # Make transition table
    for i in range(len(dfa[0])):
        transition = {'state': dfa[0][i]}
        for j in range(len(alphabet)):
            transition[alphabet[j]] = dfa[1][i][j]
        json_obj['states'].append(transition)

    # Make start state
    json_obj['start-state'] = dfa[2]

    # Make set of accept states
    json_obj['accept-states'] = []
    for i in range(len(dfa[3])):
        json_obj['accept-states'].append(({
            "state": dfa[3][i]
        }))

    # Save to json file
    with open('union_dfa.json', 'w') as jsonFile:
        json.dump(json_obj, jsonFile, indent=4)


def main():
    # Get the DFAs
    dfa1, dfa2, alphabet = getDFA()

    # Build the 5-tuple for the union dfa
    union_states = generateStates(dfa1[0], dfa2[0])
    union_transitions = addTransitions(dfa1[1], dfa2[1])
    start_state = findStartState(dfa1[2], dfa2[2])
    accept_states = findAcceptStates(dfa1[3], dfa2[3], union_states)
    union_dfa = [union_states, union_transitions, start_state, accept_states]

    # Send union dfa to json format
    makeUnion(union_dfa, alphabet)


if __name__ == "__main__":
    main()
