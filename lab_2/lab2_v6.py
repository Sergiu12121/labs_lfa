from graphviz import Digraph

fa = Digraph('finite_automaton')
fa.attr(rankdir='LR')  

states = ['q0', 'q1', 'q2', 'q3', 'q4']
for state in states:
    if state == 'q4': 
        fa.node(state, shape='doublecircle')
    else:
        fa.node(state, shape='circle')

fa.node('', shape='none')
fa.edge('', 'q0') 

transitions = [
    ('q0', 'q1', 'a'),
    ('q1', 'q1', 'b'),  
    ('q1', 'q2', 'b'),
    ('q2', 'q3', 'b'),
    ('q2', 'q4', 'a'),
    ('q3', 'q1', 'a')
]

for src, dst, label in transitions:
    fa.edge(src, dst, label=label)

fa.render('/Users/sergiu_sd/Desktop/finite_automaton', view=True, format='png')
