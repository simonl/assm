#Easy parser

unary = { "+u", "-u", "~u", "!u", "call", "."}
hiArith = { "**" }
midArith = { "*", "%", "/" } 
lowArith = { "+", "-" }
relat = { ">", ">=", "==", "!=", "<=", "<", "is" }
logic = { "&", "|", "^", "&&", "||" }
assign = { ":=", "=", "+=", "-=", "*=", "/=", "%=", "**=" }


#New
opPrecedence = [[":=", "=", "+=", "-=", "*=", "/=", "%=", "**=", "^=", "&=", "|="],
		["&", "|", "^", "&&", "||"],
		[">=", ">=", "==", "!=", "<=", "<", "is"],
		["+", "-"],
		["*", "/", "//", "%"],
		["**"],
		["+u", "-u", "!u", "~u", "."]]
operators = [(op for op in precRank) for precRank in opPrecedence]
#End new


orderPrec = [assign, logic, relat, lowArith, midArith, hiArith]

opswitch = { 	"+" : "addl %ebx, %eax",
		"-" : "subl %eax, %ebx\nmovl %ebx, %eax",
		"*" : "imull %ebx, %eax",
		"/" : "idivl %ebx, %eax",
		"%" : "idivl %ebx, %eax\nmovl %edx, %eax",
		">" : "call _greater",
		">=": "call _greaterEquals",
		"==": "call _equals",
		"is": "call _equals",
		"!=": "call _notEquals",
		"<=": "call _lesserEquals",
		"<" : "call _lesser",
		"&&": "call _and",
		"||": "call _or",
		"&" : "and %ebx, %eax",
		"|" : "or %ebx, %eax",
		"^" : "xor %ebx, %eax",
		"=" : "pushl %eax" }

keywords = dict()
callCount = 0
loopCount = 0
ifCount = 0
vars = []
inCall = False
data = [".section .data"]
dataNum = 0

import re
headerpat = re.compile(r"^\s*\w+\(.*\)")

def flushLocals() :
	global vars
	vars.pop()

def main(code) :
	makeScope()
	makeVar("_if")
	makeVar("_print")
	makeVar("_input")
	makeVar("_inputChar")
	makeVar("_printChar")
	makeVar("_repeat")
	lines = []
	numLines = len(code)
	boolpair = 1
	start = 0
	end = 0
	for index in range(numLines) :
		line = code[index]
		if headerpat.match(code[index]) :
			end = index
			print(code[index], " -- HEADER -- ")
			makeVar(code[index][:code[index].find("(")])
			lines.append(code[start:end])
			start = index
		elif line and 0:
			lines.append(preprogram(line))
	lines.append(code[start:])
	return "\n".join(doFunction(func) for func in lines if func)

def preprogram(line) :
	line = [li.strip() for li in line.split()]
	if line[0] == "import" :
		return doImport(line[1:])
	else :
		return ""

def doImport(sources) :
	lines = []
	for source in sources :
		lines.append(".include " + source)
	return "\n".join(lines)

def doFunction(code) :
	print()
	print(code, " -- FUNC -- ")
	makeScope()
	trans = []
	trans.append(doHeader(code[0]))

	for line in code[1:] :
		trans.append(compile(traverse(line)))

	flushLocals()
	return "\n".join(trans)

def doHeader(header) :
	name, params = formatCall(header)
	
	lines = []
	lines.append(".type " + name + ",@function")
	lines.append(name + ":")
	for param in params :
		makeVar(param)
	return "\n".join(lines)
	

def partition(line) :
	return [token.strip() for token in line.split()]


def compile(tokens) :
	print(tokens, " -- COMP -- ")
	if len(tokens) == 0 :
		return "\n"
	if tokens[0] in keywords :
		return keywords[tokens[0]](tokens[1:])
	if len(tokens) == 1 :
		if isEnclosed(tokens[0]) :
			return compile(traverse(token[1:-1]))
		if isNumber(tokens[0]) :
			return "movl $" + tokens[0] + ", %eax"
		if isString(tokens[0]) :
			return doString(tokens[0])
		return getVar(tokens[0])
	(pos, symb) = findNext(tokens)
	if pos != -1 :
		return doBinOp(tokens[:pos], symb, tokens[pos+1:])
	print(tokens, " -> ", pos,  symb)

def isString(str) :
	return str[0] == "\"" and str[-1:] == "\""

