from Grammar import BaseGrammar


class BreakFromLoops(Exception):
    pass


class Grammar(BaseGrammar):
    def cfg_to_cnf(self):
        self.start_symbol_rhs_removal()
        self.remove_null_productions()
        self.remove_unit_productions()
        self.remove_inaccessible_symbols()
        self.replace_terminals_with_nonterminals()
        self.reduce_production_length()

    def start_symbol_rhs_removal(self):
        if any(
            self.S in production for value in self.P.values() for production in value
        ):
            self.P = {"X": [self.S]} | self.P
            self.S = "X"
            self.Vn.append(self.S)

    def create_new_productions(self, production, character):
        return [
            production[:i] + production[i + 1 :]
            for i in range(len(production))
            if production[i] == character
        ]

    def remove_null_productions(self):
        null_prods = {key for key, values in self.P.items() if "ε" in values}
        if null_prods:
            # Remove ε productions
            for key in null_prods:
                self.P[key].remove("ε")
            # Add new productions by removing nullable symbols
            for key, values in list(self.P.items()):
                new_values = []
                for production in values:
                    for null_prod in null_prods:
                        if null_prod in production:
                            new_values.extend(
                                self.create_new_productions(production, null_prod)
                            )
                self.P[key].extend(
                    prod for prod in new_values if prod not in self.P[key]
                )

    def remove_unit_productions(self):
        for key, value in self.P.items():
            for production in value:
                if key == production:
                    self.P[key].remove(production)
        changes = True
        while changes:
            changes = False
            for key, value in self.P.items():
                for production in value:
                    if production in self.Vn:
                        changes = True
                        self.P[key].remove(production)
                        for prod in self.P[production]:
                            if prod not in self.P[key]:
                                self.P[key].append(prod)

    def remove_inaccessible_symbols(self):
        accessible = set([self.S])
        queue = [self.S]

        while queue:
            current = queue.pop(0)
            for production in self.P.get(current, []):
                for symbol in production:
                    if symbol in self.Vn and symbol not in accessible:
                        accessible.add(symbol)
                        queue.append(symbol)

        self.Vn = [nt for nt in self.Vn if nt in accessible]
        for nt in list(self.P.keys()):
            if nt not in accessible:
                del self.P[nt]

    def replace_terminals_with_nonterminals(self):
        def new_nonterminal():
            available = set(chr(i) for i in range(65, 91)) - set(self.Vn)
            if not available:
                raise ValueError("Ran out of single-letter nonterminal symbols!")
            return min(available)

        terminal_to_nonterminal = {}
        new_P = {key: [] for key in self.P}

        for key, productions in self.P.items():
            for prod in productions:
                new_prod = ""
                for char in prod:
                    if char in self.Vt and len(prod) > 1:
                        if char not in terminal_to_nonterminal:
                            new_nt = new_nonterminal()
                            self.Vn.append(new_nt)
                            terminal_to_nonterminal[char] = new_nt
                            new_P[new_nt] = [char]
                        new_prod += terminal_to_nonterminal[char]
                    else:
                        new_prod += char
                new_P[key].append(new_prod)

        self.P = new_P

    def reduce_production_length(self):
        def new_nonterminal(existing):
            for char in (chr(i) for i in range(65, 91)):
                if char not in existing:
                    return char
            raise ValueError("Ran out of single-letter nonterminal symbols!")

        existing_binaries = {}
        new_productions_dict = {}
        for key, productions in list(self.P.items()):
            new_productions = []
            for production in productions:
                if len(production) > 2:
                    while len(production) > 2:
                        last_two = production[-2:]
                        if last_two not in existing_binaries:
                            new_nt = new_nonterminal(
                                set(self.Vn) | set(new_productions_dict.keys())
                            )
                            self.Vn.append(new_nt)
                            new_productions_dict[new_nt] = [last_two]
                            existing_binaries[last_two] = new_nt
                        production = production[:-2] + existing_binaries[last_two]
                    new_productions.append(production)
                else:
                    new_productions.append(production)
            self.P[key] = new_productions
        self.P.update(new_productions_dict)


grammar = Grammar(
    vn=["S", "A", "B", "C", "D", "E", "F"],
    vt=["a", "b", "c"],
    p={
        "S": ["aB", "AC"],
        "A": ["a", "ASC", "BC", "aD"],
        "B": ["b", "bS", "bF"],
        "C": ["ε", "BA", "FB"],
        "E": ["aB"],
        "D": ["abC"],
        "F": ["c", "cS"],
    },
    s="S",
)


# Print the original grammar
grammar.print_grammar()

# Convert the grammar to Chomsky Normal Form
grammar.cfg_to_cnf()

# Print the converted grammar to see the changes
grammar.print_grammar()
