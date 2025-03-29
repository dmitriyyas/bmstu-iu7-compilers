#from typing import Self
import graphviz
from pythonds.basic.stack import Stack
from regularExpression import findClosingBracketIndex


class Node:
    nodeNumber: int | None
    letterNumber: int | None
    value: str | None
    #leftChild: Self | None
    #rightChild: Self | None
    nullable: bool
    firstpos: set[int]
    lastpos: set[int]

    def __init__(self, leftNode = None, rightNode = None) -> None:
        self.nodeNumber = None
        self.letterNumber = None
        self.value = None
        self.leftChild = leftNode
        self.rightChild = rightNode

        self.nullable = False
        self.firstpos = set()
        self.lastpos = set()


class ParseTree:
    followpos: dict[int, set]
    letterNumbers: dict[int, str]
    root: Node

    def __init__(self, regex: str) -> None:
        self.followpos = dict()
        self.letterNumbers = dict()
        self.root = self.__buildTree(regex)

    def printTree(self) -> None:
        print(f"Синтаксическое дерево для регулярного выражения:")
        self.__printNode(self.root)
        print("\n")

    def buildGraph(self, view: bool = False) -> None:
        dot = graphviz.Digraph(
            comment='Синтаксическое дерево для регулярного выражения'
        )
        self.__addNodeToGraph(self.root, dot)
        dot.render('../docs/parse-tree.gv', view=view)
    
    def __buildTree(self, regex: str) -> Node:
        root, _, _ = self.__buildTreeRecursion(regex=regex, nodeNumber=0, letterNumber=0)
        if root.value is None:
            root = root.leftChild

        return root
    
    def __buildTreeRecursion(self, regex: str, nodeNumber: int, letterNumber: int) -> list[Node, int, int]:
        nodeStack = Stack()
        curNode = Node()

        i = 0
        while i < len(regex):
            symbol = regex[i]
            if nodeStack.isEmpty():
                root = Node(leftNode=curNode)
                nodeStack.push(root)

            if symbol == '(':
                closingBracketIndex = findClosingBracketIndex(regex, i)
                subtreeRoot, nodeCount, letterCount = self.__buildTreeRecursion(
                    regex=regex[i + 1: closingBracketIndex],
                    nodeNumber=nodeNumber,
                    letterNumber=letterNumber
                )

                if subtreeRoot.value is None:
                    subtreeRoot = subtreeRoot.leftChild

                curNode.leftChild = subtreeRoot.leftChild
                curNode.rightChild = subtreeRoot.rightChild
                curNode.value = subtreeRoot.value
                curNode.nodeNumber = subtreeRoot.nodeNumber
                curNode.letterNumber = subtreeRoot.letterNumber

                nodeNumber = nodeCount
                letterNumber = letterCount
                i = closingBracketIndex
                curNode = nodeStack.pop()
                
            elif symbol not in ['.', '|', '*', ')']:
                nodeNumber += 1
                letterNumber += 1
                curNode.nodeNumber = nodeNumber
                curNode.letterNumber = letterNumber
                curNode.value = symbol
                self.letterNumbers[letterNumber] = symbol
                self.followpos[letterNumber] = set()
                curNode = nodeStack.pop()

            elif symbol in ['.', '|']:
                if curNode.value is not None:
                    curNode = nodeStack.pop()
                nodeNumber += 1
                curNode.nodeNumber = nodeNumber
                curNode.value = symbol
                curNode.rightChild = Node()
                nodeStack.push(curNode)
                curNode = curNode.rightChild

            elif symbol == '*':
                if curNode.value is not None:
                    curNode = nodeStack.pop()
                nodeNumber += 1
                curNode.nodeNumber = nodeNumber
                curNode.value = symbol
                curNode.nullable = True

            i += 1
        
        return root, nodeNumber, letterNumber
    
    def __printNode(self, node: Node, end: str = ' ') -> None:
        if node is not None:
            if node.leftChild:
                print('(', end=end)
                self.__printNode(node.leftChild)

            print(node.value, end=end)

            if node.rightChild:
                self.__printNode(node.rightChild)
                print(')', end=end)
            elif node.leftChild:
                print(')', end=end)

    def __addNodeToGraph(self, node: Node, dot: graphviz.Digraph) -> None:
        if node is not None:
            if node.leftChild:
                self.__addNodeToGraph(node.leftChild, dot)
                dot.edge(str(node.nodeNumber), str(node.leftChild.nodeNumber))

            inner = f", {node.letterNumber}" if node.letterNumber else ""
            dot.node(
                name=str(node.nodeNumber), 
                label=f"{node.value}{inner}"
            )

            if node.rightChild:
                self.__addNodeToGraph(node.rightChild, dot)
                dot.edge(str(node.nodeNumber), str(node.rightChild.nodeNumber))
