# Make Assembler

def load(filename) :
	with open(filename, "r") as file :
		text = file.read()
	tokens = removeComments(text.split("\n")).split()
	return Assembler(makeConfig(tokens))

class Assembler :
	def __init__(self, config) :
		self.config = config
	def assemble(self, text) :
		pass1 = assemblerPass1(text.split())
		pass2 = assemblerPass2(self.config, pass1)
		return pass2

def removeComments(lines) :
	return " ".join(line for line in lines if not line.startswith("%%"))

# End Assembler

# Make Config

def makeConfig(tokens) :
	sections = {}
	for token in tokens :
		if "." in token :
			section, mnemonics = createSection(sections, token[1:])
		elif token.isalpha() :
			opcode, shape = makeInst(mnemonics, token)
			shape.append( getOpcode(opcode) )
		else :
			shape.append( makeParam(section, token) )
	return sections

def createSection(sections, section) :
	if section in sections :
		raise Exception("Define sections in one block please!")
	return section, set(sections, section, {})

def set(dic, k, v) :
	dic[k] = v
	return v

def makeInst(mnemonics, mnemonic) :
	opcode = len(mnemonics)
	return opcode, set(mnemonics, mnemonic, [])

def makeParam(section, param) :
	if "$" in param :
		if param == "$" :
			return paramImmediate()
		else :
			return paramConstant(int(param[1:]))
	elif "#" in param :
		if param == "#" :
			return paramLabel(section)
		else :
			return paramLabel(param[1:])
	else :
		raise Exception("Invalid parameter type!")

def paramImmediate() :
	return (lambda sections, arg : int(arg))

def paramConstant(n) :
	def doIt(sections, arg) :
		if int(arg) == n :
			return n
		else :
			raise Exception("Expecting constant : " + str(n) + "!")
	return doIt

def paramLabel(section) :
	return (lambda sections, arg : getLabels(sections, section)[arg])

def getLabels(sections, section) :
	return sections[section][1]

def getOpcode(opcode) :
	return (lambda sections, arg : opcode)

	
# End Config


# Pass 1

def assemblerPass1(tokens) :
	sections = {}
	for token in tokens :
		if "." in token :
			data, labels = getSection(sections, token[1:])
		elif ":" in token :
			putLabel(labels, token[:-1], len(data))
		else :
			data.append(token)
	return sections

def getSection(sections, section) :
	if section not in sections :
		sections[section] = newSection()
	return sections[section]

def newSection() :
	return [], {}

def putLabel(labels, label, index) :
	if label in labels :
		raise Exception("Can only define a label once!")
	labels[label] = index

# End Pass 1



# Pass 2

def assemblerPass2(config, sections) :
	blocks = {}
	for section, (data, labels) in sections.items() :
		blocks[section] = assembleSection(sections, config[section], data)
	return blocks

def assembleSection(sections, instructions, data) :
	block = []
	iterateList(
		data,
		(lambda index :
			extendBlock( block, assembleInstruction(sections, instructions[data[index]], data[index:])))) 
	return block

def extendBlock(block, ext) :
	before = len(block)
	block.extend(ext)
	return len(block) - before

def assembleInstruction(sections, shape, data) :
	for param, arg in zip(shape, data) :
		yield param(sections, arg)

def iterateList(array, f) :
	indices = whileIn(array)
	try :
		index = f(indices.send(None))
		while True :
			index = f(indices.send(index))
	except StopIteration :
		pass

def whileIn(array) :
	index, limit = 0, len(array)
	while index < limit :
		index += (yield index)

# End Pass 2

# Test VM Generator

def makeVMConfig(tokens) :
	sections = {}
	for token in tokens :
		if "." in token :
			section, mnemonics = createSection(sections, token[1:])
		elif token.isupper() and token.isalpha() :
			mnemonics[token] = shape = [ ]
		else :
			shape.append( "arg" + str(len(shape)) )
	return sections


if __name__ == "__main__" :
	assm2 = load("lang.lasm")
	with open("lambda.lasm") as file :
		code = file.read()
	print(assm2.assemble(code))
	vmConf = makeVMConfig(".code APP # LAM IND $".split())

	for section, mnems in vmConf.items() :
		secPointer = section + "Pointer"
		secBlock = section + "Block"
		globs = "global " + secBlock + ", " + secPointer
		print(secBlock + " = []")
		print(secPointer + " = 0")
		for mnem, shape in mnems.items() :
			print("def _" + section + "_" + mnem + "() :")
			print("\t" + globs)
			for arg in shape :
				print("\t" + arg + " = " + secBlock + "[" + secPointer + "]")
				print("\t" + secPointer + " += 1")
	print("def run() :")
	print("\twhile True :")
	print("\t\toperation = codeBlock[codePointer]")
	print("\t\tcodePointer += 1")
	print("\t\toperation()")
