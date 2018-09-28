#! /usr/bin/python3

import sys
import re
from concordance import concordance

def concord(fileList, isHTML):
	#master dictionary to keep everything in, it will have
	#key = filename, value = concordance dictionary
	masterDict = {}

	for file in fileList:
		masterDict[file] = concordance(file, False)

	finalDict = {}

	#final dict will look like this:
	#{word: [{filename:linenumbers}, totalOccurences]}
	for files, concordDicts in masterDict.items():
		#loop through, making the word a key and the occurences a value
		for word, lineNumbers in concordDicts.items():
			if word in finalDict:
				finalDict[word][0][files] = lineNumbers
				finalDict[word][1] += len(lineNumbers)
			else:
				finalDict[word] = [{}, 0]
				finalDict[word][0][files] = lineNumbers
				finalDict[word][1] += len(lineNumbers)

	#here we can add the toggle for html vs. normal output
	if isHTML:
		printConcordDictHTML(finalDict)
	else:
		printConcordDictRegular(finalDict)


def printConcordDictRegular(cDict):
	#enter a loop where we are sorting the dict for 
	for key in sorted(cDict):
		print(key, "(%d):" % cDict[key][1])
		#loop through each file and show line numbers
		for file in sorted(cDict[key][0]):
			print("\t%s: " % file, end = "")
			#print out all of the line numbers, need to detect repeats
			prevNum = 0
			repeatCounter = 1
			firstPass = True
			for number in cDict[key][0][file]:
				#if this is a repeating number (reliable because lines are in order in list)
				if prevNum == number:
					repeatCounter += 1
					continue
				else:
					#if we have a prevNum and we need to display the repeat counter
					if repeatCounter != 1:
						print("(%d), " % repeatCounter, end = "")
						repeatCounter = 1
					else:
						if firstPass == False:
							print(",",end = " ")
						else:
							firstPass = False
					#print out line number, store prevNum
					print("%d" % number, end = "")
					prevNum = number
			#if we have a repat counter at the end, we need to print the repeat amount still
			if repeatCounter != 1:
				print("(%d)" % repeatCounter, end = "")
			print()

def printConcordDictHTML(cDict):
	#enter a loop where we are sorting the dict for 
	print("<table border = \"1\">")
	#making a first row that shows what each column means
	print("<tr>")
	print("<td>Word (freq.)</td><td>Filename and line number this word occured on.</td>")
	print("</tr>")
	for key in sorted(cDict):
		print("<tr>")
		print("<td>")
		print(key, "(%d):" % cDict[key][1])
		#loop through each file and show line numbers
		print("<td>")
		isFirstFile = True
		for file in sorted(cDict[key][0]):
			if isFirstFile == False:
				#seperates files with a '|'
				print(" | ", end = "")
			else:
				isFirstFile = False
			print("%s: " % file, end = "")
			#print out all of the line numbers, need to detect repeats
			prevNum = 0
			repeatCounter = 1
			firstPass = True
			for number in cDict[key][0][file]:
				#if this is a repeating number (reliable because lines are in order in list)
				if prevNum == number:
					repeatCounter += 1
					continue
				else:
					#if we have a prevNum and we need to display the repeat counter
					if repeatCounter != 1:
						print("(%d), " % repeatCounter, end = "")
						repeatCounter = 1
					else:
						if firstPass == False:
							print(",",end = " ")
						else:
							firstPass = False
					#print out line number, store prevNum
					print("%d" % number, end = "")
					prevNum = number
			#if we have a repat counter at the end, we need to print the repeat amount still
			if repeatCounter != 1:
				print("(%d)" % repeatCounter, end = "")
		print("</td>")
		print("</td>")
		print("</tr>")
	print("</table>")


def main():
	if(len(sys.argv) > 1):
		isHTML = False
		filenames = sys.argv[1:]
		#have to take out first argument of sys.argv (the executable)
		if(len(sys.argv) > 2):
			if(sys.argv[1] == "-h"):
				print("HTML output selected.")
				isHTML = True
				filenames = sys.argv[2:]

		
		concord(filenames, isHTML)
	else:
		print("Please enter a list of filenames as arguments to show a concord dictionary.")


if __name__ == '__main__':
	main()
	
