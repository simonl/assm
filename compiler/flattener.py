

lformat = r"\{}"
aformat = r"({} {})"
caseformat = r"case {} of "
def flatten(tree) :
	type, *parts = tree
	if type == "lambda" :
		return lformat.format( flatten(parts[0]) )
	elif type == "apply" :
		return aformat.format( *map(flatten, parts) )
	elif type == "record" :
		return "(" + ",".join( map(flatten, *parts) ) + ")"
	elif type == "caseexp" :
		return caseformat.format(parts[0]) + "{ " + " ".join( map(flatten, *parts[1]) ) + " }"
	elif type == "tuple" :
		return "(" + ",".join(["*"+str(part[1]) for part in parts[0]]) + ")"
	elif type == "construct" :
		return "(,)"
	return str(parts[0])

