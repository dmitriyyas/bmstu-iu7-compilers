from copy import deepcopy
import graphviz
from dfa import DFA


class MinDFA():
    dStates: dict[str, dict[str, str]]
    initialState: str
    finalStates: list[str]
    components: dict[int, list[str]]
    minDstates: dict[str, dict[str, str]]

    def __init__(self, dfa: DFA, alphabet: str):
        self.dStates = dfa.dStates
        self.alphabet = alphabet
        self.minAlphabet = self.__getMinAlphabet()
        self.__addZeroState()
        self.initialState = dfa.initialState
        self.finalStates = dfa.finalStates

        reserveEdges = self.__findReverseEdges()
        reachable = self.__getReachable()
        marked = self.__getMarked(reserveEdges)
        self.components = self.__getComponents(reachable, marked)
        self.dStates = dfa.dStates # remove zero state

        self.initialState = self.__findInitialState(dfa.initialState)
        self.finalStates = self.__findFinalStates(dfa.finalStates)
        self.minDstates = self.__findMinDstates()
    
    def __getMinAlphabet(self):
        minAlphabet: set[str] = set()
        for state in self.dStates.keys():
            for letter in self.dStates[state].keys():
                minAlphabet.add(letter)

        return minAlphabet
    
    def __addZeroState(self):
        self.dStates = deepcopy(self.dStates)
        self.dStates["0ZEROSTATE"] = {}

        for letter in self.minAlphabet:
            self.dStates["0ZEROSTATE"][letter] = "0ZEROSTATE"
        
        for state in self.dStates.keys():
            for letter in self.minAlphabet:
                if not self.dStates[state].get(letter):
                    self.dStates[state][letter] = "0ZEROSTATE"

        if len(self.minAlphabet.symmetric_difference(set(self.alphabet))) != 0:
            self.minAlphabet.add("ZEROSYMBOL")
            for state in self.dStates.keys():
                self.dStates[state]["ZEROSYMBOL"] = "0ZEROSTATE"
    
    def __findReverseEdges(self):
        reverseEdges: dict[str, dict[str, set[str]]] = {}
        for state in self.dStates:
            reverseEdges[state] = {}
        
        for state in self.dStates.keys():
            for letter, newState in self.dStates[state].items():
                if not reverseEdges[newState].get(letter):
                    reverseEdges[newState][letter] = set([state])
                else:
                    reverseEdges[newState][letter] = reverseEdges[newState][letter].union(set([state]))
        
        return reverseEdges
    
    def __getReachable(self) -> dict[str, bool]:
        reachable: dict[str, bool] = {}
        for state in self.dStates.keys():
            reachable[state] = False

        marked = []
        stack = [self.initialState]
        while len(stack) != 0:
            state = stack.pop()
            marked.append(state)
            reachable[state] = True
            for nextState in self.dStates[state].values():
                if nextState not in marked:
                    stack.append(nextState)
        
        return reachable

    def __getMarked(self, reverseEdges: dict[str, dict[str, set[str]]]) -> dict[str, dict[str, bool]]:
        marked: dict[str, dict[str, bool]] = {}
        states = list(self.dStates.keys())

        for i in states:
            marked[i] = {}
            for j in states:
                marked[i][j] = False

        queue: list[tuple[str, str]] = []
        for i in states:
            for j in states:
                if not marked[i][j] and (i in self.finalStates) != (j in self.finalStates):
                    marked[i][j], marked[j][i] = True, True
                    queue.append((i, j))
        
        while len(queue) != 0:
            u, v = queue.pop(0)
            for letter in self.minAlphabet:
                rStates = set()
                if reverseEdges[u].get(letter):
                    rStates = rStates.union(reverseEdges[u][letter])

                for r in rStates:
                    sStates = set()
                    if reverseEdges[v].get(letter):
                        sStates = sStates.union(reverseEdges[v][letter])

                    for s in sStates:
                        if not marked[r][s]:
                            marked[r][s], marked[s][r] = True, True
                            queue.append((r, s))
        
        return marked
    
    def __getComponents(self, reachable: dict[str, bool], marked: dict[str, dict[str, bool]]) -> dict[int, list[str]]:
        stateNums = {}
        total = 1
        for state in self.dStates.keys():
            if state == "0ZEROSTATE":
                stateNums[0] = state
                continue

            stateNums[total] = state
            total += 1
                
        components = [-1 for _ in range(total)]
        for i in range(total):
            if not marked[stateNums[0]][stateNums[i]]:
                components[i] = 0
        
        componentsCount = 0
        for i in range(1, total):
            if not reachable[stateNums[i]]:
                continue
            if components[i] == -1:
                componentsCount += 1
                components[i] = componentsCount
                for j in range(i + 1, total):
                    if not marked[stateNums[i]][stateNums[j]]:
                        components[j] = componentsCount
        
        componentsDict: dict[int, list[str]] = {}
        for i in range(1, total):
            if not componentsDict.get(components[i]):
                componentsDict[components[i]] = [stateNums[i]]
            else:
                componentsDict[components[i]].append(stateNums[i])

        return componentsDict



    def printGroupList(self) -> None:
        print(f"Группы состояний, полученные после минимизации ДКА:")
        for i, group in self.components.items():
            print(f"{i}: {group}")
        print()

    def printMinDFA(self) -> None:
        print(f"Минимизированный ДКА:")
        for key, value in self.minDstates.items():
            print(f"{key}: {value}")

    def buildMinDFAGraph(self, view: bool = False) -> None:
        dot = graphviz.Digraph(
            comment='Минимизированный ДКА'
        )
        dot.node("", peripheries="0")
        dot.edge("", self.initialState, label="start")

        for state in self.minDstates.keys():
            if state in self.finalStates:
                linesCount = '2'
            else:
                linesCount = '1'

            dot.node(state, peripheries=linesCount)
            for key, value in self.minDstates[state].items():
                dot.edge(state, value, label=key, constraint='true')

        dot.render('../docs/min-dfa.gv', view=view)
        dot.render('../docs/min-dfa', format='png')
    
    def __findInitialState(self, dfaInitialState: str) -> str:
        for group in self.components.values():
            if dfaInitialState in group:
                return group[0]
            
    def __findFinalStates(self, dfaFinalStates: list[str]) -> list[str]:
        finalStates = []
        for group in self.components.values():
            state = group[0]
            if state in dfaFinalStates:
                finalStates.append(state)
        
        return finalStates
    
    def __findMinDstates(self) -> dict[str, dict[str, str]]:
        minDstates: dict[str, dict[str, str]] = {}
        for group in self.components.values():
            state = group[0]
            minDstates[state] = {}
            for letter, nextState in self.dStates[state].items():
                groupIndex = self.__getGroupIndexOfState(nextState)
                minDstates[state][letter] = self.components[groupIndex][0]
        
        return minDstates

    def __getGroupIndexOfState(self, nextState: str) -> int:
        for i, group in self.components.items():
            if nextState in group:
                return i
        
        return -1
    