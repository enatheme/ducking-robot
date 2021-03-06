import os, sys, re

nbLine = 0
nbFolder = 0
nbCfile = 0
target_folder = ""
header_folder = ""


#get arguments
def read_args(argv):
	#var
	number_args = len(argv) - 1
	ret = 0

	#we have arguments
	if (number_args > 0):
		ret = 1
		target_folder = argv[1]
		print("Target folder = %s" % (target_folder))
		if(number_args > 1):
			header_folder = argv[2]
			print("Header folder = %s" % (header_folder))
	return(ret)
		

#read_config function
def read_config():

	#var
	global header_folder
	global target_folder
	re_header_folder = re.compile("^header_folder = ")
	re_target_folder = re.compile("^target_folder = ")

	#we try to open the config file
	try:
		config_file = open(".ducking-robot.cfg", "r")
		
		for line in config_file:
			if re_header_folder.match(line):
				temp = line.split("= ")[1]
				header_folder = temp[:len(temp) - 1]
				print("Header folder = %s" % (header_folder))
			if re_target_folder.match(line):
				temp = line.split("= ")[1]
				target_folder = temp[:len(temp) - 1]
				print("Target folder = %s" % (target_folder))
		return(1)

		config_file.close()
			
	except (IOError, OSError) as e:
		print("Error : %s" % (e))
	return(0)

#main class, scan folders and use parsingCodeFile
def main(folder):
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
	name_exit = (nameFile[:len(nameFile) - 2] + ".h")
	#if we have a header folder:
	if(header_folder != ""):
		temp_name_exit = name_exit.split("/")
		name_exit = header_folder + temp_name_exit[len(temp_name_exit) - 1]
	fExit = open(name_exit, 'w')
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

got_config = 0
if(read_config() == 0):
	print("No config file found, read arguments")
	#we don't have a config file, so we read argument line
	if(read_args(sys.argv) == 0):
		#no args line, print the error message
		print("Usage: python main.py target_folder [header_folder]")
	else:
		got_config = 1
else:
	got_config = 1

if(got_config == 1):
	main(target_folder)
	print ("%s folder(s), %s C file and %s line(s)" % (nbFolder,nbCfile,nbLine))
