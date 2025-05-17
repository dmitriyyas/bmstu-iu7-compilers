from parser import tokenize, parse

code = '''
begin 
    a := (0-800 + (0-56)) <> 34;
    b := (a * 2) >= (88 - 3);
    c := (0-a + 0.003) = (b * (a - 28));
    d := (50.0 / (12 + 98) - 48 * 0.002);
end
'''


def main():
    tokens = tokenize(code)
    print(tokens)
    parse(tokens)


if __name__ == '__main__':
    main()