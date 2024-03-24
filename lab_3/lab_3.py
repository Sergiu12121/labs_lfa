import re

TOKENS = [
    ("NUMBER", r"\d+"),
    ("PLUS", r"\+"),
    ("MINUS", r"-"),
    ("TIMES", r"\*"),
    ("DIVIDE", r"/"),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("WHITESPACE", r"\s+"),
    ("ERROR", r"."),
]


def lexer(input_string):
    tokens = []
    while input_string:
        match = None
        for token_type, pattern in TOKENS:
            regex = re.compile(pattern)
            match = regex.match(input_string)
            if match:
                value = match.group(0)
                if token_type != "WHITESPACE":
                    tokens.append((token_type, value))
                input_string = input_string[match.end() :]
                break
        if not match:
            print("Invalid character:", input_string[0])
            input_string = input_string[1:]

    return tokens


input_string = "3 + 4 * 2 / (1 - 5)"
tokens = lexer(input_string)
print(tokens)
