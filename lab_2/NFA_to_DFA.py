import graphviz

dot = graphviz.Digraph(comment='NFA to DFA Conversion')

dot.node("{'q0'}")
dot.node("{'q1'}")
dot.node("{'q1', 'q2'}")
dot.node("{'q1', 'q3', 'q2'}")
dot.node("{'q1', 'q4'}")

dot.edge("{'q0'}", "{'q1'}", label='a')
dot.edge("{'q1'}", "{'q1', 'q2'}", label='b')
dot.edge("{'q1', 'q2'}", "{'q4'}", label='a')
dot.edge("{'q1', 'q2'}", "{'q1', 'q3', 'q2'}", label='b')
dot.edge("{'q1', 'q3', 'q2'}", "{'q1', 'q4'}", label='a')
dot.edge("{'q1', 'q3', 'q2'}", "{'q1', 'q3', 'q2'}", label='b')
dot.edge("{'q1', 'q4'}", "{'q1', 'q2'}", label='b')

dot.render("DFA", view=True, format="png")
