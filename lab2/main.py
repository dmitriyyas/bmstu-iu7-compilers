from grammar import Grammar, reedGrammarFromFile


INPUT_FILE_NAME = "./input.txt"
OUTPUT_FILE_NAME = "./result.txt"


def main():
    grammar: Grammar = reedGrammarFromFile(INPUT_FILE_NAME)
    grammar.removeLeftRecursion()
    print("Грамматика после устранения левой рекурсии:")
    grammar.printGrammar()

    grammar: Grammar = reedGrammarFromFile(INPUT_FILE_NAME)
    grammar.removeChainRules()
    print("Грамматика после устранения цепных правил:")
    grammar.printGrammar()


if __name__ == '__main__':
    main()