from parsimonious.grammar import Grammar, NodeVisitor
grammar = Grammar(
"""

body = ( stm ? eol ) * "§"
stm = comment /  feature / block 

uffa = "ok:" 

eol = ~"\\s*\\n"
comment = ~"--[^\\n]*"

word = ~r"[-_\w]+"

intvalue = ~r"0x[0-9A-F]+" /
    ~r"[0-9]+" /
    "<<MIN>>" /
    "<<MAX>>" /
    ("<<malloc " ~r"[0-9]+" ">>") /
    "TRUE" / "FALSE" / "ON" / "RESTORE" / "NODE_A" /
    "<<null>>"

garbage = ~"[^\\n]*"

feature = "TEST.SCRIPT_FEATURE:" word
unit = "TEST.UNIT:" word
subprogram = "TEST.SUBPROGRAM:" word
begin = "TEST." begin_verb 
begin_verb = "NEW"/"ADD"/"REPLACE"
test_name = "TEST.NAME:" word ( "." word)?

end_notes = "TEST.END_NOTES:"
note_line = !end_notes  ~"[^\\n]*"
notes = "TEST.NOTES:" eol ( note_line eol ) * end_notes

end_block = "TEST.END" &eol
block = unit eol subprogram eol begin eol test_name eol ( !end_block inner_stm eol )* end_block

inner_stm =  notes / assign / check / user_code / stub / stub_val_user_code / garbage


assign = "TEST.VALUE:" var ":" intvalue

var = var1 / var2
var1 = word "." ( word / "<<GLOBAL>>" ) ("." word)*( "[" ~r"[0-9]+" "]" )?
var2 = "<<OPTIONS>>.DO_COMBINATION"

check = "TEST.EXPECTED:" var ":" intvalue

end_user_code = "TEST.END_VALUE_USER_CODE:"
user_code = "TEST.VALUE_USER_CODE:" var eol ( !end_user_code ~"[^\\n]*" eol )* end_user_code


stub = "TEST.STUB:" word "." word

end_stub_val_user_code = "TEST.END_STUB_VAL_USER_CODE:"
stub_val_user_code = "TEST.STUB_VAL_USER_CODE:" word ("." word)+ eol \
    ( !end_stub_val_user_code ~"[^\\n]*" eol)* \
    end_stub_val_user_code


""")

##

#print(grammar)

class MyVisitor(NodeVisitor):
    
    def __init__(self):
        self.errcount = 0

    def visit_feature(self, node, visited_children):
        name = visited_children[1].text
        # print(name)
        
    def visit_unit(self, node, visited_children):
        name = visited_children[1].text
        # print(f"unit='{name}'")

    def visit_subprogram(self, node, visited_children):
        name = visited_children[1].text
        # print(f"subprogram='{name}'")

    def visit_begin(self, node, visited_children):
        name = visited_children[1][0].text
        # print(f"begin='{name}'")
        global nnode
        
        
    def visit_name(self, node, visited_children):
        name = visited_children[1].text
        print(f"name='{name}'")

    def visit_note_line(self, node, visited_children):
        # print(f"note='{node.text}'")
        pass
    
    def visit_notes(self, node, visited_children):
        # print("notes")
        pass
        
    def visit_garbage(self, node, visited_children):
        self.errcount += 1
        print(node.text, node.full_text.count('\n', 0, node.start) + 1)
        
        

    def generic_visit(self, node, visited_children):
        """ The generic visit method. """
        return visited_children or node
visitor = MyVisitor()


fn = "examples/GEMINIX_5407_WB.tst"

with open(fn, "r") as file:
    src = file.read()
    
tree = grammar.parse(src + "§")
result = visitor.visit(tree)

print(visitor.errcount)

