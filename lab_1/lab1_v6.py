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
print(grammar)
