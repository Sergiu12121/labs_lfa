class FiniteAutomaton:

    def __init__(self, states, alphabet, transition_function, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transition_function = transition_function
        self.start_state = start_state
        self.accept_states = accept_states

    def __str__(self):
        fa_str = "States: {}\n".format(self.states)
        fa_str += "Alphabet: {}\n".format(self.alphabet)
        fa_str += "Start State: {}\n".format(self.start_state)
        fa_str += "Accept States: {}\n".format(self.accept_states)
        fa_str += "Transition Function:\n"
        for (state, symbol), next_state in self.transition_function.items():
            fa_str += "  δ({}, {}) = {}\n".format(state, symbol, next_state)
        return fa_str

    def check_string(self, input_string):
        current_state = self.start_state

        for symbol in input_string:
            if (current_state, symbol) in self.transition_function:
                current_state = self.transition_function[(current_state, symbol)]
            else:
                return False

        return current_state in self.accept_states


finite_automaton = FiniteAutomaton(
    states={'S', 'I', 'J', 'K', 'F'},
    alphabet={'a', 'b', 'c', 'e', 'n', 'f', 'm'},
    transition_function={
        ('S', 'c'): 'I',
        ('I', 'b'): 'J',
        ('I', 'f'): 'I',
        ('J', 'n'): 'J',
        ('J', 'c'): 'S',
        ('J', 'e'): 'K',
        ('K', 'n'): 'K',
        ('K', 'e'): 'F',
        ('K', 'm'): 'F'
    },
    start_state='S',
    accept_states={'K', 'F'}
)

test_strings = ['cnb', 'fm', 'ccce', 'cbne']
results = {s: finite_automaton.check_string(s) for s in test_strings}
print(results)
