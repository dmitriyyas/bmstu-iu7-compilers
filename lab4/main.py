from parser import parse

code = '''
begin 
    a := (0-800 + (0-56)) <> 34;
    b := (a * 2) >= (88 - 3);
    c := (0-a + 0.003) = (b * (a - 28));
    d := (50.0 / (12 + 98) - 48 * 0.002);
end
'''

tests = [
    (
        '(0-800 + (0-56)) <> 34',
        '0 800 - 0 56 - + 34 <>',
    ),
    (
        '(a * 2) >= (88 - 3)',
        'a 2 * 88 3 - >=',
    ),
    (
        '(0-a + 0.003) = (b * (a - 28))',
        '0 a - 0.003 + b a 28 - * =',
    ),
    (
        '(50.0 / (12 + 98) - 48 * 0.002)',
        '50.0 12 98 + / 48 0.002 * -',
    ),
    (
        '(a + b) * c',
        'a b + c *',
    ),
]


def main():
    for test in tests:
        print("\n")
        parse(test)


if __name__ == '__main__':
    main()