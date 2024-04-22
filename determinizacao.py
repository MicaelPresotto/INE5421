def parse_input(input_string):
    num_states = int(input_string[0])
    inital_state = input_string[1]
    final_states = set(input_string[2].split(','))
    alphabet = sorted(set(input_string[3].replace("{", "").replace("}", "").split(',')))
    transitions = input_string[4:]

    transition_dict = {}
    for transition in transitions:
        src, symbol, dst = transition.split(',')
        if (src, symbol) not in transition_dict:
            transition_dict[(src, symbol)] = {dst}
        else:
            transition_dict[(src, symbol)].add(dst)

    return num_states, inital_state, final_states, alphabet, transition_dict

def epsilon_closure(states, transition_dict):
    closure = set(states)
    queue = list(states)
    while queue:
        state = queue.pop()
        if (state, '&') in transition_dict:
            for dest in transition_dict[(state, '&')]:
                if dest not in closure:
                    closure.add(dest)
                    queue.append(dest)
    return sorted(closure)

def nfa_to_dfs(initial_state, final_states, alphabet, transition_dict):
    alphabet.remove('&') if '&' in alphabet else None
    dfa_states = set()
    dfa_transitions = {}
    dfa_inital_state = epsilon_closure(initial_state, transition_dict)
    dfa_states.add(tuple(sorted(dfa_inital_state)))
    stack = [tuple(sorted(dfa_inital_state))]
    while stack:
        current_state = stack.pop(0)
        if current_state == tuple():
            continue
        for symbol in alphabet:
            new_state = set()
            for state in current_state:
                if (state, symbol) in transition_dict:
                    new_state.update(transition_dict[(state, symbol)])
            new_state = epsilon_closure(new_state, transition_dict)
            new_state = tuple(sorted(new_state))

            dfa_transitions[(current_state, symbol)] = sorted(set(new_state))

            if new_state not in dfa_states:
                dfa_states.add(new_state) if new_state else None
                stack.append(new_state)

    dfa_final_states = set()
    final_states = tuple(sorted(final_states))
    for state in dfa_states:
        for final_state in final_states:
            final_state = final_state.replace('}', '').replace('{', '')
            if final_state in state:
                dfa_final_states.add(state)
    
    return dfa_states, dfa_inital_state, dfa_final_states, alphabet, dfa_transitions


def print_dfa(dfa_states, dfa_inital_state, dfa_final_states, alphabet, dfa_transitions):
    print_for_transitions = []
    for transition in dfa_transitions:
        if dfa_transitions[transition] == []:
            continue
        string_builder = '{'
        for state in transition[0]:
            string_builder += state
        string_builder += '}'
        string_builder += f",{transition[1]},{{{''.join(dfa_transitions[transition])}}}"
        print_for_transitions.append(string_builder)
    print(f"{len(dfa_states)};{{{''.join(dfa_inital_state)}}};{{{','.join(dfa_final_states)}}};{{{','.join(alphabet)}}};{';'.join(print_for_transitions)}")
                
            
input_string = [x for x in input().split(';')]
num_states, inital_state, final_states, alphabet, transition_dict = parse_input(input_string)
dfa_states, dfa_inital_state, dfa_final_states, alphabet, dfa_transitions = nfa_to_dfs(inital_state, final_states, alphabet, transition_dict)
true_final_states = []
dfa_final_states = sorted(dfa_final_states)
dfa_transitions = dict(sorted(dfa_transitions.items()))
for final_states in dfa_final_states:
    string_builder = '{'
    for state in final_states:
        string_builder += state
    true_final_states.append(string_builder+'}')
print_dfa(dfa_states, dfa_inital_state, true_final_states, alphabet, dfa_transitions)
