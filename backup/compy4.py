import sys

def activate(args) :
	return "\nenter $" + str(int(args[0])*4) + ", $0"

def number(args) :
	return "\nmovl $" + args[0] + ", %eax"

def boolean(args) :
	return "\nmovl $" + ("1" if args[0] == "true" else "0") + ", %eax"

def identifier(args) :
	return getId(args[0])

def address(args) :
	return getAddr(args[0])

def push(args) :
	return "\npushl %eax"

def variable(args) :
	makeVar(args[0])
	return ""

def parameter(args) :
	makeParam(args[0])
	return ""

def returncode(args) :
	flush()
	return "\nleave\nret"

def call(args) :
	return "\ncall *%eax\naddl $" + str(int(args[0])*4) + ", %esp"

def iterate(args) :
	iterator = "\ncall *%eax\ncmp $0, (%esp)\nje end_iter0"
	hasnext = "\npushl %ebp\nmovl (%ebp), %ebp"
	loopvar =  translate([["PUSH"], ["ADDRESS", args[0]],
			      ["PUSH"], ["ADDRESS", "__as__"], ["CALL", " 2"]])
	return iterator + hasnext + loopvar

def callback(args) :
	return "\npopl %ebp\nret\nend_iter0:\naddl $" + str((int(args[0])+1) * 4) + ", %esp"

def startwhile(args) :
	return translate([["PUSH"], ["ADDRESS", "_loopEnd" + "0"], 
			  ["PUSH"], ["ADDRESS", "__jmpf__"], ["CALL", "2"]])
	
def endwhile(args) :
	return translate([["ADDRESS", "_loopStart" + "0"], ["JUMP"],
			  ["LABEL", "_loopEnd" + "0"]])

def jump(args) :
	return "\njmp *%eax"

def label(args) :
	return "\n" + args[0] + ":"

def section(args) :
	makeLabel(args[0])
	return ""

def function(args) :
	name = args[0]
	makeFunc(name)
	return "\n.type " + name + ",@function"

codes = {"ACTIVATE": activate, "NUMBER": number, "IDENTIFIER" : identifier, 
	 "ADDRESS" : address, "PUSH" : push, "PARAMETER" : parameter, "VARIABLE" : variable,
	 "RETURN": returncode, "CALL": call , "LABEL" : label, "FUNCTION": function,
	 "BOOLEAN": boolean, "JUMP":jump, "SECTION": section, "ITERATE":iterate, 
	 "CALLBACK": callback, "STARTWHILE":startwhile, "ENDWHILE":endwhile}

functions = dict()
sections  = dict()
locals    = dict()
params    = dict()

def makeVar(name) :
	make(locals, name, varTup( str( -( len(locals)+1 )*4 ) ))	

def makeParam(name) :
	make(params, name, varTup( str( ( len(params)+2 )*4) ))

def varTup(offset) :
	return ( "\nmovl " + offset + "(%ebp), %eax", 
		 "\nmovl %ebp, %eax\naddl $" + offset + ", %eax")

def makeFunc(name) :
	make(functions, name, labelTup(name))

def makeLabel(name) :
	if name not in functions :
		make(sections, name, labelTup(name))

def labelTup(name) :
	return ("\nmovl " + name + ", %eax", "\nmovl $" + name + ", %eax")
	

def make(set, name, tuple) :
	set[name] = tuple

def flush() :
	global locals, params
	printLocals()
	locals = dict()
	params = dict()
	sections = dict()

def getId(name) :
	return get(name)[0]

def getAddr(name) :
	return get(name)[1]

def get(name) :
	print(name)
	global locals, params, functions, sections
	if name in locals :
		return locals[name]
	if name in params :
		return params[name]
	if name in sections :
		return sections[name]
	if name in functions :
		return functions[name]

def importFile(filename) :
	with open(filename, "r") as file :
		for line in file :
			line = line.split()
			if line and line[0] == ".globl" :
				makeFunc(line[1])

def compile(source) :
	importFile("std.s")
	code = translate(clean(source))
	code = "\n".join(line for line in code.split("\n") if line)

	printGlobals()
	return header() + "\n" + code + "\n"

def translate(lines) :
	return "\n".join( "\n\t#" + " ".join(line) + codes[line[0]](line[1:]) for line in lines )

def clean(code) :
	while "//" in code :
		index = code.index("//")
		code = code[:index] + code[code.index("\n", index)+1:]
	return [line.split() for line in code.split("\n") if line]

def header() :
	return "\n".join(
		['.include "std.s"',
		 ".section .data",
		 ".section .text",
		 ".globl _start",
		 "_start:",
		 "pushl $0",
		 "movl %esp, %ebp",
		 "call main",
		 "movl %eax, %ebx",
		 "movl $1, %eax",
		 "int $0x80"] )

def main() :
	file = sys.argv[1]
	with open(file + ".lang", "r") as source :
		with open(file + ".s", "w") as destination :
			destination.write(compile(source.read()))	
	
def printGlobals() :
	print("\t-- GLOBALS --")
	for name in functions :
		print(name)
	
def printLocals() :
	print("\t-- LOCALS --")
	for name in params :
		print(name)
	for name in locals :
		print(name)

if __name__ == "__main__" :
	main()
