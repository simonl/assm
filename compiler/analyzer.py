
def analyze(tree) :
	result = check(*tree)
	if not result :
		raise Exception("Invalid Type!")
	else :
		return result


types = []
def check(type, parts) :
	if type == "lambda" :
		val = ("funtype", [check(*parts[0]), check(*parts[1])])
		remvar()
		return val
	elif type == "apply" :
		return checkApply(parts[0], parts[1])
	elif type == "declaration" :
		return checkDecl(parts[0], parts[1])
	elif type == "number" :
		return ("type", "Int")
	elif type == "character" :
		return ("type", "Char")
	elif type == "string" :
		return resolve( ("type", "String") )
	elif type == "variable" and parts in ("true", "false") :
		return resolve( ("type", "Bool") )
	elif type == "primitive" :
		return checkPrim(*parts)
	elif type == "forall" :
		return checkForall(*parts)
	elif type == "type" :
		return (type, parts)
	return lookup(parts)

#Boolean = True 
#	 | False

def checkApply(func, arg) :
	ftype = check(*func)
	atype = check(*arg)

	if ftype[0] != "funtype" :
		raise Exception("Should be funtype!", tostr(ftype), "::", func)
	else :
		set = checkEq(ftype[1][0], atype)
		for fro, to in set :
			ftype[1][1] = replace(fro, to, ftype[1][1])
	return ftype[1][1]

def checkEq(type1, type2) :
	if type1 == type2 :
		return []
	elif type1[0] in ("funtype", "constype") :
		if type2[0] == type1[0] :
			return checkEq(type1[1][0], type2[1][0]) + checkEq(type1[1][1], type2[1][1])
	elif type1[0] == "variable" :
		return [(type1, type2)]
	raise Exception("Incompatible types!", tostr(type1), "!=", tostr(type2))


typedefs= {}
def checkDecl(type, var) :
	global types
	type = resolve(type)
	types = [(var, type)] + types
	return type

def resolve(type) :
	if type[0] == "type" and type in typedefs :
		return typedefs[type]
	return type

opclasses = [
		([("type", "Int"), ("type", "Int"), ("type", "Int")], ["+", "-", "*", "/", "%"]),
		([("type", "Int"), ("type", "Int"), ("type", "Bool")], ["<", "<=", "==", "!=", ">=", ">"])
		]

def checkPrim(arg1, op, arg2) :
	t1 = check(*arg1)
	t2 = check(*arg2)
	for type, ops in opclasses :
		if op[1] in ops :
			if t1 != type[0] or t2 != type[1] :
				raise Exception("Type mismatch in primitive op!", tostr(t1), tostr(t2), "!=", tostr(type[0]), tostr(type[1]))
			return type[2]
	raise Exception("Unknown operation!", op)

def checkForall(variable, body) :
	print(variable, body)
	return check(*body)

def lookup(name) :
	for var, type in types :
		if var[1] == name :
			return type
	raise Exception("Variable not found!", name)

def remvar() :
	global types
	types = types[1:]

def replace(fro, to, tree) :
	(type, parts) = tree
	if type in ("funtype", "constype") :
		return (type, [replace(fro, to, part) for part in parts]) 
	if tree == fro :
		return to
	return tree


def tostr(type) :
	(type, parts) = type
	if type in ("type", "variable") :
		return parts
	return "(" + tostr(parts[0]) + ("->" if type == "funtype" else " ") + tostr(parts[1]) + ")"


import lexer
import parser
import unsugarer
import copy

if __name__ == "__main__" :
	unsugarer.load("lang.uns")
	lexer.load("lang.lex")
	parser.load("lang.par")

	typedefs[("type", "Bool")] = ("funtype", [("variable", "a"), ("funtype", [("variable", "a"), ("variable", "a")])])
	typedefs[("type", "String")]=("constype", [("type", "List"), ("type", "Char")])
	typedefs[("type", "Pair")] = ("funtype", [("funtype", [("variable", "a"), ("funtype", [("variable", "b"), ("variable", "c")])]), ("variable", "c")])


	print( tostr(analyze( unsugarer.unsugar(parser.parse(lexer.lex(
		r"(\(a->b)::x.(x x))"
	))))))

