#Compiler for proto-language

import re

vars = dict()
varc = 0
funcs = list()

#unit = r"\s*(\(*{}\)*)\s*"
#statement = unit.format(assignment + " | " + call)
#expression = unit.format(val + " | " + var + " | " + arith + " | " + relat + " | " + logic + " | " + call)
#assignment = unit.format(var + assignop + expression)
#assignop = unit.format("=")

#arith = unit.format(binarith + " | " + unarith)
#binarith = unit.format(expression + binarithop + expression)
#binarithop = unit.format("[-+*/%]")
#unarith = unit.format(unarithop + expression)
#unarithop = unit.format("[-+~]")

#val = unit.format(number + " | " + bool)
#var = unit.format("\w+")
#number = unit.format("\d+")
#bool = unit.format("true | false")

#relat = unit.format(expression + relatop + expression)
#relatop = unit.format("> | >= | == | != | <= | <")

#logic = unit.format(binlogic + " | " + unlogic)
#binlogic = unit.format(expression + binlogicop + expression)
#binlogicop = unit.format("[&|^]")
#unlogic = unit.format(unlogicop + expression)
#unlogicop = unit.format("!")

#call = unit.format(var + "\(" + params + "\)")
#params = unit.format("(" + leadingparam + ")* " + tailingparam)
#leadingparam = unit.format(tailingparam + ",")
#tailingparam = unit.format(var)


headerpat = re.compile(r"\s*(\w+)\(((\w+),\s*)*(\w+)\)")
print("Hi")


def main() :
	code = []
	#filename = "power"
	#with open(filename) as file :
	file = ["main(allo)", "e = -3 + 4", "another(hey, ha)", "code"]
	if 1 :
		for function in iterFuncs(file) :
			code.append(compileFunc(function))
	print( " ".join(["\n".join(func) for func in code] ) )
	print(vars, funcs)

def addParams(params) :
	for param in params :
		addVar(param)

def getVar(var) :
	if not vars.get(var) :
		addVar(var)
	return vars[var]
	

def addVar(var) :
	global varc
	varc += 1
	vars[var] = str(varc * -4) + "(%ebp)"
	return vars[var]

def clearVars() :
	global varc
	varc = 0
	vars = dict()

def doHeader(header) :
	headtokens = [token for token in headerpat.match(header).groups() if token and "," not in token]
	funcs.append(headtokens[0])
	addParams(headtokens[1:])
	
def compileFunc(function) :
	trans = []
	doHeader(function[0])

	for line in function[1:] :
		trans.append(compile(partition(line)))
	
	clearVars()
	return "\n".join([line for line in trans if line])


print("Before")
opswitch = { 	"+" : "addl %ebx, %eax",
		"-" : "subl %ebx, %eax",
		"*" : "imull %ebx, %eax",
		"/" : "idivl %ebx, %eax",
		"**": "call pow",
		"%" : "idivl %ebx, %eax\nmovl %edx %eax",
	     	"+u": "",
		"-u": "negl %eax", 
		"~u" : "idivl %eax, $1",
		"==": "call equals", 
		"!=": "call notEquals",
	     	"<" : "call lesser", 
		"<=": "call lesserEquals", 
		">" : "call greater", 
		">=": "call greaterEquals",
		"&" : "and %ebx, %eax",
		"|" : "or  %ebx, %eax",
		"^" : "xor %ebx, %eax",
		"!u" : "not %eax",
		"=" : "movl %eax (%ebx)" }
print("After")

def partition(line) :
	other = ""
	for i in range(len(line)) :
		cl = line[i]
		co = other[-1:]
		
		if (isSymbol(cl) and not isSymbol(co)) :
			other += " "
		elif (cl.isalnum() and not co.isalnum()) :
			other += " "
		other += cl

	print(line, " : ", other)
		
	return [token.strip() for token in other.split()]
		
def isSymbol(c) :
	return c in opswitch

def compile(expr) :
	if len(expr) == 1 :
		return doAtom(expr[0])

	for symbols in symbolLists :
		if match(assign, expr) :
			pos, op = closest(symbols, expr)
			return doOp(expr[:pos], op, expr[pos+1:])
	if match(unary, expr) :
		pos, op = firstUni(expr)
		return doUn(op, expr[1:])
	print("Invalid Expression ! -- " + " ".join(expr))

assign = [ "=" ]
relat = ["==", "!=", "<", ">", "<=", ">="]
logic = [ "&", "|", "^" ]
arith = [ "+", "-", "*", "/", "**", "%" ]
unary = [ "+u", "-u", "~u", "!u" ]
symbolLists = [assign, logic, relat, arith]

def doAtom(expr) :
	if isNumber(expr) :
		return "movl $" + expr + ", %eax"
	elif isVar(expr) :
		return "movl " + getVar(expr) + ", %eax"
	print("ERROR AGAIN -- Not an atom : " + str(expr))

def isNumber(expr) :
	return expr.isdecimal()

def isVar(expr) :
	return expr.isalnum()

def match(symbols, expr) :
	for op in symbols :
		if op in expr :
			return 1
	return 0
	
def closest(symbols, expr) :
	return min( [(p, sym) for p in [find(sym, expr) for sym in symbols] if p != -1] )
	

def doOp(expr1, op, expr2) :
	lines = []
	lines.append(compile(expr1))
	lines.append("pushl %eax")
	lines.append(compile(expr2))
	lines.append("pop %ebx")
	lines.append(opswitch[op])
	return "\n".join([line for line in lines if line])

def doUni(op, expr) :
	lines = []
	lines.append(compile(expr))
	lines.append(opswitch(op))
	return "\n".join([line for line in lines if line])

def find(val, ls) :
	for i, x in enumerate(ls) :
		if x == val :
			return i
	return -1

def iterFuncs(file) :
	pair = 1
	curFunc = []
	for line in file :
		com = line.find("//")
		com = com if com + 1 else len(line)
		if headerpat.match(line) :
			pair = not pair
			if pair :
				yield curFunc
				curFunc = []
		curFunc.append(line[:com])
	yield curFunc


if __name__ == "__main__" :
	print("Hello")
	main()

