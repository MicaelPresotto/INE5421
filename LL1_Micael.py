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

def getBodyFirst(production:str, firsts:dict):
    body_firsts = set()
    for i,symbol in enumerate(production):
        if is_terminal(symbol) and i==0 or symbol=="&":
            return {symbol}
        if not is_terminal(symbol) and i==0 and "&" not in firsts[symbol]:
            return firsts[symbol]
        body_firsts.update(firsts[symbol])
        body_firsts.discard("&")
        for char in production[1:]:
            if is_terminal(char):
                body_firsts.add(char)
                return body_firsts
            if "&" in firsts[char]:
                body_firsts.update(firsts[char])
                body_firsts.discard("&")
                continue
            body_firsts.update(firsts[char])
            return body_firsts
    count_epsilon = 0
    for char in production:
        if is_terminal(char) or char=="&":
            break
        else:
            if "&" in firsts[char]:
                count_epsilon+=1
                continue
            else:
                break
    if count_epsilon==len(production):
        body_firsts.add("&")

    return body_firsts

def getLL1ParsingTable(firsts: dict, follows:dict, grammar:dict):
    ll1ParsingTable = set()
    i = 0
    for head,body in grammar.items():
        for production in body:
            i+=1
            body_firsts = getBodyFirst(production, firsts)
            for symbol in body_firsts:
               if symbol == "&":
                   for f in follows[head]:
                       ll1ParsingTable.add(tuple([head,f, i]))
               else:
                    ll1ParsingTable.add(tuple([head,symbol, i]))
    return list(ll1ParsingTable)

def is_factored(grammar: dict, firsts: dict):
    for head, body in grammar.items():
        elements = []
        for production in body:
            body_firsts = getBodyFirst(production, firsts)
            if "&" in body_firsts:
                body_firsts.remove("&")
            for i in body_firsts:
                elements.append(i)
        if len(elements) != len(set(elements)):
            return False            
    return True

def is_left_recursive(grammar: dict, firsts: dict) -> bool:
    # direct left recursion
    heads_reached_dict = {head: set() for head in grammar}
    for head,body in grammar.items():
        for production in body:
            for c in production:
                if c == head:
                    return True
                if is_terminal(c) or c == "&":
                    break
                heads_reached_dict[head].add(c)
                if "&" not in firsts[c]:
                    break
                
    for head in heads_reached_dict: # indirect left recursion
        to_expand = heads_reached_dict[head]
        already_expanded = set()
        while len(to_expand):
            head_reached = to_expand.pop()
            already_expanded.add(head_reached)
            if head_reached == head:
                return True
            for h in heads_reached_dict[head_reached]:
                if h not in already_expanded:
                    to_expand.add(h)
    return False
 
def firstAndFollowsConflictOk(firsts: dict, follows: dict, heads: list):
    for head in heads:
        first = firsts[head]
        follow = follows[head]
        if '&' in first and set(first) & set(follow) != set():
            return False
    return True

def print_formatted(start: str, heads : list, ll1_table: list, terminals: list):
    print(f"\x7B{','.join(sorted(heads))}\x7D", end=",")
    print(start, end=",")
    custom_sort = lambda c: 123 if c == "$" else ord(c)
    print(f"\x7B{','.join(sorted(terminals, key= custom_sort))}\x7D", end=";")
    ll1_table.sort(key = lambda l: l[2])
    ll1_table.sort(key = lambda l: custom_sort(l[1]))
    ll1_table.sort(key = lambda l: l[0])
    for item in ll1_table: print(f"[{item[0]},{item[1]},{item[2]}]", end="")

def main():
    grammar = parse_input(input_string)

    firsts_of_grammar = calculate_firsts(grammar)
    follows_of_grammar = calculate_follows(grammar, firsts_of_grammar)

    if not is_factored(grammar, firsts_of_grammar):
        print("The grammar is not factored")
        return
    if is_left_recursive(grammar, firsts_of_grammar):
        print("The grammar is left recursive")
        return

    if not firstAndFollowsConflictOk(firsts_of_grammar, follows_of_grammar, list(grammar.keys())):
        print("The grammar has a conflict between firsts and follows")
        return
    
    terminals = set([char for body in grammar.values() for production in body for char in production if is_terminal(char)]).union({"$"})

    ll1Table = getLL1ParsingTable(firsts_of_grammar, follows_of_grammar, grammar)
    print_formatted(list(grammar.keys())[0], list(grammar.keys()), ll1Table, terminals)

main()
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