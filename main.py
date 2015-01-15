import os, sys, re

nb_line = 0
nb_folder = 0
nb_cmp_file = 0

#main class, scan folders and use parsingCodeFile
def main (folder):
	#var
	global nb_cmp_file 
	global nb_folder
	cmpt=1 
	cmd = os.popen("ls -F " + folder)
	cmd = cmd.readlines()
	iterator = 0
	#add here your extension
	list_extension = ["\.c", "\.c\*"]
	re_array = []
	
	#re
	for tmp in list_extension:
		re_array.append(re.compile("([^ ]+)" + tmp + "$"))
	re_folder = re.compile("([^ ]+)/$")


	#recuperation of all files

	#file checking
	for line in cmd:
		iterator = 0
		while (iterator < len(re_array)):
			if (re_array[iterator].match(line)):
				#call parsing of code file
				if (iterator == 0):
					parsing_c_file(folder + line[:len(line) - 1])
				if (iterator == 1):
					parsing_c_file(folder + line[:len(line) - 2])
				nb_cmp_file += 1
			iterator += 1
			
		
		#folder detected, recursivity
		if (re_folder.match(line)):
			main(folder + line[:len(line) - 2] + '/')
			nb_folder += 1

#parsing for C file
def parsing_c_file (name_file):
	global nb_line
	#var
	f_entry = open(name_file, 'r')
	f_exit = open(name_file[:len(name_file) - 2] + ".h", 'w')
	list_function= ["int", "void", "char", "double"]
	is_in = 0
	temp_line = ""
	listTemp = []
	declaration = []
	re_array = []
	iterator2 = 0

	#re
	for tmp in list_function:
		re_array.append(re.compile("^" + tmp))
	reInclude = re.compile("^#include+[(^ )]")

	#parsing of the file
	for line in f_entry:
		iterator = 0
		nb_line += 1

		#detection of include
		if (reInclude.match(line)):
			declaration += line

		#if a re_array is ok
		if (is_in == 1):
			#detection of function
			if ("{" in line):
				for car in temp_line:
					listTemp.append(car)
				listTemp[len(listTemp) - 1] = ';'
				declaration += "".join(listTemp) + '\n'
				listTemp = []
			is_in = 0

		#if a re_array is not ok
		if (is_in == 0):
			iterator2 = 0
			#test of re_array
			while (iterator < len(list_function)):
				while (iterator2 < len(re_array)):
					if (re_array[iterator2].match(line)):
						is_in = 1
					iterator2 += 1
				iterator += 1

		temp_line = line

	for line in declaration:
		f_exit.write(line)



	f_entry.close()
	f_exit.close()

main(sys.argv[1])
print (str(nb_folder) + " folder(s), " + str(nb_cmp_file) + " C file and " + str(nb_line) + " line(s)")
