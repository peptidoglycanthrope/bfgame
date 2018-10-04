from copy import copy
import sys, time

def update(tup):
	(p,pc,m,mp,s,c) = tup
	redraw = True
	mem = copy(m)
	stac = copy(s)
	#p  - string containing the program
	#pc - index of the current instruction being executed
	#m  - list representing the memory
	#mp - position of tape head
	#s  - stack containing loop starts to return to
	instr = p[pc]
	if instr == "+":
		mem[mp] += 1
	elif instr == "-":
		if mem[mp] == 0:
			return None
		mem[mp] -= 1
	elif instr == "<":
		if mp == 0:
			return None
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
	elif instr == "]":
		last = stac.pop()
		if m[mp] > 0:
			pc = last-1
	else:
		return None
	return ((p,pc+1,mem,mp,stac,c+1),redraw)

def run(p,steps=1000,t=[0]):
	sys.stdout.write("\033c")
	brackets = 0
	for c in p:
		if c == "[":
			brackets += 1
		elif c == "]":
			if brackets == 0:
				print("Unmatched brackets")
				return None
			brackets -= 1
	if brackets != 0:
		print("Unmatched brackets")
		return None
	
	state = (p,0,t,0,[],0)
	drawState(state)
	for i in range(steps):
		(state, redraw) = update(state)
		drawState(state)
		if state == None:
			print("Crashed")
			return None
		if state[1] == len(p):
			return state
	print("Did not halt after " + str(steps) + " steps")
	return state

def drawState(state):
	(p,pc,m,mp,s,c) = state
	toprow = "╔" + "╦".join(list(map(lambda x: (len(str(x))+2)*"═", m))) + "╦══"
	midrow = "║" + "║".join(list(map(lambda x: (len(str(x))+2)*" ", m))) + "║  "
	datastrings = list(map(lambda x: " " + str(x) + " ", m))
	datastrings[mp] = "[" + datastrings[mp][1:-1] + "]"
	datrow = "║" + "║".join(datastrings) + "║ ..."
	botrow = "╚" + "╩".join(list(map(lambda x: (len(str(x))+2)*"═", m))) + "╩══"
	display = toprow + "\n" + midrow + "\n" + datrow + "\n" + midrow + "\n" + botrow + "\n"
	
	sys.stdout.write("\033[H")
	sys.stdout.write(display)
	sys.stdout.flush()
	time.sleep(.025)
