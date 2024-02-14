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


class Grammar:
    def __init__(self, variables, terminals, productions, start_variable):
        self.variables = set(variables)
        self.terminals = set(terminals)
        self.productions = productions
        self.start_variable = start_variable

    def __str__(self):
        grammar_str = "Variables: {}\n".format(self.variables)
        grammar_str += "Terminals: {}\n".format(self.terminals)
        grammar_str += "Productions:\n"
        for variable, expansions in self.productions.items():
            for expansion in expansions:
                grammar_str += "  {} -> {}\n".format(variable, expansion)
        grammar_str += "Start Variable: {}\n".format(self.start_variable)
        return grammar_str

    def to_finite_automaton(self):
        states = self.variables.union({'F'})
        alphabet = self.terminals
        transition_function = {}
        accept_states = set()

        for variable, expansions in self.productions.items():
            for expansion in expansions:
                if expansion != 'e':  # We skip the epsilon transitions for now
                    if len(expansion) == 2 and expansion[1] in self.variables:
                        transition_function[(variable, expansion[0])] = expansion[1]
                    else:
                        transition_function[(variable, expansion[0])] = 'F'
                        accept_states.add('F')
                else:
                    accept_states.add(variable)

        return FiniteAutomaton(states, alphabet, transition_function, self.start_variable, accept_states)

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

finite_automaton = grammar.to_finite_automaton()
print(finite_automaton)
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


class Grammar:
    def __init__(self, variables, terminals, productions, start_variable):
        self.variables = set(variables)
        self.terminals = set(terminals)
        self.productions = productions
        self.start_variable = start_variable

    def __str__(self):
        grammar_str = "Variables: {}\n".format(self.variables)
        grammar_str += "Terminals: {}\n".format(self.terminals)
        grammar_str += "Productions:\n"
        for variable, expansions in self.productions.items():
            for expansion in expansions:
                grammar_str += "  {} -> {}\n".format(variable, expansion)
        grammar_str += "Start Variable: {}\n".format(self.start_variable)
        return grammar_str

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

finite_automaton = grammar.to_finite_automaton()
print(finite_automaton)
 