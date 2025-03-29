from minDfa import MinDFA


def checkChain(chain: str, minDfa: MinDFA) -> bool:
    state = minDfa.initialState
    for symbol in chain:
        nextState = minDfa.minDstates[state].get(symbol)
        if nextState:
            print(f"{symbol}: {state} -> {nextState}")
            state = nextState
        else:
            print(f"{symbol}: {state} -> нет состояния")
            return False
    
    if state not in minDfa.finalStates:
        print(f"Состояние '{state}' не является конечным")
        return False
    
    return True


def inputAndCheckChain(regex: str, minDFA: MinDFA) -> None:
    chain = input(f"\nВходная цепочку для проверки на соответсвие регулярному выражению '{regex}': ")
    if checkChain(chain, minDFA):
        print(f"\n'{chain}' соответствует '{regex}'")
    else:
        print(f"\n'{chain}' не соответствует '{regex}'")