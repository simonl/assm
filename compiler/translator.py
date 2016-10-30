#!/usr/bin/python3

datasection = ["\n\n.section .data"]
textsection = ["\n\n.section .text",
		"main:", 
		"enter $0, $0", 
		"pushl Null", 
		"pushl $lambda0", 
		"call __lambda__", 
		"pushl %eax", 
		"call __force__", 
		"leave\nret $4\n\n"]
lambdaCount = 0
vars = []

globals = ["add", "mul", "sub", "div", "cond", "cons", "ycomb", "map", "filter", "truel", "falsel"]

def flush() :
	global textsection, lambdaCount, vars
	textsection = []
	vars = []
	lambdaCount = 0
	
def getresult() :
	return '.include "../lambdatest.s"\n' + "\n".join(datasection) + "\n".join(textsection)

def translate(tree) :
	lines = []

	type = tree[0]
	parts = tree[1]
	if type == "number" :
		lines.append( value(parts) )
	elif type == "character" :
		lines.append( value(parts) )
	elif type == "variable" :
		lines.append( lookup(parts) )
	elif type == "string" :
		lines.append( string(parts) )
	elif type == "nil" :
		lines.append( null() )
	elif type == "apply" :
		lines.append( translate(parts[1]) )
		lines.append( push() )
		lines.append( translate(parts[0]) )
		lines.append( push() )
		lines.append( apply() )
	elif type == "valueat" :
		lines.append( translate( ("number", "24") ) )
	elif type == "lambda" :
		lines.append( closure() )
		#addvar(parts[0])
		addfunc(parts[0])
		#remvar()
	elif type == "primitive" :
		lines.append( translate(parts[2]) )
		lines.append( push() )
		lines.append( translate(parts[0]) )
		lines.append( translate(parts[1]) )
	elif type == "operator" :
		lines.append( "popl %ebx\n" + ops[parts] )
	elif type == "index" :
		lines.append(
		"pushl $" + parts + "\npushl 8(%ebp)\ncall __get__" )

	return "\n".join(lines)


relatform = "pushl %ebx\npushl %eax\ncall __{}__"
ops = {"+":"addl %ebx, %eax", "-":"subl %ebx, %eax", "*":"mull %ebx",
	"/":"xorl %edx, %edx\ndivl %ebx", "%":"xor %edx, %edx\ndivl %ebx\n movl %edx, %eax",
	":":"pushl %ebx\npushl %eax\ncall __cons__", ">":relatform.format("lgt"),
	"<":relatform.format("llt"), "==":relatform.format("leq"),
	"++":relatform.format("concat")}

def addvar(var) :
	global vars
	vars = [var[1]] + vars

def remvar() :
	global vars
	vars = vars[1:]

def addfunc(exp) :
	global lambdaCount
	lines = ["\nlambda" + str(lambdaCount) + ":"]
	lambdaCount += 1

	lines.append( "enter $0, $0" )
	lines.append( translate(exp) )
	lines.append( "leave\nret $4\n" )
	textsection.append( "\n".join(lines) )

def lookup(var) :
	if var in vars :
#		return "movl 8(%ebp), %eax\n" + ("movl 4(%eax), %eax\n" * vars.index(var)) + "movl (%eax), %eax"
		return "pushl $" + str(vars.index(var)) + "\npushl 8(%ebp)\ncall __get__"
	elif var in globals :
		return "movl $" + var + ", %eax"
	raise Exception("Unfound variable!", var)

def string(s) :
	num = str(len(datasection))
	length = str(len(s)-2)
	datasection.append( ".int " + length + "\nstring" + num + ":\n.ascii " + s )
	return "movl $string" + num + ", %eax"

def push() :
	return "pushl %eax"

def null() :
	return "movl Null, %eax"

def value(val) :
	return "movl $" + val + ", %eax"

def apply() :
	return "call __apply__"

def force() :
	return "call __force__"

def closure() :
	return "\n".join( ["pushl 8(%ebp)", "pushl $lambda" + str(lambdaCount), "call __lambda__"] )

def thunk() :
	return closure()
