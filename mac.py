import random


def tokenize_regex(pattern):
    triggers = ["*", "+", "?", "^"]
    tokens = []
    elements = pattern.replace("(", " (").replace(")", ") ").split()

    for element in elements:
        if element in triggers:
            tokens[-1] = (element, tokens[-1][1])
        elif "|" in element:
            parts = element.strip("()").split("|")
            last_char = element[-1]
            count = last_char if last_char in "0123456789" else "1"
            tokens.append((count, parts))
        else:
            tokens.append(("1", [element]))

    return tokens


def generate_strings(tokenized_pattern, num_strings, max_repeats):
    def print_generation_step(step_description):
        print(step_description)

    results = []

    for _ in range(num_strings):
        result = ""
        for multiplier, elements in tokenized_pattern:
            element = random.choice(elements)
            step_msg = f"Chosen element '{element}' from {elements} with multiplier '{multiplier}'"
            if multiplier == "1":
                result += element
                print_generation_step(f"Appending '{element}': {result}")
            elif multiplier == "?":
                if random.choice([True, False]):
                    result += element
                    print_generation_step(f"Optionally appending '{element}': {result}")
            elif multiplier == "+":
                repeats = random.randint(1, max_repeats)
                result += element * repeats
                print_generation_step(
                    f"Appending '{element}' repeated {repeats} times: {result}"
                )
            elif multiplier == "*":
                repeats = random.randint(0, max_repeats)
                result += element * repeats
                print_generation_step(
                    f"Appending '{element}' repeated {repeats} times (maybe 0): {result}"
                )
            else:
                # Fixed number of repetitions
                repeats = int(multiplier)
                result += element * repeats
                print_generation_step(
                    f"Appending '{element}' repeated {repeats} times (fixed): {result}"
                )

        results.append(result)
        print("\n")  # Add a newline between results for clarity

    return results


regex_patterns = ["(a|b)(c|d)E⁺G?", "P(Q|R|S)T(UV|W|X)*Z⁺", "1(0|1)*2(3|4)⁵36"]
tokenized_regex_patterns = [
    [("1", ["a", "b"]), ("1", ["c", "d"]), ("+", ["E"]), ("?", ["G"])],
    [
        ("1", ["P"]),
        ("1", ["Q", "R", "S"]),
        ("1", ["T"]),
        ("*", ["UV", "W", "X"]),
        ("+", ["Z"]),
    ],
    [("1", ["1"]), ("*", ["0", "1"]), ("1", ["2"]), ("5", ["3", "4"]), ("1", ["36"])],
]
max_length = 5  # Limit for symbols written an undefined number of times
number_of_strings = 5  # Number of strings to generate

for tokens, pattern in zip(tokenized_regex_patterns, regex_patterns):
    print(f"{number_of_strings} random strings for the regex pattern '{pattern}':")
    generate_strings(tokens, number_of_strings, max_length)
    print("\n")
