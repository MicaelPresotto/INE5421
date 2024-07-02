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
    firsts = {}
    for head in grammar.keys():
        firsts[head] = set()
    for head, body in grammar.items():
        for symbol in body:
            for char in symbol:
                if is_terminal(char) or char == '&':
                    firsts[head].add(char)
                    break
                else:
                    if firsts[char]:
                        if "&" in firsts[char]:
                            firsts[head].update(firsts[char])
                            firsts[head].remove("&")
                        else:
                            firsts[head].update(firsts[char])
                            break
                    else:
                        firsts[char].update(calculate_first(grammar, char))
                        if "&" in firsts[char]:
                            firsts[head].update(firsts[char])
                            firsts[head].remove("&")
                        else:
                            firsts[head].update(firsts[char])
                            break
    while True:
        firsts_copy = deepcopy(firsts)
        firsts = define_epsilon(grammar, firsts)
        if firsts == firsts_copy:
            break

    return firsts

def calculate_first(grammar:dict, char:str):
    first = set()
    for body in grammar[char]:
        for symbol in body:
            if is_terminal(symbol) or symbol == '&':
                first.add(symbol)
                break
            else:
                first.update(calculate_first(grammar, symbol))
    return first

def define_epsilon(grammar: dict, firsts_follows: dict):
    for i, (head, body) in enumerate(grammar.items()):
        for symbol in body:
            for i, char in enumerate(symbol):
                if is_terminal(char) or char == "&":
                    break
                else:
                    if "&" in firsts_follows[char]:
                        if i == len(symbol) - 1:
                            firsts_follows[head].add("&")
                        else:
                            continue
                    else:
                        break
    return firsts_follows

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
