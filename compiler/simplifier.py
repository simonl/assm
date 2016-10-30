def simplify(tree) :
	return tree
#	return toIndex(tree)

def toIndex(tree, table=[]) :
	(type, parts) = tree
	if type == "apply" :
		return indexApply(table, *parts)
	elif type == "lambda" :
		return indexLambda(table, *parts)
	elif type == "variable" :
		return lookup(parts, table)
	elif type == "caseexp" :
		return indexCase(table, *parts)
	elif type == "construct" :
		return tree
	raise Exception("Illegal Expression!", tree)

def indexApply(table, f, x) :
	return ("apply", toIndex(f, table), toIndex(x, table))

def indexLambda(table, var, body) :
	return ("lambda", toIndex(body, [var[1]] + table))

def lookup(var, table) :
	if var not in table :
		raise Exception("Undeclared variable!", var, table)
	return ("index", table.index(var))

def indexCase(table, scrut, conts) :
	return ("caseexp", toIndex(scrut, table), [toIndex(cont, table) for cont in conts])
