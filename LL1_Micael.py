from copy import deepcopy

input_string = [x for x in input().split(';')]
input_string.remove('')
def parseInput(input_string):
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

def calculateFirsts(grammar: dict):
    firsts = {head: set() for head in grammar}
    while True:
        first_copy = deepcopy(firsts)
        for head, body in grammar.items():
            for production in body:
                for i, char in enumerate(production):
                    if isTerminal(char) or char == "&":
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

def calculateFollows(grammar: dict, firsts: dict):
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
                    if isTerminal(char) or char == "&": 
                        continue
                    else:
                        if i == len(symbol) - 1:
                            for c in symbol[::-1]:
                                if isTerminal(c):
                                    break
                                follows[c].update(follows[head])
                                if "&" not in firsts[c]: break
                        else:
                            for j in symbol[i+1:]:
                                if isTerminal(j):
                                    follows[char].add(j)
                                    break
                                follows[char].update(firsts[j])
                                follows[char].discard("&")
                                if "&" not in firsts[j]: break        
        if follows == follows_copy:
            break
    return follows

def isTerminal(symbol):
    return symbol.islower()

def getProductionFirsts(production:str, firsts:dict):
    body_firsts = set()
    for i,symbol in enumerate(production):
        if isTerminal(symbol) and i==0 or symbol=="&":
            return {symbol}
        if not isTerminal(symbol) and i==0 and "&" not in firsts[symbol]:
            return firsts[symbol]
        body_firsts.update(firsts[symbol])
        body_firsts.discard("&")
        for char in production[1:]:
            if isTerminal(char):
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
        if isTerminal(char) or char=="&":
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
            body_firsts = getProductionFirsts(production, firsts)
            for symbol in body_firsts:
               if symbol == "&":
                   for f in follows[head]:
                       ll1ParsingTable.add(tuple([head,f, i]))
               else:
                    ll1ParsingTable.add(tuple([head,symbol, i]))
    return list(ll1ParsingTable)

def isFactored(grammar: dict, firsts: dict):
    for body in grammar.values():
        elements = []
        for production in body:
            body_firsts = getProductionFirsts(production, firsts)
            if "&" in body_firsts:
                body_firsts.remove("&")
            for i in body_firsts:
                elements.append(i)
        if len(elements) != len(set(elements)):
            return False            
    return True

def isLeftRecursive(grammar: dict, firsts: dict):
    # direct left recursion
    heads_reached_dict = {head: set() for head in grammar}
    for head,body in grammar.items():
        for production in body:
            for c in production:
                if c == head:
                    return True
                if isTerminal(c) or c == "&":
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
 
def hasConflictFirstAndFollows(firsts: dict, follows: dict, heads: list):
    for head in heads:
        first = firsts[head]
        follow = follows[head]
        if '&' in first and set(first) & set(follow) != set():
            return False
    return True

def printFormatted(start: str, heads : list, ll1_table: list, terminals: list):
    print(f"\x7B{','.join(sorted(heads))}\x7D", end=",")
    print(start, end=",")
    custom_sort = lambda c: 123 if c == "$" else ord(c)
    print(f"\x7B{','.join(sorted(terminals, key= custom_sort))}\x7D", end=";")
    ll1_table.sort(key = lambda l: l[2])
    ll1_table.sort(key = lambda l: custom_sort(l[1]))
    ll1_table.sort(key = lambda l: l[0])
    for item in ll1_table: print(f"[{item[0]},{item[1]},{item[2]}]", end="")

def main():
    grammar = parseInput(input_string)

    firsts_of_grammar = calculateFirsts(grammar)
    follows_of_grammar = calculateFollows(grammar, firsts_of_grammar)

    if not isFactored(grammar, firsts_of_grammar):
        print("The grammar is not factored")
        return
    if isLeftRecursive(grammar, firsts_of_grammar):
        print("The grammar is left recursive")
        return

    if not hasConflictFirstAndFollows(firsts_of_grammar, follows_of_grammar, list(grammar.keys())):
        print("The grammar has a conflict between firsts and follows")
        return
    
    terminals = set([char for body in grammar.values() for production in body for char in production if isTerminal(char)]).union({"$"})

    ll1Table = getLL1ParsingTable(firsts_of_grammar, follows_of_grammar, grammar)
    printFormatted(list(grammar.keys())[0], list(grammar.keys()), ll1Table, terminals)

main()