import random
import re


def generate_from_regex(pattern, max_repeat=5):
    def generate_from_group(group):
        alternatives = group.strip("()").split("|")
        return random.choice(alternatives)

    def generate_from_token(token):
        if token.endswith("?"):
            return (
                generate_from_token(token[:-1]) if random.choice([True, False]) else ""
            )
        elif token.endswith("*"):
            return "".join(
                generate_from_group(token[:-1])
                for _ in range(random.randint(0, max_repeat))
            )
        elif token.endswith("+"):
            return "".join(
                generate_from_group(token[:-1])
                for _ in range(random.randint(1, max_repeat))
            )
        else:
            return generate_from_group(token)

    tokens = re.findall(r"\([^)]*\)\*|\([^)]*\)\+|\([^)]*\)\?|\([^)]*\)|.", pattern)

    return "".join(generate_from_token(token) for token in tokens)


regex_patterns = ["(a|b)(c|d)E+G?", "P(Q|R|S)T(UV|W|X)*Z+", "1(0|1)*2(3|4)^536"]

# Generate and print strings for each regex pattern
generated_strings = [generate_from_regex(p) for p in regex_patterns]
print("\n The generated words are:")
print(generated_strings, "\n")
