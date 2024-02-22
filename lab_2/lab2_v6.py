# Define the finite automaton components
states = ['q0', 'q1', 'q2', 'q3', 'q4']
alphabet = ['a', 'b']
accepting_states = ['q4']
transitions = {
    ('q0', 'a'): 'q1',
    ('q1', 'b'): 'q1',
    ('q1', 'b'): 'q2',
    ('q2', 'b'): 'q3',
    ('q3', 'a'): 'q1',
    ('q2', 'a'): 'q4'
}

# a) Convert FA to a Regular Grammar
def convert_fa_to_rg(states, transitions, accepting_states):
    grammar = {}
    for state in states:
        grammar[state] = []
        for (current_state, symbol), next_state in transitions.items():
            if current_state == state:
                grammar[state].append((symbol, next_state))
        if state in accepting_states:
            grammar[state].append(('ε',))
    return grammar

# Convert and prepare the grammar for printing
converted_grammar = convert_fa_to_rg(states, transitions, accepting_states)
readable_grammar = {}
for state, productions in converted_grammar.items():
    readable_grammar[state] = [''.join(prod) for prod in productions]

# Print the Regular Grammar
print("Regular Grammar:")
for state, rules in readable_grammar.items():
    for rule in rules:
        print(f"{state} -> {rule}")

# b) Determine if the FA is deterministic
def is_deterministic(transitions, states, alphabet):
    transition_count = {}
    for state in states:
        for symbol in alphabet:
            transition_count[(state, symbol)] = 0
    for (state, symbol), _ in transitions.items():
        transition_count[(state, symbol)] += 1
    return all(count <= 1 for count in transition_count.values())

# Determine if the FA is a DFA or an NFA
is_dfa = is_deterministic(transitions, states, alphabet)

# Print whether the FA is deterministic or non-deterministic
if is_dfa:
    print("\nThe FA is deterministic (DFA).")
else:
    print("\nThe FA is non-deterministic (NFA).")
