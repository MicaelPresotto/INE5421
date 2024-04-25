def parse_input(input_string):
    num_states = int(input_string[0])
    inital_state = input_string[1]
    final_states = set(input_string[2].replace("{", "").replace("}", "").split(','))
    alphabet = sorted(set(input_string[3].replace("{", "").replace("}", "").split(',')))
    transitions = input_string[4:]
    transition_dict = {}
    for transition in transitions:
        src, symbol, dst = transition.split(',')
        transition_dict[(src, symbol)] = dst

    return num_states, inital_state, final_states, alphabet, transition_dict

def reachable_states(initial_state, alphabet, transition_dict):
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
    return visited_states

def find_equivalent_states(final_states, states, alphabet, transition_dict):
    p = set()
    p.add(frozenset(final_states))
    p.add(frozenset(states.difference(final_states)))
    q = set()
    q.add(frozenset(final_states))
    while q:
        a = q.pop()
        for symbol in alphabet:
            x = set()
            for state in states:
                if transition_dict[(state, symbol)] in a:
                    x.add(state)
            for y in list(p):
                if x.intersection(frozenset(y)):
                    new_y1 = x.intersection(frozenset(y))
                    new_y2 = frozenset(y).difference(x)
                    p.remove(y)
                    p.add(frozenset(new_y1))
                    p.add(frozenset(new_y2))
                    if y in q:
                        q.remove((y))
                        q.add(frozenset(new_y1))
                        q.add(frozenset(new_y2))
                    else:
                        if len(frozenset(new_y1)) <= len(frozenset(new_y2)):
                            q.add(frozenset(new_y1))
                        else:
                            q.add(frozenset(new_y2))
    return p
    
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

def new_automata(equivalant_classes, alphabet, transition_dict):
    new_transition_dict = {}
    for classes in equivalant_classes:
        minor_class = sorted(classes)[0]
        for symbol in alphabet:
            if(minor_class, symbol) in transition_dict:
                dst = transition_dict[(minor_class, symbol)]
                for classes2 in equivalant_classes:
                    if dst in classes2:
                        new_transition_dict[(minor_class, symbol)] = sorted(classes2)[0]
    return new_transition_dict

def print_dfa(dfa_states, dfa_inital_state, dfa_final_states, alphabet, dfa_transitions):
    print_for_transitions = []
    print_for_final_states = []
    for final_states in dfa_final_states:
        string_builder = ''
        for state in final_states:
            string_builder += state
        print_for_final_states.append(string_builder)
    for transition in dfa_transitions:
        if dfa_transitions[transition] == []:
            continue
        string_builder = ''
        for state in transition[0]:
            string_builder += state
        string_builder += f",{transition[1]},{{{''.join(dfa_transitions[transition])}}}"
        print_for_transitions.append(string_builder)
    print(f"{len(dfa_states)};{{{''.join(sorted(dfa_inital_state))}}};{{{','.join(print_for_final_states)}}};{{{','.join(alphabet)}}};{';'.join(print_for_transitions)}")        

def find_final_states(final_states, equivalent_classes):
    new_final_states = set()
    for classes in equivalent_classes:
        minor_class = sorted(classes)[0]
        if minor_class in final_states:
            new_final_states.add(minor_class)
    return new_final_states

input_string = [x for x in input().split(';')]
num_states, inital_state, final_states, alphabet, transition_dict = parse_input(input_string)
states = get_states(transition_dict)
rec_states = reachable_states(inital_state, alphabet, transition_dict)
remove_transitions(states.difference(rec_states), alphabet, transition_dict)
dead_states = find_dead_states(final_states, rec_states, alphabet, transition_dict)
remove_transitions(states.difference(dead_states) , alphabet, transition_dict)
p = find_equivalent_states(final_states, dead_states, alphabet, transition_dict)
p.remove(frozenset())
new_transition_dict = new_automata(p, alphabet, transition_dict)
new_transition_dict = dict(sorted(new_transition_dict.items()))
new_final_states = find_final_states(final_states, p)
print_dfa(p, inital_state, new_final_states, alphabet, new_transition_dict)
