import os, sys, re

nbLine = 0
nbFolder = 0
nbCfile = 0
header_folder = ""
test = ""

#read_config function
def read_config():

	#var
	re_header_folder = re.compile("^header_folder = ")

	#we try to open the config file
	try:
		config_file = open(".ducking-robot.cfg", "r")
		
		for line in config_file:
			if re_header_folder.match(line):
				header_folder = line.split("= ")[1]

				
			
	except (IOError, OSError) as e:
		print("Error : %s" % (e))

#main class, scan folders and use parsingCodeFile
def main (folder):
	#var
	global nbCfile
	global nbFolder

	cmpt=1 
	cmd = os.popen("ls -F " + folder)
	cmd = cmd.readlines()
	iterator = 0
	#add here your extension
	listExtension = ["\.c", "\.c\*"]
	reArray = []
	
	#re
	for tmp in listExtension:
		reArray.append(re.compile("([^ ]+)" + tmp + "$"))
	reFolder = re.compile("([^ ]+)/$")


	#recuperation of all files

	#file checking
	for line in cmd:
		iterator = 0
		while (iterator < len(reArray)):
			if (reArray[iterator].match(line)):
				#call parsing of code file
				if (iterator == 0):
					parsingCfile(folder + line[:len(line) - 1])
				if (iterator == 1):
					parsingCfile(folder + line[:len(line) - 2])
				nbCfile += 1
			iterator += 1
			
		
		#folder detected, recursivity
		if (reFolder.match(line)):
			main(folder + line[:len(line) - 2] + '/')
			nbFolder += 1

#parsing for C file
def parsingCfile (nameFile):
	global nbLine
	#var
	fEntry = open(nameFile, 'r')
	fExit = open(header_folder + nameFile[:len(nameFile) - 2] + ".h", 'w')
	listFunction= ["int", "void", "char", "double"]
	isIn = 0
	lineTemp = ""
	listTemp = []
	declaration = []
	reArray = []
	iterator2 = 0

	#re
	for tmp in listFunction:
		reArray.append(re.compile("^" + tmp))
	reInclude = re.compile("^#include+[(^ )]")

	#parsing of the file
	for line in fEntry:
		iterator = 0
		nbLine += 1

		#detection of include
		if (reInclude.match(line)):
			declaration += line

		#if a reArray is ok
		if (isIn == 1):
			#detection of function
			if ("{" in line):
				for car in lineTemp:
					listTemp.append(car)
				listTemp[len(listTemp) - 1] = ';'
				declaration += "".join(listTemp) + '\n'
				listTemp = []
			isIn = 0

		#if a reArray is not ok
		if (isIn == 0):
			iterator2 = 0
			#test of reArray
			while (iterator < len(listFunction)):
				while (iterator2 < len(reArray)):
					if (reArray[iterator2].match(line)):
						isIn = 1
					iterator2 += 1
				iterator += 1

		lineTemp = line

	for line in declaration:
		fExit.write(line)



	fEntry.close()
	fExit.close()
read_config()
#main(sys.argv[1])
#print ("%s folder(s), %s C file and %s line(s)" % (nbFolder,nbCfile,nbLine))
