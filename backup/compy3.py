import sys
import re

terminals = [
	( "NUMBER", re.compile(r"\d+") ),
	( "NEWLINE", re.compile(r"\n") ),
	( "BLOCKTAB", re.compile(r"\t") ),
	( "IDENTIFIER", re.compile(r"[a-zA-Z_]\w*") ),
	( "ADDRESS", re.compile(r"&[a-zA-Z_]\w*") ),
	( "OPEN_PAREN", re.compile(r"\(") ),
	( "CLOSE_PAREN", re.compile(r"\)") ),
	( "COMMA", re.compile(r",") ),
	( "OPERATOR", None ) 
	]

whitespace = re.compile(r"[ \r\f\v]+")

def lexer(text) :
	text = "".join(whitespace.split(text))

	tokens = []
	
	while text :
		type, token = nextToken(text)
		text = text[len(token):]
		tokens.append(type)
		tokens.append(token)
	return tokens

def fix(tokens) :
	tokens = [line for line in tokens if line]
	while True :
		break
	return tokens

def nextToken(text) :
	for name, matcher in terminals :
		found = matcher.match(text)
		if found :
			tok = found.group()
			return  (name, tok)

opTable = dict()

def getOperators() :
	with open("operators.conf", "r") as opFile :
		specs = [line.split() for line in removeComments(opFile.read()).split("\n") if line.strip()]
	return specs

def initOperators() :
	global teminals, opTable

	specs = getOperators()

	symbols = r""
	for line in specs :
		if len(line) == 3 :
			opTable[line[0]] = (line[2], [])
		else :
			opTable[line[0]][1].append( (line[1], line[3:]) )
			safeOp = ["["+c+"]" for c in line[1]]
			symbols += "".join(safeOp) + r" "
	symbols = "|".join( reversed( sorted( symbols.split(), key=len ) ) )
	last = len(terminals)-1
	terminals[last] = ( terminals[last][0], re.compile(symbols) )

def tryLexer() :
	initOperators()
	for token in lexer("44 = = 3 3 ** 2 + __add__(4 - 2, 5)") :
		print("\t", token)








def compile(code) :
	code2 = removeComments(code).split("\n")
	code = [unOperate(clean(line)) for line in code2 if line]
	initVars(code)
	print(vars)

	#print(code)
	pad = len(max(code2, key=len))

	instructions = ""
	for i, line in enumerate(code) :
		print(code2[i], " " * (pad - len(code2[i])) + "\t", line)
		tree = tokenize(line.strip())
		#print(tree, "\n")
		instructions += "\n#" + line + "\n" + evaluate(tree)
	#print(instructions)

	return intro + "\n.type main,@function\nmain:\n" + "subl $" + str(len(vars)*4) + ", %esp\n" + instructions + "\nleave\nret\n"

ops = dict()
symbols = []
delimeters = ["(", ")", "{", "}", "[", "]", ";", ","]
opDispatch = dict()

def setupOps2() :
	global ops, symbols

	with open("operators.conf", "r") as opFile :
		ops = [ line.split() for line in removeComments(opFile.read()).split("\n") if line.strip() ]
	symbols = [op[2] for op in ops]
	sortOps()

def setupOps() :
	global ops, symbols
	with open("operators.conf", "r") as opFile :
		for line in removeComments(opFile.read()).split("\n") :
			if line.strip() :
				doOpLine(line.split())

def doOpLine(line) :
	global ops, symbols
	rank = line[0]
	if len(line) == 3 :
		ops[rank] = (line[2], [])
	else :
		ops[rank][1].append( (line[1], line[3:]) )
		symbols.append(line[1])



def findIn(tokens, sub, subs) :
	return findAll(tokens, sub, subs)

def findPre(tokens, sub, subs) :
	return findAll(tokens, sub, subs)

def findPost(tokens, sub, subs) :
	return findAll(tokens, sub, subs)

def findOut(tokens, sub, subs) :
	indices = []
	for i, token in enumerate(tokens) :
		if token == sub[0] :
			close = findClose(tokens[i:], sub[1]) + i
			indices.append( (i, close, subs) )
	return indices

def findClose(tokens, close) :
	open = tokens[0]
	count = 0
	for i, tok in enumerate(tokens) :
		if tok == open :
			count += 1
		elif tok == close :
			count -= 1
			if count == 0 :
				return i

findAllDispatch = {"infixr":findIn, "infixl":findIn, "prefix":findPre, "postfix":findPost, "outfix":findOut}

def unOperate(tokens) :
	for rank, (type, opers) in reversed(sorted(ops.items())) :
		indices = getIndices(tokens, type, opers)
		#indices = findAllDispatch[type](tokens, opers[0])
		if indices :
			opDispatch[type](tokens, indices)
	return "".join(tokens)
		
def getIndices(tokens, type, symbols) :
	ops = [op for op, subs in symbols]
	subs = [subs for op, subs in symbols]

	indices = []
	for i, token in enumerate(tokens) :
		if token in ops :
			if valid(tokens, i, type) :
				indices.append( (i, subs[ops.index(token)]) )
	return indices

