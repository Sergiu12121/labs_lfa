from collections import defaultdict
from graphviz import Digraph

states = ["q0", "q1", "q2", "q3", "q4"]
alphabet = ["a", "b"]
accepting_states = ["q4"]
transitions = {
    ("q0", "a"): "q1",
    ("q1", "b"): "q2",
    ("q2", "b"): "q3",
    ("q3", "a"): "q1",
    ("q2", "a"): "q4",
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
            grammar[state].append(("ε",))
    return grammar


converted_grammar = convert_fa_to_rg(states, transitions, accepting_states)
readable_grammar = {}
for state, productions in converted_grammar.items():
    readable_grammar[state] = ["".join(prod) for prod in productions]

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


is_dfa = is_deterministic(transitions, states, alphabet)

if is_dfa:
    print("\nThe FA is deterministic (DFA).")
else:
    print("\nThe FA is non-deterministic (NFA).")

# Exercise c) Convert NFA to DFA
nfa = {
    "states": ["q0", "q1", "q2", "q3", "q4"],
    "alphabet": ["a", "b"],
    "transitions": {
        "q0": {"a": ["q1"]},
        "q1": {"b": ["q1", "q2"]},
        "q2": {"a": ["q3"], "b": ["q4"]},
        "q3": {"a": ["q1"]},
        "q4": {"a": ["q2"]},
    },
    "start_state": "q0",
    "accept_states": ["q4"],
}


def nfa_to_dfa(nfa):
    new_states_list = []
    dfa = {
        "states": [],
        "alphabet": nfa["alphabet"],
        "transitions": defaultdict(dict),
        "start_state": frozenset([nfa["start_state"]]),
        "accept_states": set(),
    }
    states_queue = [frozenset([nfa["start_state"]])]
    while states_queue:
        current_state = states_queue.pop(0)
        if current_state not in new_states_list:
            new_states_list.append(current_state)
            for symbol in nfa["alphabet"]:
                next_state = frozenset(
                    sum(
                        [
                            nfa["transitions"].get(state, {}).get(symbol, [])
                            for state in current_state
                        ],
                        [],
                    )
                )
                dfa["transitions"][current_state][symbol] = next_state
                if next_state not in new_states_list:
                    states_queue.append(next_state)
    for new_state in new_states_list:
        if any(state in nfa["accept_states"] for state in new_state):
            dfa["accept_states"].add(new_state)
    dfa["states"] = new_states_list
    return dfa


converted_dfa = nfa_to_dfa(nfa)


def print_dfa(dfa):
    print("DFA:")
    print("States:", [set(state) for state in dfa["states"]])
    print("Start State:", set(dfa["start_state"]))
    print("Accept States:", [set(state) for state in dfa["accept_states"]])
    print("Transitions:")
    for state, transitions in dfa["transitions"].items():
        for symbol, next_state in transitions.items():
            print(f"    {set(state)} --{symbol}--> {set(next_state)}")


print_dfa(converted_dfa)

# Exercise d) Visualize the FA using Graphviz
fa = Digraph("finite_automaton")
fa.attr(rankdir="LR")

# Add states to the graph
states = ["q0", "q1", "q2", "q3", "q4"]
for state in states:
    if state == "q4":
        fa.node(state, shape="doublecircle")
    else:
        fa.node(state, shape="circle")

fa.node("", shape="none")
fa.edge("", "q0")

transitions = [
    ("q0", "q1", "a"),
    ("q1", "q1", "b"),
    ("q1", "q2", "b"),
    ("q2", "q3", "b"),
    ("q2", "q4", "a"),
    ("q3", "q1", "a"),
]

for src, dst, label in transitions:
    fa.edge(src, dst, label=label)

fa.render("/Users/sergiu_sd/Desktop/finite_automaton", view=True, format="png")
