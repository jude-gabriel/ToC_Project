###################################################
# errorChecker.py
#
#
# Does all error checking on json input file data
#
# Author: Jude Gabriel
###################################################


# Checks if both DFAs are empty. If one is then union is just non-empty dfa
def checkEmptyDFAs(dfa1, dfa2):
    if (len(dfa1) == 0) and (len(dfa2) == 0):
        print("DFAs have no states. No transformation to do. Exiting...")
        quit()


# Make sure the DFAs use have
def checkDifferentStateChars(dfa1, dfa2):
    for i in range(len(dfa1)):
        for j in range(len(dfa2)):
            if dfa1[i] == dfa2[j]:
                print("Use different state symbols for each DFA")
                quit()
    for i in dfa1:
        if dfa1.count(i) > 1:
            print("Duplicate state symbol. Exiting...")
            quit()
    for i in dfa2:
        if dfa2.count(i) > 1:
            print("Duplicate state symbol. Exiting...")
            quit()


# Error Checks the alphabet
def checkAlphabets(l1, l2):
    # Check alphabets were found in json
    if l1 is None or l2 is None:
        print("No alphabet provided. Exiting...")
        quit()

    # Check if alphabets are common
    if l1 != l2:
        print("Alphabets are not the same! Exiting....")
        quit()

    # Error Check: Make sure alphabets do not have duplicates
    for i in l1:
        if l1.count(i) > 1:
            print("Duplicate character in alphabet. Exiting...")
            quit()

    # Check alphabets are not empty
    if not l1:
        print("Empty alphabet. Exiting....")
        quit()


# Error checks valid states
def checkValidStates(states_to_check, dfa_states):
    # Check if start state is valid
    if not isinstance(states_to_check, list):
        if states_to_check not in dfa_states:
            print("Start state not in list of states. Exiting...")
            quit()
        return

    # Check if states in transition table are valid
    if isinstance(states_to_check[0], list):
        for i in range(len(states_to_check)):
            for j in range(len(states_to_check[i])):
                if states_to_check[i][j] not in dfa_states:
                    print("State in transition table not in list of states. Exiting...")
                    quit()
        return

    # Check if accept states are valid
    if isinstance(states_to_check, list):
        if states_to_check == ['']:  # If accept states are empty then return
            return
        else:
            for i in range(len(states_to_check)):
                if states_to_check[i] not in dfa_states:
                    print("Accept states not in list of states. Exiting...")
                    quit()
            return


# Check that the transition keys and alphabet chars are the same
def checkKeys(keys, alphabet):
    if keys != alphabet:
        print("Invalid Transition Table. Need 1 transition from each state for each alphabet character")
        quit()


# Checks that order of alphabet and transitions is the same in the json file
def checkTransitions(transition_char, alphabet_char):
    if transition_char != alphabet_char:
        print("Invalid Transition Table. Please list transitions in same order as alphabet")
        print("Exiting...")
        quit()
