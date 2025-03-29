from regularExpression import convertRegexToDesiredFormat, ALPHABET
from parseTree import ParseTree
from dfa import DFA
from minDfa import MinDFA
from chain import inputAndCheckChain


MSG = f"""
    Меню\n
    1. Синтаксическое дерево для регулярного выражения;
    2. ДКА для регулярного выражения;
    3. Минимизированный ДКА;
    4. Проверка входной цепочки на соответсвие регулярному выражению;

    0. Выход.\n
    Выбор: """


def inputOption():
    try:
        option = int(input(MSG))
    except:
        option = -1
    
    if option < 0 or option > 4:
        print("\nОжидался ввод целого числа от 0 до 4")

    return option


def main():
    regex = input(f"\nВведите регулярное выражение: ")
    convertedRegex = convertRegexToDesiredFormat(regex)
    if convertedRegex is None:
        return

    parseTree = ParseTree(convertedRegex)
    dfa = DFA(parseTree)
    minDFA = MinDFA(dfa, ALPHABET)

    option = -1
    while option != 0:
        option = inputOption()
        match option:
            case 1:
                parseTree.buildGraph(view=True)
            case 2:
                dfa.buildDFAGraph(view=True)
            case 3:
                minDFA.buildMinDFAGraph(view=True)
            case 4:
                inputAndCheckChain(regex, minDFA)


if __name__ == '__main__':
    main()
