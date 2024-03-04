from graphviz import Digraph


class FiniteAutomaton:
    def __init__(self, states, alphabet, start_state, final_states, transitions):
        self.states = states
        self.alphabet = alphabet
        self.start_state = start_state
        self.final_states = final_states
        self.current_state = self.start_state
        self.delta = transitions

    def to_regular_grammar(self):
        grammar = {state: set() for state in self.states}
        for (current_state, input_symbol), next_states in self.delta.items():
            for next_state in next_states:
                grammar[current_state].add((input_symbol, "A" + next_state[1]))

        for final_state in self.final_states:
            grammar[final_state].add(("ε",))  # Add ε-production for final states

        for state, productions in grammar.items():
            for production in productions:
                print(
                    f"q{state[1]} -> {production[0]}"
                    + (f"q{production[1][1]}" if len(production) > 1 else "")
                )

    def determine_type(self):
        for state in self.states:
            transitions = {symbol: 0 for symbol in self.alphabet}
            for (current_state, input_symbol), next_states in self.delta.items():
                if current_state == state:
                    transitions[input_symbol] += len(next_states)

            if any(count > 1 for count in transitions.values()):
                print("NFA")
                return

        print("DFA")

    def convert_to_dfa(self):
        new_states = {frozenset([self.start_state])}
        dfa_transitions = {}
        unmarked_states = new_states.copy()

        while unmarked_states:
            current_state_set = unmarked_states.pop()
            for symbol in self.alphabet:
                next_state_set = frozenset(
                    sum(
                        [
                            self.delta.get((state, symbol), [])
                            for state in current_state_set
                        ],
                        [],
                    )
                )
                if next_state_set:
                    dfa_transitions[(current_state_set, symbol)] = next_state_set

                    if next_state_set not in new_states:
                        new_states.add(next_state_set)
                        unmarked_states.add(next_state_set)

        for (state_set, symbol), next_state_set in dfa_transitions.items():
            if next_state_set:
                print(f"    {set(state_set)} --{symbol}--> {set(next_state_set)}")

    def visualize(self):
        dot = Digraph()
        dot.attr(rankdir="LR", size="8")

        dot.node("fake", style="invisible")
        dot.edge("fake", f"q{self.start_state[1]}", style="bold")
        for final_state in self.final_states:
            dot.node(f"q{final_state[1]}", shape="doublecircle")

        for state in self.states:
            if f"q{state[1]}" not in dot.body:  # Avoid duplicating final states
                dot.node(f"q{state[1]}")

        for (state, symbol), next_states in self.delta.items():
            for next_state in next_states:
                dot.edge(f"q{state[1]}", f"q{next_state[1]}", label=str(symbol))

        dot.render("FA", view=True, format="png")


states = {"q0", "q1", "q2", "q3", "q4"}
alphabet = {"a", "b"}
start_state = "q0"
final_states = {"q4"}
transitions = {
    ("q0", "a"): ["q1"],
    ("q1", "b"): ["q1", "q2"],
    ("q2", "b"): ["q3"],
    ("q3", "a"): ["q1"],
    ("q2", "a"): ["q4"],
}

fa = FiniteAutomaton(states, alphabet, start_state, final_states, transitions)
print("\nThe Regular Grammar:")
fa.to_regular_grammar()
print("\nThe Finite Automaton is of type:")
fa.determine_type()
print("\nThe NFA converted to DFA:")
fa.convert_to_dfa()
fa.visualize()