def valid(tokens, index, type) :
	next, prev = nextTok(tokens, index), prevTok(tokens, index)
	if "infix" in type :
		if next == -1 or prev == -1 :
			return False
		if hasValue(tokens[next]) and hasValue(tokens[prev]) :
			return True
	elif "prefix" in type :
		if next == -1 :
			return False
		if hasValue(tokens[next]) and (prev == -1 or not hasValue(tokens[prev])) :
			return True
	elif "postfix" in type :
		if prev == -1 :
			return False
		if hasValue(tokens[prev]) and (next == -1 or not hasValue(tokens[next])) :
			return True
	elif "outfix" in type :
		return True
	return False

def hasValue(token) :
	return token not in symbols and token not in delimeters

def subFunc(name, *args) :
	return name + "(" + ",".join(args) + ")"

def subMethod(name, *args) :
	return args[0] + "." + name + "(" + ",".join(args[1:]) + ")"

def subLiteral(name, *args) :
	return name.format(*args)

subDispatch = {"function":subFunc, "method":subMethod, "literal":subLiteral}
def doInr(tokens, places) :
	doIn(tokens, reversed(sorted(places)))

def doInl(tokens, places) :
	doIn(tokens, sorted(places))

def doIn(tokens, places) :
	for index, subs in places :
		next, prev = nextTok(tokens, index), prevTok(tokens, index)
		tokens[index] = subDispatch[subs[0]]("".join(subs[1:]), tokens[prev], tokens[next])
		tokens[next], tokens[prev] = "", ""
	return tokens

def doOut(tokens, places) :
	for start, end, subs in places :
		result = unOperate(places[start+1:end])

def nextTok(text, index) :
	for i, tok in enumerate(text[index+1:]) :
		if tok :
			return index + i + 1
	return -1

def prevTok(text, index) :
	for i, tok in enumerate(reversed(text[:index])) :
		if tok :
			return index - i - 1
	return -1

def doPre(text, places) :
	places = reversed(sorted(places))
	for place, subs in places :
		next, prev = nextTok(text, place), prevTok(text, place)
		text[place] = subDispatch[subs[0]]("".join(subs[1:]), text[next])
		text[next] = ""
	return text

def doPost(text, places) :
	places = sorted(places)
	for place, subs in places :
		next, prev = nextTok(text, place), prevTok(text, place)
		text[place] = subDispatch[subs[0]]("".join(subs[1:]), text[prev])
		text[prev] = ""
	return text

def doOut(text, places) :
	pass

opDispatch = {"infixr" : doInr, "infixl" : doInl, "prefix" : doPre, "postfix" : doPost, "outfix": doOut}

def findAll(tokens, sub, subs) :
	return [ (i, subs) for i, token in enumerate(tokens) if token == sub]

def clean(text) :
	text2 = text
	buffer = ""
	tokens = []
	text = "".join(text.split())
	while text :
		if validToken(text) :
			tokens.append(text)
			text, buffer = buffer, ""
		else :
			text, buffer = text[:-1], text[-1:] + buffer
	return tokens


def validToken(tok) :
	if tok in symbols :
		return True
	if tok in delimeters :
		return True
	if isId(tok) :
		return True
	return False

def isId(tok) :
	for c in tok :
		if not (c.isalnum() or c == "_") :
			return False
	return True

def initVars(code) :
	code = "\n".join(code)
	start = 0
	while True :
		index = code.find("&", start)
		if index == -1:
			break
		end = endOfRef(code, index)
		makeVar(code[index+1:end].strip())
		start = end

def endOfRef(code, index) :
	for i, c in enumerate(code[index:]) :
		if c == "(" or c == "," or c == ")" :
			return i + index
	return len(code)

def removeComments(code) :
	return removeLineComments(removeBlockComments(code))

def removeBlockComments(code) :	
	while True :
		start = code.find("/*")
		if start == -1 :
			break
		end = code.find("*/", start + 2)
		if end == -1 :
			code = code[:start]
			break
		code = code.replace(code[start:end+2], "")
	return code

def removeLineComments(code) :
	lines = []
	for line in code.split("\n") :
		index = line.find("//")
		if index == -1 :
			lines.append(line)
		else :
			lines.append(line[:index])
	
	return "\n".join(lines)		

def tokenize(code) :
	if isAtom(code):
		return [code.strip()]
	elif isList(code) :
		return parseParams(code)
	elif isFunction(code) :
		return parseFunction(code)	

def parseFunction(call) :
	open = call.find("(")
	close = call.find(")", -1)
	return [[call[:open].strip()], parseParams(call[open+1:close])]

def parseParams(params) :
	tokens = []
	count = 0
	start = 0
	for index,  c in enumerate(params) :
		if c == "(" :
			count += 1
		elif c == ")" :
			count -= 1
		elif c == "," and count == 0 :
			tokens.append(tokenize(params[start:index]))
			start = index + 1
	tokens.append(tokenize(params[start:]))
	return tokens

def isAtom(token) :
	return token.find("(") == -1 and token.find(",") == -1

def isFunction(token) :
	comma = token.find(",")
	if comma == -1 :
		return True
	part = token[:comma]
	return part.count("(") - part.count(")") != 0

