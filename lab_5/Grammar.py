class BaseGrammar:
    def __init__(self, vn, vt, p, s):
        self.Vn = vn
        self.Vt = vt
        self.P = p
        self.S = s

    def print_grammar(self):
        print("\nCurrent Grammar:")
        print("Nonterminals (Vn):", self.Vn)
        print("Terminals (Vt):", self.Vt)
        print("Productions (P):")
        for key, value in self.P.items():
            print(f"{key} -> {value}")
        print("Start symbol (S):", self.S, "\n")
