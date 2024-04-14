import random
import re

def tokenize_regex(pattern):
    # Tokenizing the regex pattern
    special_chars = ['*', '+', '?', '^']
    pattern = pattern.replace('(', '%(').replace(')', ')%').strip('%').replace('%%', '%')
    segments = pattern.split('%')

    tokens = []
    for i in range(len(segments)-1, 0, -1):
        if segments[i][0] in special_chars:
            segments[i-1] += segments[i][0]
            segments[i] = segments[i][1:]

    for segment in segments:
        if segment:
            first_char = segment[0]
            if first_char == '(':
                options, modifier = segment[1:-1], segment[-1]
                if modifier in special_chars:
                    tokens.append((modifier, options.split('|')))
                else:
                    tokens.append(('1', options.split('|')))
            else:
                tokens.append(('1', [segment]))
    return tokens

def generate_strings(tokens, num_strings, max_reps):
    results = []
    for _ in range(num_strings):
        result = ""
        for modifier, options in tokens:
            choice = random.choice(options)
            if modifier == '?':
                result += choice if random.random() > 0.5 else ''
            elif modifier == '+':
                result += ''.join([choice] * random.randint(1, max_reps))
            elif modifier == '*':
                result += ''.join([choice] * random.randint(0, max_reps))
            else:
                result += choice
        results.append(result)
    return results

def explain_string_generation(pattern, tokens, num_strings, max_reps):
    print(f"\nExplaining string generation for the pattern: {pattern}")
    for _ in range(num_strings):
        result = ""
        steps = []
        for modifier, options in tokens:
            choice = random.choice(options)
            if modifier == '1':
                result += choice
                steps.append(f"Added '{choice}'")
            elif modifier == '?':
                if random.random() > 0.5:
                    result += choice
                    steps.append(f"Optionally added '{choice}'")
            elif modifier == '+':
                count = random.randint(1, max_reps)
                result += ''.join([choice] * count)
                steps.append(f"Added '{choice}' {count} times")
            elif modifier == '*':
                count = random.randint(0, max_reps)
                result += ''.join([choice] * count)
                steps.append(f"Optionally added '{choice}' {count} times")

        print("\n".join(steps))
        print(f"Generated string: {result}\n")

# Example usage
pattern = '(a|b)(c|d)E+G?'
tokens = tokenize_regex(pattern)

num_strings = 5
max_reps = 5

generated_strings = generate_strings(tokens, num_strings, max_reps)
print(generated_strings)
explain_string_generation(pattern, tokens, num_strings, max_reps)
