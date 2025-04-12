from grammar import Grammar, reedGrammarFromFile


INPUT_FILE_NAME = "./input.txt"
OUTPUT_FILE_NAME = "./result.txt"


def main():
    grammar: Grammar = reedGrammarFromFile(INPUT_FILE_NAME)
    print("Исходная грамматика:")
    grammar.printGrammar()

    grammar.removeChainRules()
    print("Грамматика после устранения цепных правил:")
    grammar.printGrammar()

    grammar: Grammar = reedGrammarFromFile(INPUT_FILE_NAME)
    grammar.removeLeftRecursion()
    print("Грамматика после устранения левой рекурсии:")
    grammar.printGrammar()

    grammar.leftFactorization()
    print("Грамматика после левой факторизации:")
    grammar.printGrammar()


if __name__ == '__main__':
    main()