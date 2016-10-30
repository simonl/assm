
def generate(tree) :
	blocks["main"] = genCode(tree)
	main = "main:\n" + blocks.pop("main")
	a = ".code\n" + main + "\n" + "\n".join( [label + ":\n" + body for label, body in sorted(blocks.items())] )
#	print(a)
	return a

label = -1
def fresh() :
	return "L" + str(next())

def next() :
	global label
	label += 1
	return label

blocks = {}
def genCode(tree) :
	type = tree[0]
	if type == "lambda" :
		return "LAM\n" + genCode(tree[1])
	elif type == "apply" :
		arg, *parts = tree[2]
		if arg == "index" :
			return "APPI "  + str(parts[0]) + "\n" + genCode(tree[1])
		lbl = fresh()
		blocks[lbl] = genCode(tree[2])
		if arg == "lambda" :
			return "APPC " + lbl + "\n" + genCode(tree[1])
		return "APP " + lbl + "\n" + genCode(tree[1])
	elif type == "index" :
		return "IND " + str(tree[1]) + "\n"
	elif type == "force" :
		cont = tree[1]
		return "FOR\n" + genCode(cont)
	else :
		raise Exception("AGG!")

# lambda	-> (add "LAM\n" *@)
# apply		-> 

code = ("lambda", 
		("force",
			("index", 0),
			("lambda", ("index", 0))))

#\x. force x in \x.x

import assembler
if __name__ == "__main__" :
	print( generate( code ) )

#	lambda	>> (join "\n" ["LAM \n" *$1])
#	apply	>> do lbl = (fresh) 
#		   then	(join "\n" ["APP " lbl "\n" *$1 (join " :\n" [(fresh) *$2])])
#	index	>> (join "\n" ["IND " (str @) "\n"])
