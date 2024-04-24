def parse_input(input_string):
    num_states = int(input_string[0])
    inital_state = input_string[1]
    final_states = set(input_string[2].split(','))
    alphabet = sorted(set(input_string[3].replace("{", "").replace("}", "").split(',')))
    transitions = input_string[4:]

    transition_dict = {}
    for transition in transitions:
        src, symbol, dst = transition.split(',')
        transition_dict[(src, symbol)] = dst

    return num_states, inital_state, final_states, alphabet, transition_dict

def reachable_states(initial_state, states, alphabet, transition_dict):
    reachable_states = set(inital_state)
    queue = [initial_state]
    while queue:
        state = queue.pop(0)
        for symbol in alphabet:
            if (state, symbol) in transition_dict:
                next_state = transition_dict[(state, symbol)]
                if next_state not in reachable_states:
                    reachable_states.add(next_state)
                    queue.append(next_state)
    remove_transitions(states - reachable_states, alphabet, transition_dict)
    return reachable_states

def find_dead_states(final_states, states, alphabet, transition_dict):
    visited_states = set()
    queue = [state for state in final_states]
    while queue:
        current_state = queue.pop(0)
        for state in states:
         for symbol in alphabet:
            if transition_dict[(state, symbol)] == current_state:
                if state not in visited_states:
                    visited_states.add(state)
                    queue.append(state)
    remove_transitions(states - visited_states , alphabet, transition_dict)
    return visited_states
                
def minimize_dfa(initial_state, final_states, states, alphabet, transition_dict):
    partition = [final_states, states - final_states]
    new_partition = []
    #todo


def remove_transitions(states, alphabet, transition_dict):
    for state in states:
        for symbol in alphabet:
            if (state, symbol) in transition_dict:
                del transition_dict[(state, symbol)]

def get_states(transition_dict):
    states = set()
    for key in transition_dict.keys():
        states.add(key[0])
        states.add(transition_dict[key])
    return states

input_string = [x for x in input().split(';')]
num_states, inital_state, final_states, alphabet, transition_dict = parse_input(input_string)
states = get_states(transition_dict)
rec_states = reachable_states(inital_state, states, alphabet, transition_dict)
dead_states = find_dead_states(final_states, rec_states, alphabet, transition_dict)
minimized_num_states, minimized_initial_state, minimized_final_states, minimized_alphabet, minimized_transition_dict = minimize_dfa(inital_state, final_states, rec_states, alphabet, transition_dict)
print(minimized_transition_dict)