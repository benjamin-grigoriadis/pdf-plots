import numpy as np
import os.path

class Search(object):
	'This class searches the absolute paths of data files for the given object. Operation: Searches first directory. Uses the found directory as a start for searching files. Uses last found directory to search new files.'
	search_input = ''
	n_cases = 0
	#absolute_path_first
	def __init__(self, filename):	
		self.filename = filename 
		#self.absolute_paths
		
#--------Searching the data files------------

	def abs_path(self):			 	
		if Search.search_input == '':
			Search.search_input = raw_input("Give folder name or absolute path to the directory of the case(s).\n") #Setting class attribute.
			self.search() 
			Search.absolute_path_first = self.absolute_paths[0]	#Sets class attribute absolute_path_first: path for the next search to begin from.
		else: #The search for the second data file path starts from the folder of the last found file.
			if len(Search.search_input.split()) > 1:
				self.search() 	
			else:
				absolute_path_dirs = []
				for case in range(Search.n_cases):
					absolute_path_dirs.append(os.path.dirname(Search.absolute_path_first[case])) #The starting directory for find_file function must be a list.  
				self.find_file(absolute_path_dirs) 

#---------Functions for searching folders----

	def search(self): #Calls the find_directory and find_file functions and iterates the search with different starting directorys.
		if '/' not in Search.search_input: #Indicates if the user has given an absolute path or a directory name.
			#Find directory(s):
			absolute_path_dirs = []
			search_input_splitted = Search.search_input.split()
			print('Searching the directory...')
			for dirname in search_input_splitted:
				if self.find_directory(os.curdir, dirname) != None:
					absolute_path_dirs.append(self.find_directory(os.curdir, dirname)) #Directory name search for several specific cases.
			if len(absolute_path_dirs) < len(search_input_splitted):
				print('The directory(s) were not found in the current working directory. Trying a wider search.')
				absolute_path_dirs = []
				for dirname in search_input_splitted:
					absolute_path_dirs.append(self.find_directory(os.path.expanduser("~"), dirname))

			#Calculates number of cases:
			if Search.n_cases == 0:	#Checks if n_cases has been calculated already.
				for absolute_path in absolute_path_dirs:
					n_cases_previous = self.n_cases_check(absolute_path)
					Search.n_cases += n_cases_previous
				print(str(Search.n_cases)+' case(s) were found.')

			#Find files:			
			self.find_file(absolute_path_dirs)
	
		else: #When absolute path given as input.
			Search.n_cases = self.n_cases_check(Search.search_input) 
			print(str(Search.n_cases)+' case(s) were found.')
			absolute_path_dirs = []
			absolute_path_dirs.append(Search.search_input)
			self.find_file(absolute_path_dirs)			

#------Function for finding directory path---

	def find_directory(self, starting_directory, dirname):
		for root, dirs, files in os.walk(starting_directory, topdown=True):
			dirs[:] = [d for d in dirs if not d.startswith(".")] #For faster searching excluding files starting with .* from being searched.
			for dir_name in dirs: #Finding dirs. 
					if dir_name == dirname:
						absolute_path = os.path.abspath(os.path.join(root, dir_name))
						return absolute_path

#-----Calculate and check how many cases-----

	def n_cases_check(self, absolute_path):	#Checks if the found/given directory is direct case or a folder for cases.
		n_cases = 1
		folder_or_case = 0
		for case_dir in os.listdir(absolute_path):
			if os.path.exists(absolute_path+'/'+case_dir+'/'+self.filename):
				n_cases += 1
				folder_or_case = 1
		n_cases = n_cases - folder_or_case
		return n_cases #Returns number of cases in the found/given folder or if it is a direct case n_cases = 1.

#----------Function for finding file path----

	def find_file(self, starting_directorys): #Finds the absolute path of the files' directory 
		absolute_paths = np.empty((3,0)).tolist() #[[absolute_path], [absolute_path_grid_inp], [absolute_path_parameters]]
		print('Searching the files...')	
		i = 0
		for b in range(len(starting_directorys)):
			for root, dirs, files in os.walk(starting_directorys[b], topdown=True):
				dirs[:] = [d for d in dirs if not d.startswith(".")] #For faster searching excluding files starting with .* from being searched.
				for name in files: #Finding files.
					if name == self.filename:
						if len(absolute_paths[0]) != Search.n_cases:	
							absolute_paths[0].append(os.path.abspath(os.path.join(root, name)))	#Append the absolute path of file.
							absolute_paths[1].append(os.path.join(os.path.dirname(absolute_paths[0][i]), 'grid.inp')) #Append the absolute path of grid.inp.
							absolute_paths[2].append(os.path.join(os.path.dirname(absolute_paths[0][i]), 'parameters')) #Append the absolute path of parameters.
							print('The file(s) were found in ' + absolute_paths[0][i])	
							i = i + 1
		setattr(self, 'absolute_paths', absolute_paths)	#Sets object attribute absolute_paths: a list of absolute paths to the folder of the file. 


#----------------Main------------------------

#def main():
#	dataPathsAll = [Search(filename) for filename in ['outkhi', 'outpfl', 'outqfl']]
#	for dataPaths in dataPathsAll:
#		dataPaths.abs_path()
#	for dataPaths in dataPathsAll:
#		print(dataPaths.absolute_paths)
#main()




