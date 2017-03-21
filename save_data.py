import numpy as np
import os.path
import search

class Data(search.Search):
	'This class inherits Search class attributes. It reads files from the absolute paths location given by Search class and saves all the data from columns.'
	def __init__(self, filename):
		self.filename = filename
		self.cut_from_beginning = filename[1]
		self.data_columns_list = [] 
		self.data_column_grid_inp = [] 
		self.time_step_list = [] 
		self.lines_paramters = []
		#self.n_columns 
		#search.Search.n_cases
		#self.time_radius_matrix_list

#----------Reading the data files------------

	def lines(self): #Gets all columns from one data (for example outkhi) from each case.
		setattr(self, 'time_radius_matrix_list', np.empty((search.Search.n_cases, 0)).tolist())
		data = []
		data_grid = []
		data_parameters = []
		lines_data = []
		lines_grid_inp = []
		for case in range(0, search.Search.n_cases):
			#Prepare absolute paths for reading the text files: obj_list[object][file_type][case]
			data.append(open(os.path.join(os.path.dirname(self.absolute_paths[0][case]), self.filename)))
			data_grid.append(open(os.path.join(os.path.dirname(self.absolute_paths[1][case]), 'grid.inp')))
			data_parameters.append(open(os.path.join(os.path.dirname(self.absolute_paths[2][case]), 'parameters')))		

			#Save data rows:
			lines_data.append(data[case].readlines()) #Save all data to one list where the elements are the rows.
			lines_grid_inp.append(data_grid[case].readlines())				
			self.lines_parameters.append(data_parameters[case].readlines())

			#Use function data_columns to save data and grid_inp data:
			setattr(self, 'n_columns', len(lines_data[case][0].split())) #Calculates how many colums (parameters) there are in the data.
			self.data_columns_list.append(self.data_columns(lines_data[case], self.n_columns)) #Get the data. List contains data from all cases. The elements are the different cases.
			self.data_column_grid_inp.append(self.data_columns(lines_grid_inp[case], 1)) #Grid_inp file includes radius points of the measurements.

			#Remove 2 last data points from data_column_grid_inp:
			del self.data_column_grid_inp[case][0][-1] #[case][column][data_element]
			del self.data_column_grid_inp[case][0][-1]		
		
			#Data is measured in several different radiuses at one time value. 
			#The data is organized so that each column has this data in different radiuses for one time value.
			#Time_radius_matrix calculates how the data should be divided to a matrix. 
			#i.e relates how many data points there is in total and how many data points are calculated per one time value.
			#time_radius_matrix.extend([len(data_columns_list[case][0]/(len(lines_grid_inp[case])-2), (len(lines_grid_inp[case])-2)]) 
			radius_indices = len(lines_grid_inp[case])-2
			number_of_data_points = len(self.data_columns_list[case][0])
			time_indices = number_of_data_points/radius_indices
			self.time_radius_matrix_list[case] = [time_indices, radius_indices]

			data[case].close() #Closes the text file.
			data_grid[case].close()	#Closes the text file.
		
			#Calculates timestep for each case:
			self.time_step_list.append((self.data_columns_list[case][0][-1]*self.time_radius_matrix_list[case][1])/(len(self.data_columns_list[case][0])-self.time_radius_matrix_list[case][1]))
			#Removes timesteps from the beginning by an amount that user has written in --Enter data-- section. Othervise does not alter the data:
			self.reduce_time_steps(case) 
	
#-------Leave out timesteps from beginning--

	def reduce_time_steps(self, case):
		cut = int(self.time_radius_matrix_list[case][1]*int(self.cut_from_beginning)/self.time_step_list[case])
		for column in range(self.n_columns):
			for i in range(cut):
				del self.data_columns_list[case][column][0]

		updated_number_of_data_points = len(self.data_columns_list[case][0])		
		self.time_radius_matrix_list[case] = [updated_number_of_data_points/self.time_radius_matrix_list[case][1], self.time_radius_matrix_list[case][1]]

#----------Saving the data to vectors--------

	def data_columns(self, lines, n_columns):
		data_columns = np.empty((n_columns, 0)).tolist()#Makes a list containing n amount of empty lists that will be appended.
		for line in lines:	
			if line[0] == "c": #Overlooks the "c" in between data
				pass
			else:
				i = line.split() #Splits the row string after an empty space making a list of the strings.
								 #i.e. i = List of parameters as strings in a row.	
				iii = 0	
				for ii in data_columns: #Taking the empty lists in data_columns.
					ii.append(float(i[iii])) #Appending the lists and changeing data strings to floats.
					iii += 1 #Next index. So appending goes to the next parameter.
		return data_columns

#----------------Main------------------------

#def main():
#	dataColumnsAll = [Data(filename) for filename in ['outkhi', 'outpfl', 'outqfl']]
#	for dataColumns in dataColumnsAll:
#		dataColumns.abs_path()
#		dataColumns.lines()
#	for dataColumns in dataColumnsAll:
#		print(dataColumns.lines_parameters[0])
#		print(len(dataColumns.data_columns_list[0][0]))	#data_columns_list[case][column][data_element]
#main()












