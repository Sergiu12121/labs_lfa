import random

class Grammar:
    def __init__(self, variables, terminals, productions, start_variable):
        self.variables = set(variables)
        self.terminals = set(terminals)
        self.productions = productions
        self.start_variable = start_variable

    def generate_string(self):
        def generate_from(variable):
            production = random.choice(self.productions[variable])
            return ''.join(generate_from(sym) if sym in self.variables else sym for sym in production)
        
        return generate_from(self.start_variable)

    def generate_strings(self, n):
        return [self.generate_string() for _ in range(n)]

    def to_finite_automaton(self):

        states = self.variables.union({'F'})
        alphabet = self.terminals
        transition_function = {}
        accept_states = set()

        for variable, expansions in self.productions.items():
            for expansion in expansions:
                if expansion != 'e':  
                    if len(expansion) == 2 and expansion[1] in self.variables:
                        transition_function[(variable, expansion[0])] = expansion[1]
                    else:
                        transition_function[(variable, expansion[0])] = 'F'
                        accept_states.add('F')
                else:
                    accept_states.add(variable)

        return FiniteAutomaton(states, alphabet, transition_function, self.start_variable, accept_states)


class FiniteAutomaton:
    def __init__(self, states, alphabet, transition_function, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transition_function = transition_function
        self.start_state = start_state
        self.accept_states = accept_states

    def check_string(self, input_string):
        current_state = self.start_state

        for symbol in input_string:
            if (current_state, symbol) in self.transition_function:
                current_state = self.transition_function[(current_state, symbol)]
            else:
                return False

        return current_state in self.accept_states


# a. Creating the grammar object
variables = ['S', 'I', 'J', 'K']
terminals = ['a', 'b', 'c', 'e', 'n', 'f', 'm']
productions = {
    'S': ['cI'],
    'I': ['bJ', 'fI'],
    'J': ['nJ', 'cS', 'eK'],
    'K': ['nK', 'e', 'm']
}
start_variable = 'S'
grammar = Grammar(variables, terminals, productions, start_variable)

# b. Generating 5 valid strings from the grammar
valid_strings = grammar.generate_strings(5)

# c. Converting the grammar to a finite automaton
finite_automaton = grammar.to_finite_automaton()

# d. Checking if certain strings can be obtained from the finite automaton
print()
test_strings = input("Input the word to check ")

print ("5 VALID STRINGS :")
for i in valid_strings:
    print(i)
print()
print(f"The word {test_strings} is {finite_automaton.check_string(test_strings)}")


