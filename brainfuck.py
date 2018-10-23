from copy import copy
import sys, time

levelInfo = {
	1 : ("Easy as 1, 2, 3","Write 1 2 3 to the first three cells of the tape.",100, [0]),
	2 : ("kill screen","omae wa mou shinderu",69, [420])
}

class State():
	def __init__(self):
		self.reset()
		self.level = 0

	def reset(self):
		self.p = ""  #string containing the program
		self.pc = 0  #index of the current instruction being executed
		self.m = [0] #list representing the memory
		self.mp = 0  #position of tape head
		self.s = []  #stack containing loop starts to return to
		self.c = 0   #cycle count
		self.redraw = True
		self.message = ""

	def tape(self):
		return (self.p, self.pc, self.m, self.mp, self.s, self.c)

	def checkSolution(self):
		if self.level == 1:
			return self.m == [1,2,3]
		return False

	def setTape(self, tup):
		(self.p, self.pc, self.m, self.mp, self.s, self.c) = tup

	def update(self):
		(p,pc,m,mp,s,c) = self.tape()
		if pc == len(p):
			return False
		self.redraw = True
		mem = copy(m)
		stac = copy(s)
		instr = p[pc]
		if instr == "+":
			mem[mp] += 1
		elif instr == "-":
			if mem[mp] == 0:
				self.message = "Cannot decrement 0."
				return False
			mem[mp] -= 1
		elif instr == "<":
			if mp == 0:
				self.message = "Cannot go left of left edge of tape."
				return False
			mp -= 1
		elif instr == ">":
			if mp >= len(mem)-1:
				mem.append(0)
			mp += 1
		elif instr == "[":
			if m[mp] == 0:
				brackets = 1
				for i in range(pc+1,len(p)):
					if p[i] == "[":
						brackets += 1
					elif p[i] == "]":
						brackets -= 1
					if brackets == 0:
						break
				pc = i
			else:
				stac.append(pc)
			self.redraw = False
		elif instr == "]":
			last = stac.pop()
			if m[mp] > 0:
				pc = last-1
			self.redraw = False
		elif instr == " ":
			pass
		else:
			self.message = "Invalid character."
			return False
		self.setTape((p,pc+1,mem,mp,stac,c+1))
		return True
	
	def generateDisplay(self):
		if self.level == 0:
			display = "wow cool is this a help screen? fuck you\nnah dude sorry about that actually I lied\n\n you're valid\n"
		else:
			(p,pc,m,mp,s,c) = self.tape()
			toprow = "╔" + "╦".join(list(map(lambda x: (len(str(x))+2)*"═", m))) + "╦══"
			midrow = "║" + "║".join(list(map(lambda x: (len(str(x))+2)*" ", m))) + "║  "
			datastrings = list(map(lambda x: " " + str(x) + " ", m))
			datastrings[mp] = "[" + datastrings[mp][1:-1] + "]"
			datrow = "║" + "║".join(datastrings) + "║ ..."
			botrow = "╚" + "╩".join(list(map(lambda x: (len(str(x))+2)*"═", m))) + "╩══"
			info = "Cycles:	%i\nTape used: %i\nProgram length: %i"%(c,len(m),len(p))
			tape = toprow + "\n" + midrow + "\n" + datrow + "\n" + midrow + "\n" + botrow + "\n" + info + "\n"

			display = "Level %i: %s\n%s\nCycle limit: %i\n"%(self.level,levelInfo[self.level][0],levelInfo[self.level][1],levelInfo[self.level][2]) + tape
		display += "\n" + self.message + "\n\n"
		return display

	def drawState(self):
		display = self.generateDisplay()
		# AKI WAS HERE
		# AKI LOVES U <3
		sys.stdout.write("\033c")
		sys.stdout.write("\033[H")
		sys.stdout.write(display)
		sys.stdout.flush()
		time.sleep(.025)

	def run(self,program,steps):
		self.reset()
		sys.stdout.write("\033c")
		sys.stdout.flush() #clear whole terminal
		self.p = program
		for i in range(steps):
			success = self.update()
			if not success:
				return None
			elif self.checkSolution():
				self.message = "Cleared."
				self.drawState()
				input()
				self.level += 1
				self.reset()
			if self.redraw:
				self.drawState()
		self.message = "Hit cycle limit."

def runGame():
	state = State()
	while True:
		if state.level == 0:
			state.drawState()
			inpt = input()
			state.level = 1
		else:
			state.m = levelInfo[state.level][3]
			state.drawState()
			program = input()
			state.run(program,levelInfo[state.level][2])


runGame()