def odd(n) :
	return n % 2 != 0

def isNumber(n) :
	return n.isNumeric();

def isList(token) :
	count = 0
	for c in token :
		if c == "," and count  == 0:
			return True
		elif c == "(" :
			count += 1
		elif c == ")" :
			count -= 1
	return False 

def evaluate(tokens) :
	length = len(tokens)
	if length == 1 :
		atom = tokens[0]
		if isNumber(atom) :
			return "movl $" + atom + ", %eax"
		elif isVariable(atom) :
			return getVar(atom)
		elif isReference(atom) :
			return getRef(atom[1:])
		else :
			return "YOU FAIL ATOM" + str(tokens)
	elif length == 2 :
		return evalFunction(tokens[0], tokens[1])
	else :
		return "YOU FAIL!" + str(tokens)

def isNumber(atom) :
	return atom.isnumeric()

def isVariable(atom) :
	return atom in vars or isGlobal(atom)

def isReference(atom) :
	return atom[0] == "&" and isVariable(atom[1:])

def getRef(var) :
	lines = []
	off = vars[var]
	lines.append("movl %ebp, %eax")
	lines.append("movl (%eax), %eax\n" * inCall)
	lines.append("subl $" + off + ", %eax")
	return "\n".join(lines)

def getVar(var) :
	if isGlobal(var) :
		return "movl $" + var + ", %eax"
	return getRef(var) + "\nmovl (%eax), %eax"
	 
def makeVar(var) :
	if var in vars :
		return
	vars[var] = str( 4*(len(vars) + 1))

def evalFunction(name, params) :
	global callCount
	global inCall
	lines = []

	lines.append("			#Calling " + name[0])
	next = "__next__" + str(callCount)
	lines.append("pushl $" + next)
	callCount += 1

	lines.append("pushl %ebp\nmovl %esp, %ebp")
	inCall += 1

	for param in params :
		lines.append(evaluate(param))
		lines.append("pushl %eax")
	lines.append(evaluate(name))
	lines.append("jmp *%eax\n" + next + ":")
	inCall -= 1

	return "\n".join(lines)

def isGlobal(var) :
	return var[:2] == "__" and var[-2:] == "__"

callCount = 0
inCall = 0

vars = {}


def test() :
	testComments()
	testTokenizer()
	testEvaluate()

def testCase(fun, input, output) :
	returned = fun(input)
	print( returned, "==", output)
	assert(returned == output)
	print("\t-- Pass!")

def testComments() :
	print("\n -- Removing comments -- ")
	testCase( removeComments, 
		"this is a /* comment that */ I like", 
		"this is a  I like")
	testCase( removeComments, 
		"this is an /* ending comment", 
		"this is an " )
	testCase( removeComments, 
		"this is // comments that goes \n to the end of line", 
		"this is \n to the end of line" )
	testCase( removeComments, 
		"this is an /* end of \n comment */ on next line", 
		"this is an  on next line" )

def testTokenizer() :
	print("\n -- Tokenizing -- ")
	testCase( tokenize, 
		"__add__(4, __sub__(5, 1))", 
		[["__add__"], [["4"], [["__sub__"], [["5"],["1"]]]]])

	testCase( tokenize, 
		"__sub__(&a, 4, __mul__(5, 2), b)",
		[["__sub__"], [["&a"], ["4"], [["__mul__"], [["5"], ["2"]]], ["b"]]] )

def testEvaluate() :
	print("\n -- Evaluating -- ")
	testCase( evaluate,
		["__add__"],
		"movl $__add__, %eax")
	makeVar("a")
	#testCase( evaluate, 
	#	[["__asg__"], [["&a"], [["__mul__"], [["a"], ["2"]]]]],
	#	evaluate([["__asg__"], [["&a"], [["__mul__"], [["a"], ["2"]]]]]))


intro = "\n".join([
	'.include "std.s"',
	".section .data",
	".section .text",
	".globl _start",
	"_start:",
	"movl %esp, %ebp",
	"pushl $__next__",
	"pushl %ebp",
	"movl %esp, %ebp",
	"jmp main",
	"__next__:",
	"movl %eax, %ebx",
	"movl $1, %eax",
	"int $0x80"])

if __name__ == "__main__" :
	#test()

	#print(" -- Compiling -- ")
	#print(compile("__asg__( &a , __asg__( &b, 5))\n"))
	
	tryLexer()

	ready = True
	setupOps()
	#for rank, (type, mems) in sorted(ops.items()) :
	#	print(rank, " : ", type)
	#	for symbol in mems :
	#		print("\t", symbol)

	#print( unOperate( ["a", ":=", "4", "+", "4", "**", "2", "-", "1"] ) )
	if ready :
		
		#print( unOperate(clean("3+4*5:-+3**2/4:+-2")) )
		filename = sys.argv[1]
		
		with open(filename + ".lang", "r") as inFile :
			input = inFile.read()
		
		output = "\n".join([line.strip() for line in compile(input).split("\n") if line]) + "\n"
		
		with open(filename + ".s", "w") as outFile :
			outFile.write(output)

	