def doString(stri) :
	global data
	global dataNum

	strName = "_dt_" + str(dataNum)
	data.append(strName + ":")
	dataNum += 1
	data.append(".ascii " + stri + "\n")
	return "movl $" + strName + ", %eax\nmovl $" + str(len(stri) - 3) + ", %ebx"

def getVar(var) :
	global inCall

	scope, place = lookup(var)
	if scope == len(vars) - 1 :
		return "movl $" + place + ", %eax"
	if scope != 0 or inCall:
		str = "movl (%ebp), %eax\n" + "movl (%eax), %eax\n" * (scope - 1)
		return str + "movl " + place.replace("bp", "ax") + ", %eax"
	return "movl " + place + ", %eax"

def lookup(var) :
	for i, scope in enumerate(reversed(vars)) :
		for v in scope :
			if v == var :
				return i, scope[v]

def isEnclosed(token) :
	return token[0] == "(" and token[-1:] == ")"

def isNumber(token) :
	if token.isdecimal() :
		return 1
	elif isHex(token) :
		return 1
	elif isOctal(token) :
		return 1
	return 0

def isHex(token) :
	return token[:2] == "0x" and token[2:].isdecimal()

def isOctal(token) :
	return token[:1] == "0" and token[1:].isdecimal()

def ret(value) :
	lines = []
	lines.append(compile(value))
	#lines.append("movl %ebp, %esp")
	#lines.append("popl %ebp")
	lines.append("leave")
	lines.append("ret")
	return "\n".join(lines)

def call(values) :
	name, args = formatCall(" ".join(values))
	print(name, args, " -- CALL -- ")

	lines = []
	preCall, next = prepareCall()
	
	lines.append(preCall)
	lines.append(pushArgs(args))
	lines.append(finalizeCall(name, next))
	return "\n".join(lines)

def finalizeCall(name, next) :
	global inCall 
	out = "\n".join([getVar(name), "jmp *%eax", next + ":"])
	inCall -= 1
	return out
	
def pushArgs(args) :
	lines = []
	for arg in args :
		lines.append(compile(traverse(arg)))
		lines.append("pushl %eax")
	return "\n".join(lines)

def prepareCall() :
	global callCount
	global inCall

	next = "_next_" + str(callCount)
	callCount += 1
	inCall += 1
	return "pushl $" + next + "\npushl %ebp\nmovl %esp, %ebp", next

def formatCall(header) :
	paren = header.find("(")
	return header[:paren], traverse(header[paren+1:-1], ",")

def system(values) :
	lines = []
	lines.append("movl $" + values[0] + ", %eax")
	lines.append("int $0x80")
	return "\n".join(lines)

def traverse(string, sep=" ", base=0) :
	tokens = []
	parenCount = 0
	for i, c in enumerate(string) :
		if c == "(" :
			parenCount += 1
		elif c == ")" :
			parenCount -= 1
		if c == sep and parenCount == 0 :
			tokens.append(string[base:i])
			base = i + 1
	tokens.append(string[base:])
	return [token.strip() for token in tokens if token]

def findNext(tokens) :
	pairs = []
	for rank in orderPrec :
		for symbol in rank :
			for index, token in enumerate(tokens) :
				if symbol == token :
					pairs.append((index, symbol))
		if pairs :
			return min(pairs)
		pairs = []
	return (-1, "Q") 

def doBinOp(exp1, op, exp2) :
	if op == "=" :
		return doAssign(exp1[0], exp2)

	lines = []
	lines.append(compile(exp1))
	lines.append("pushl %eax")
	lines.append(compile(exp2))
	lines.append("pop %ebx")
	lines.append(opswitch[op])
	return "\n".join(lines)

def doAssign(var, exp) :
	lines = []
	lines.append(compile(exp))
	if var in vars :
		lines.append("movl %eax, " + getVar(var))
	else :
		lines.append(makeVar(var))
	return "\n".join(lines)

def makeVar(var) :
	if len(vars) == 1 :
		vars[0][var] = var
		return
	vars[len(vars)-1][var] = str( -4 * (len(vars[len(vars)-1])+1) ) + "(%ebp)"
	return opswitch["="]

def makeScope() :
	vars.append(dict())

def quitScope() :
	vars.pop()

throw = "\n".join([
"movl %eax, __defHandler__",
"unwind_loop:",
"jcmp %ebp, %esp",
"je next",
"cmp ((%esp)), %eax",
"je found",
"incl %esp",
"jmp unwind_loop",
"next:",
"popl %ebp",
"incl %esp",
"jmp unwind_loop",
"found:",
"movl 4((%esp)), %ebx",
"movl %eax, (%esp)",
"jmp %ebx"])

