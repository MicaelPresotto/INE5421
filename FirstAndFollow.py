from copy import deepcopy

input_string = [x for x in input().split(';')]
input_string.remove('')
def parse_input(input_string):
    grammar = {}
    for i in input_string:
        i.replace(' ', '')
        head, body = i.split('=')
        head = head.strip()
        body = body.strip()
        if head not in grammar:
            grammar[head] = []
        grammar[head].append(body)
    return grammar

def print_formatted(firsts : dict, follows : dict, heads : list):
    for i, head in enumerate(heads):
        print(f"First({head}) = \x7B{', '.join(custom_sort(firsts[head]))}\x7D", end='; ')
    for i, head in enumerate(heads):
        print(f"Follow({head}) = \x7B{', '.join(custom_sort(follows[head]))}\x7D", end=f";{(1 - (i // len(follows[head]) - 1)) * ' '}")

def custom_sort(lst: dict) -> list:
    new_lst = list(lst.copy())
    new_lst.sort()
    for c in ["&", "$"]:
        if c in new_lst: 
            new_lst.remove(c)
            new_lst.append(c)
    return new_lst

def calculate_firsts(grammar: dict):
    firsts = {head: set() for head in grammar}
    while True:
        first_copy = deepcopy(firsts)
        for head, body in grammar.items():
            for production in body:
                for i, char in enumerate(production):
                    if is_terminal(char) or char == "&":
                        firsts[head].add(char)
                        break
                    firsts[head].update(firsts[char])
                    if i < len(production) - 1:
                        firsts[head].discard("&")
                    if "&" not in firsts[char]:
                        break
        if firsts == first_copy:
            break
    return firsts

def calculate_follows(grammar: dict, firsts: dict):
    follows = {}
    for i,head in enumerate(grammar.keys()):
        follows[head] = set()
        if i == 0:
            follows[head].add("$")
    while True:
        follows_copy = deepcopy(follows)
        for head, body in grammar.items():
            for symbol in body:
                for i, char in enumerate(symbol):
                    if is_terminal(char) or char == "&": 
                        continue
                    else:
                        if i == len(symbol) - 1:
                            for c in symbol[::-1]:
                                if is_terminal(c):
                                    break
                                follows[c].update(follows[head])
                                if "&" not in firsts[c]: break
                        else:
                            for j in symbol[i+1:]:
                                if is_terminal(j):
                                    follows[char].add(j)
                                    break
                                follows[char].update(firsts[j])
                                follows[char].discard("&")
                                if "&" not in firsts[j]: break        
        if follows == follows_copy:
            break
    return follows

def is_terminal(symbol):
    return symbol.islower()

grammar = parse_input(input_string)
firsts_of_grammar = calculate_firsts(grammar)
follows_of_grammar = calculate_follows(grammar, firsts_of_grammar)
print_formatted(firsts_of_grammar, follows_of_grammar, list(grammar.keys()))
