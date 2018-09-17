import sys
import struct
import time
import os
import psutil

class entry(object):
	n1 = ""
	n2 = ""
	n3 = ""
	w1 = ""
	w2 = ""
	#declare all elements of an entry
	def __init__(self, lis):
		self.n1=lis[0]
		self.n2=lis[1]
		self.n3=lis[2]
		self.w1=lis[3]
		self.w2=lis[4]


	def compareTo(self, other):
		if self.str1 == other.str1:
			return 0;
		elif self.str1 > other.str1:
			return -1
		elif self.str1 < other.str1:
			return 1

	def toString(self):
		return (str(self.n1)+" "+str(self.n2)+" "+str(self.n3)+" "+self.w1+" "+self.w2)

	def size(self):
		return sys.getsizeof(n1)+sys.getsizeof(n2)+sys.getsizeof(n3)+sys.getsizeof(w1)+sys.getsizeof(w2)

	def __gt__(self, other):
		self.w1 > other.w1
	def __lt__(self, other):
		self.w1 <= other.w1

def getKey(item):
	return (item.w1+item.w2)

def readThrough(filename):
	oFile = open( filename, 'rb' )
	start = 0
	end = 0
	tape = []
	count = 0
	otherCount = 0
	tracker = 0
	while True:
		count += 1
		otherCount += 1
		rec = oFile.read( 44 )
		if len(rec) < 44 :
			break
		if end != 0 and count > end :
			break
		if count < start+1:
			continue
		line = struct.unpack( 'qqqbbbbbbbbbbbbbbbbbbbb', rec ) 

		n1 = int( line[0] );
		n2 = int( line[1] );
		n3 = int( line[2] );
		w1 = ''
		for i in range( 3, 13 ):
			w1 = w1 + chr( line[i] )
			w2 = ''
		for i in range( 13, 23 ):
			w2 = w2 + chr( line[i] )

		e = entry( [n1, n2, n3, w1, w2] )
		tape.append(e)

		if (otherCount >= allowedMem or len(rec) < 44 or (end != 0 and count > end) ) and tracker == 0:
			tape=sorted(tape, key=getKey)
			file = open(".Tb1", "a")
			for line in tape:
				file.write(line.toString()+'\n')
			file.close()
			otherCount = 0
			tracker =1
			tape = []
		elif (otherCount >= allowedMem or len(rec) < 44 or (end != 0 and count > end) ) and tracker == 1:
			tape=sorted(tape, key=getKey)
			file = open(".Tb2", "a")
			for line in tape:
				file.write(line.toString()+'\n')
			file.close()
			otherCount = 0
			tracker =0
			tape = []

def merge():
	tb1 = open(".Tb1", "r")
	tb2 = open(".Tb2", "r")
	out = open("sorted.txt", "w")
	e1 = entry(tb1.readline().split(" "))
	e2 = entry(tb2.readline().split(" "))
	e1count = 0 #we will count how many from each we've read.  This will be limited to allowedmem per read
	e2count = 0

	while True:
		if e1count >= allowedMem and e2count >= allowedMem:
			ta1 = open(".Ta1", "w")
			ta2 = open(".Ta2", "w")
			x=tb1.readline()
			while x is not '':
				ta1.write(x)
				x=tb1.readline()
			x=tb2.readline()
			while x is not '':
				ta2.write(x)
				x=tb2.readline()
			ta1.close()
			ta2.close()
			tb1.close()
			tb2.close()
			break
		if (e1 > e2 and e1count < allowedMem) or e2count > allowedMem:
			out.write(e2.toString()+" e2 "+str(e2count))
			if len(e2.w2) < 10:
				out.write("\n")
			e2 = entry(tb2.readline().split(" "))
			e1count += 1
		else:
			out.write(e1.toString()+" e1 "+str(e1count))
			if len(e1.w2) < 10:
				out.write("\n")
			e1 = entry(tb1.readline().split(" "))
			e2count += 1
		



allowedMem = int((int(sys.argv[1])*1024*1024)/200) #number of items we can keep in memory at one time
					      #for 100MB this is ~500,000 objects but a 1GB bin file
					      #will have ~20,000,000 objects so we can only keep
					      #~1/40th that number of objects in memory at a time
print(allowedMem)
open(".Tb1", "w").write("")
open(".Tb2", "w").write("")

readThrough(sys.argv[2])	# readThrough goes through this input file, 
merge()