def boiler() :
	return "\n".join ( 
		['.include "STD_IO.s"',
		'.include "Boolean.s"',
		".section .text", 
		".globl _start",
		".globl main",
		"_start:",
		"movl %esp, %ebp",
		"pushl $next",
		"pushl %ebp",
		"movl %esp, %ebp",
		"jmp main",
		"next:",
		"movl %eax, %ebx"] + [system(["1"])] )

def doPrint(text) :
	lines = []
	vars[0]["print"] = "_print"
	vars[0]["str"] = "str"
	
	preCall, next = prepareCall()
	lines.append(preCall)
	lines.append(pushArgs(("str",)))
	lines.append(finalizeCall("print", next))
	return "\n".join(lines)

def isCode(line) :
	return line != "\n" and line[0] != "#"

if __name__ == "__main__" :
	keywords["return"] = ret
	keywords["call"] = call
	keywords["system"] = system
	keywords["print"] = doPrint

	input = ["main()", "a = 3 * 3", "returb a + call other()", 
		"other()", "return 3 + call another(8,5)",
		"another(v, s)", "return v * s"]

	import sys 
	fileName , codes = sys.argv[1], ""

	with open(fileName + ".lang", "r") as f :
		code = [line.strip("\n") for line in f if isCode(line)]

	print(" -- PROGRAM -- ")
	print("\n".join(code) + "\n")
	with open(fileName + ".s", "w") as f :
		f.write(boiler() + "\n" + main(code) + "\n" + "\n".join(data))

#def delimitStmts(text) :
# stmts = []
# curly, square, paren = 0, 0, 0
# start = 0
# for i, char in enumerate(text) :
#	if char == ";" :
#		if curly == square == paren == 0 :
#			stmts.append(text[start:i+1])
#			start = i+1
#	else :
#		update = updateCounts(char)
#		curly += update[0]
#		square += update[1]
#		paren += update[2]
# return stmts

#def updateCounts(char) :
# counts = (0, 0, 0)
# counts[0] = 1 if char == "{" else (-1 if char == "}" else 0)
# counts[1] = 1 if char == "[" else (-1 if char == "]" else 0)
# counts[2] = 1 if char == "(" else (-1 if char == ")" else 0)
# return counts

#def compile(code) :
# return "\n".join(doFunction(func) for func in getFunctions(code) if func)

#def doFunction(func) :
# return "\n".join(evaluate(statement) for statement in func if statement)

#def evaluate(stmt) :
# return "\n".join(apply(develop(polish(parse(stmt)))) 

#def parse(stmt) :
# tokens, term, buffer = [], stmt.strip(), ""
# while term :
#	if isLegal(term) :
#		tokens.append(term)
#		term, buffer = buffer, ""
#	else :
#		stmt, buffer = stmt[:-1], term[-1:] + buffer
# return tokens

#def isLegal(term) :
# if isNumber(term) :
#	return True
# if isString(term) :
#	return True
# if term in operators :
#	return True
# if term in vars :
#	return True
# if isBlock(term) :
#	return True 
# if isEnclosed(term) :
#	return True
# if isArray(term) :
#	return True
# return False

#def isBlock(term) :
# return isEnclosed(term, "{", "}")

#def isEnclosed(term, opened="(", closed=")") :
# if term[0] == opened and term[-1] == closed :
#	return term.count(opened) == term.count(closed)
# return False

#def isArray(term) :
# return isEnclosed(term, "[", "]")

#def polish(tokens) :
# inPolish = []
# 
# for opLevel in rankedOperators :
#	index = minPos(matches(tokens, opLevel))
#	if index != -1 :
#		op = tokens[index]
#		inPolish.append(op)
#		if isBinary(op) :
#			inPolish += polish(tokens[:index])
#			inPolish += polish(tokens[index+1:])
#		elif isUnary(op) :
#			inPolish += polish(tokens[index+1:])
#		break
# return inPolish

#def develop(polishStmt) :
# nodes = polishStmt[:1]
# index = 1
# for count in range(exam(nodes[0])) :
#	operand, index = develop(polishStmt[index:])
#	nodes.append(operand)
# return nodes, index

#def exam(term) :
# if isAtom(term) :
#	return 0
# elif isUnary(term) :
#	return 1
# elif isBinary(term) :
#	return 2 
