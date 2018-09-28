#! /usr/bin/python
import re

#helper function to check if string has alphabet chars
def hasAlphaChars(string):
	if re.search('[a-zA-Z]', string):
		return True
	else:
		return False

def concordance(f, unique=True):
	#make sure the file exists 
	try:
		file = open(f, "r")
	except IOError:
		print("Error: file %s does not exist!" % f)
		return
	print("Successfully opened file %s." % f)

	#we need to keep track of the line number (starts at 1)
	lineCount = 1 
	#we need our dictionary
	concordDict = {}

	for line in file:
		#we need to make sure to convert to lowercase
		line = line.lower()
		splitLine = line.split()

		for word in splitLine:
			if hasAlphaChars(word):
				#we need to put it in the dictionary
				#first, we check if the word is already in there
				if word in concordDict:
					#if unique is true, we have to see if
					#word has already been counted for line
					if unique:
						if lineCount in concordDict[word]:
							continue
						else:
							concordDict[word].append(lineCount)
					else:	
						concordDict[word].append(lineCount)
				#if it isn't, start a new list
				else:
					concordDict[word] = [lineCount]
			else:
				#continue because we are ignoring non-alpha words
				continue 
		#we need to increment linecount
		lineCount += 1

	return concordDict

if __name__ == '__main__':
	print(concordance("declaration.txt"))
	print(concordance("gettysburg.txt"))
