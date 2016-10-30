





states = {}


def drive(string) :
	state = states["start"]
	while state :
		c, string = string[0], string[1:]
		print(c)
		state = states[state[c]]
	return string

if __name__ == "__main__" :
	states["start"] = {"\\":"lambda", "x":"end"}
	states["lambda"] = {"x":"lambda0"}
	states["lambda0"] = {".":"lambda1"}
	states["lambda1"] = {".":"start"}
	states["end"] = {}

	print(drive("\\x.y"))
