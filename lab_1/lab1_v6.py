import random

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

    def generate_string(self):
        """Generates a single string from the grammar."""
        def generate_from(variable):
            production = random.choice(self.productions[variable])
            return ''.join(generate_from(sym) if sym in self.variables else sym for sym in production)
        
        return generate_from(self.start_variable)

    def generate_strings(self, n):
        """Generates n valid strings from the grammar."""
        return [self.generate_string() for _ in range(n)]

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

valid_strings = grammar.generate_strings(5)
for i in valid_strings:
    print (i)
