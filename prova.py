from parsimonious.grammar import Grammar, NodeVisitor
grammar = Grammar(
    """
    body = stm*
    stm = comment /
        foo /
        unit /
        assignment /
        garbage

    comment = ~"--[^\\n]*" eol 
    garbage = ~"[^\\n]*" eol
    
    unit = "TEST." ("UNIT" / "SUBPROGRAM") ":" word eol

    assignment = "TEST.VALUE:" var ":" value
    
    foo = "TEST.SCRIPT_FEATURE:" word eol

    word = ~r"[-\w]+"
    
    uffa = "TEST.NEW" eol
    ende = "TEST.END" eol

    eol = ~"\\s*\\n"

    var = word "." ("<<GLOBAL>>" / word ) "." word
    value = ~"[0-9]+"
    
    """)

class MyVisitor(NodeVisitor):
    
    def __init__(self):
        self.errcount = 0

    def visit_foo(self, node, visited_children):
        ( _, payload, _) = visited_children
        # print(f"-SCRIPT_FEATURE----> '{payload.text}'")

    def visit_unit(self, node, visited_children):
        ( _, v, _, payload, _) = visited_children
        # print(f"-{v[0].text}--UNIT----> '{payload.text}'")

    def visit_assignment(self, node, visited_children):
        ( _, var, _, value) = visited_children
        print(f"assignment. value={value.text}")
        pass

    
    def visit_end(self, node, visited_children):
        print("END")
        pass
    def visit_uffa(self, node, visited_children):
        # print(f"----> '{node.text.rstrip()}'")
        pass
    
    def visit_comment(self, node, visited_children):
        comment = node.text.rstrip()
        # print(f"comment: '{comment}'")
        pass

    def visit_garbage(self, node, visited_children):
        self.errcount += 1
        
    def generic_visit(self, node, visited_children):
        """ The generic visit method. """
        return visited_children or node

fn = "examples/GEMINIX_5407_WB.tst"

with open(fn, "r") as file:
    src = file.read()

v = MyVisitor()
    
tree = grammar.parse(src)
result = v.visit(tree)


print(v.errcount)


