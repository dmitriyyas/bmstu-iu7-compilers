import graphviz
from parseTree import ParseTree, Node


class DFA:
    parseTree: ParseTree
    followpos: dict[int, set]
    letterNumbers: dict[int, str]
    initialState: str
    dstates: dict[str, dict[str, str]]
    finalStates: list[str]

    def __init__(self, parseTree: ParseTree | None):
        if parseTree:
            self.root = parseTree.root
            self.followpos = parseTree.followpos
            self.letterNumbers = parseTree.letterNumbers

            self.__completeTree(self.root)
            self.initialState = self.__convertSetToString(self.root.firstpos)
            self.dStates = self.__findDStates()
            self.finalStates = self.__findFinalStates()
        else:
            self.initialState = "A"
            self.dStates = {
                "A": {"0": "B", "1": "C"},
                "B": {"0": "E", "1": "F"},
                "C": {"0": "A", "1": "A"},
                "D": {"0": "F", "1": "E"},
                "E": {"0": "D", "1": "F"},
                "F": {"0": "D", "1": "E"},
            }
        
            self.finalStates = ["E", "F"]

    def printFirstposLastpos(self) -> None:
        print(f"Значения функций firstpos и lastpos в узлах синтаксического дерева для регулярного выражения:")
        self.__printNode(self.root)
        print("\n")

    def printFollowpos(self) -> None:
        print(f"Ориентированный граф для функции followpos:")
        for key, value in self.followpos.items():
            print(f"{key}: {value}")
        print()

    def printDFA(self) -> None:
        print(f"ДКА для регулярного выражения:")
        for key, value in self.dStates.items():
            print(f"{key}: {value}")
        print()

    def buildFirstposLastposGraph(self, view: bool = False) -> None:
        dot = graphviz.Digraph(
            comment='Значения функций firstpos и lastpos в узлах синтаксического дерева для регулярного выражения'
        )
        self.__addNodeToGraph(self.root, dot)
        dot.render('../docs/firstpos-lastpos.gv', view=view)

    def buildFollowposGraph(self, view: bool = False) -> None:
        dot = graphviz.Digraph(
            comment='Ориентированный граф для функции followpos'
        )
        for i in self.followpos:
            dot.node(str(i))
            for j in self.followpos[i]:
                dot.edge(str(i), str(j))

        dot.render('../docs/followpos.gv', view=view)

    def buildDFAGraph(self, view: bool = False) -> None:
        dot = graphviz.Digraph(
            comment='ДКА для регулярного выражения'
        )
        dot.node("", peripheries="0")
        dot.edge("", self.initialState, label="start")
        for state in self.dStates.keys():
            if state in self.finalStates:
                linesCount = '2'
            else:
                linesCount = '1'

            dot.node(state, peripheries=linesCount)
            for key, value in self.dStates[state].items():
                dot.edge(state, value, label=key, constraint='true')

        dot.render('../docs/dfa.gv', view=view)
        dot.render('../docs/dfa', format='png')

    def __printNode(self, node: Node, end: str = ' ') -> None:
        if node is not None:
            if node.leftChild:
                print('(', end=end)
                self.__printNode(node.leftChild)

            print(f"{node.firstpos} {node.value} {node.lastpos}", end=end)

            if node.rightChild:
                self.__printNode(node.rightChild)
                print(')', end=end)
            elif node.leftChild:
                print(')', end=end)

    def __completeTree(self, node: Node) -> None:
        if node is not None:
            if node.leftChild:
                self.__completeTree(node.leftChild)
            if node.rightChild:
                self.__completeTree(node.rightChild)

            node.nullable = self.__calcNullable(node)
            node.firstpos = self.__calcFirstpos(node)
            node.lastpos = self.__calcLastpos(node)

            if node.value == '.':
                for i in node.leftChild.lastpos:
                    for j in node.rightChild.firstpos:
                        self.followpos[i].add(j)
            elif node.value == '*':
                for i in node.lastpos:
                    for j in node.firstpos:
                        self.followpos[i].add(j)

    def __calcNullable(self, node: Node) -> bool:
        if node.value == '|':
            nullable = node.leftChild.nullable or node.rightChild.nullable
        elif node.value == '.':
            nullable = node.leftChild.nullable and node.rightChild.nullable
        elif node.value == '*':
            nullable = True
        else:
            nullable = False

        return nullable

    def __calcFirstpos(self, node: Node) -> set:
        if node.value == '|':
            firstpos = node.leftChild.firstpos.union(node.rightChild.firstpos)
        elif node.value == '.':
            firstpos = node.leftChild.firstpos.union(node.rightChild.firstpos) if node.leftChild.nullable else node.leftChild.firstpos
        elif node.value == '*':
            firstpos = node.leftChild.firstpos
        else:
            firstpos = {node.letterNumber}

        return firstpos

    def __calcLastpos(self, node: Node) -> set:
        if node.value == '|':
            lastpos = node.leftChild.lastpos.union(node.rightChild.lastpos)
        elif node.value == '.':
            lastpos = node.leftChild.lastpos.union(node.rightChild.lastpos) if node.rightChild.nullable else node.rightChild.lastpos
        elif node.value == '*':
            lastpos = node.leftChild.lastpos
        else:
            lastpos = {node.letterNumber}

        return lastpos
    
    def __addNodeToGraph(self, node: Node, dot: graphviz.Digraph) -> None:
        if node is not None:
            if node.leftChild:
                self.__addNodeToGraph(node.leftChild, dot)
                dot.edge(str(node.nodeNumber), str(node.leftChild.nodeNumber))

            inner = f", {node.letterNumber}" if node.letterNumber else ""
            dot.node(
                name=str(node.nodeNumber), 
                label=f"{node.firstpos}  {node.value}{inner}  {node.lastpos}"
            )

            if node.rightChild:
                self.__addNodeToGraph(node.rightChild, dot)
                dot.edge(str(node.nodeNumber), str(node.rightChild.nodeNumber))

    def __findDStates(self) -> dict[str, dict[str, str]]:
        dStates: dict[str, dict[str, str]] = {}
        unmarkedStates = [self.initialState]
        while len(unmarkedStates) > 0:
            state = unmarkedStates.pop()
            dStates[state] = {}
            for i in state.split(','):
                i = int(i)
                if self.letterNumbers[i] == '#':
                    continue
                elif not dStates[state].get(self.letterNumbers[i]):
                    dStates[state][self.letterNumbers[i]] = self.followpos[i]
                else:
                    dStates[state][self.letterNumbers[i]] = self.followpos[i].union(dStates[state][self.letterNumbers[i]])
            
            for letter, nextState in dStates[state].items():
                nextState = self.__convertSetToString(nextState)
                dStates[state][letter] = nextState
                if nextState not in dStates and nextState not in unmarkedStates:
                    unmarkedStates.append(nextState)
        
        return dStates
    
    def __findFinalStates(self) -> list[str]:
        finalStates = []
        for state in self.dStates.keys():
            for i in state.split(','):
                if int(i) == self.root.rightChild.letterNumber:
                    finalStates.append(state)
                    break
        
        return finalStates
    
    def __convertSetToString(self, item: set) -> str:
        item = list(item)
        item.sort()
        itemStr = ""
        for i in item:
            itemStr += f"{i},"
        
        return itemStr[:-1]
