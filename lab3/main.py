from parser import tokenize, parse

code = '''
begin 
    a := (0-1800 + (0-56)) <> 18;
    b := (a * 2) >= (88 - 3);
    c := (0-a + 0.007) = (b * (a - 45));
    d := (100.0 / (25 + 46) - 28 * 0.001)
end
'''


def main():
    tokens = tokenize(code)
    print(tokens)
    parse(tokens)


if __name__ == '__main__':
    main()