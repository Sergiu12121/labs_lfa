import re
import enum
from graphviz import Digraph


class TokenType(enum.Enum):
    NUMBER = 1
    PLUS = 2
    MINUS = 3
    TIMES = 4
    DIVIDE = 5
    LPAREN = 6
    RPAREN = 7
    WHITESPACE = 8
    ERROR = 9


def lexer(input_string):
    tokens = []
    while input_string:
        match = None
        for token_type, pattern in TOKENS:
            regex = re.compile(pattern)
            match = regex.match(input_string)
            if match:
                value = match.group(0)
                if token_type != TokenType.WHITESPACE and token_type != TokenType.ERROR:
                    tokens.append((token_type, value))
                input_string = input_string[match.end() :]
                break
        if not match:
            print("Invalid character:", input_string[0])
            input_string = input_string[1:]

    return tokens


class ASTNode:
    def __init__(self, type, children=None, value=None):
        self.type = type
        self.value = value
        self.children = children if children is not None else []

    def __repr__(self):
        type_name = self.type.name if isinstance(self.type, enum.Enum) else self.type
        return f"{type_name}({self.value}, {self.children})"


def parse(tokens):
    root = ASTNode(TokenType.PLUS, value="ROOT")
    current_node = root

    i = 0
    while i < len(tokens):
        token_type, value = tokens[i]
        if token_type in [
            TokenType.PLUS,
            TokenType.MINUS,
            TokenType.TIMES,
            TokenType.DIVIDE,
        ]:
            current_node = ASTNode(token_type, value=value)
            root.children.append(current_node)
        elif token_type == TokenType.NUMBER:
            number_node = ASTNode(token_type, value=value)
            current_node.children.append(number_node)
            if i + 1 < len(tokens) and tokens[i + 1][0] in [
                TokenType.PLUS,
                TokenType.MINUS,
                TokenType.TIMES,
                TokenType.DIVIDE,
            ]:
                operator_node = ASTNode(tokens[i + 1][0], value=tokens[i + 1][1])
                current_node.children.append(operator_node)
                i += 1
        elif token_type == TokenType.LPAREN:
            current_node = ASTNode(TokenType.LPAREN, value=value)
            root.children.append(current_node)
        elif token_type == TokenType.RPAREN:
            current_node = ASTNode(TokenType.RPAREN, value=value)
            root.children.append(current_node)
        i += 1

    return root


def add_nodes_edges(tree, graph=None):
    if graph is None:
        graph = Digraph()
        graph.node(name=str(id(tree)), label=f"{tree.type.name}({tree.value})")

    for child in tree.children:
        child_label = (
            f"{child.type.name}({child.value})" if child.value else child.type.name
        )
        graph.node(name=str(id(child)), label=child_label)
        graph.edge(str(id(tree)), str(id(child)))
        graph = add_nodes_edges(child, graph)

    return graph


TOKENS = [
    (TokenType.NUMBER, r"\d+"),
    (TokenType.PLUS, r"\+"),
    (TokenType.MINUS, r"\-"),
    (TokenType.TIMES, r"\*"),
    (TokenType.DIVIDE, r"\/"),
    (TokenType.LPAREN, r"\("),
    (TokenType.RPAREN, r"\)"),
    (TokenType.WHITESPACE, r"\s+"),
    (TokenType.ERROR, r"."),
]

input_string = "3 + 4 * 2 / (1 - 5)"
tokens = lexer(input_string)
ast = parse(tokens)
graph = add_nodes_edges(ast)
graph.render("ast_arithmetic", view=True)
