import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import math
import search
import save_data

class Plot_pdf(save_data.Data, search.Search):
	'This class inherits class attributes from Data and Search classes. It uses the data from Data class to post-process and plot the data into a pdf-file.'				

#----------Plot general----------------------

	def plot(self):	
		for column in range(2, self.n_columns):
			if self.subplot_order == 429:
				self.pdf_page_legend()						#Plot legend for ready pdf page.
				Plot_pdf.subplot_order = 421 				#Prepare next place to plot.
				Plot_pdf.fig = plt.figure(figsize=(8, 11))	#Prepare a new pdf page.
			for case in range(search.Search.n_cases):	
				x_array = np.array(self.data_column_grid_inp[case][0]) #Radius (m)		
				y_array = np.mean((np.reshape(self.data_columns_list[case][column], (self.time_radius_matrix_list[case][0], self.time_radius_matrix_list[case][1])).transpose()), axis=1)

				#Delete data points from head and tail as indicated in enter data.
				if int(self.n_delete_points[column-2][0])+int(self.n_delete_points[column-2][1]) < len(x_array) and int(self.n_delete_points[column-2][0])+int(self.n_delete_points[column-2][1]) < len(y_array):
					for delete_first in range(self.n_delete_points[column-2][0]):
						x_array = np.delete(x_array, 0)		#Delete head element from radius grid points.
						y_array = np.delete(y_array, 0)		#Delete head element.
					for delete_last in range(self.n_delete_points[column-2][1]):		
						x_array = np.delete(x_array, -1)	#Delete tail element from radius grid points.
						y_array = np.delete(y_array, -1)	#Delete tail element from y_array.
				#Exceptions.
				title = self.legend_list[column-2]+' '+ self.measured_quantity
				if self.filename == 'avgcden' and column == 4:	#If there is no data for impurities then separation data comes one column before than written in the entered data.
					if self.n_columns < 6:
						self.legend_list[column-2] = self.legend_list[3]
						title = self.measured_quantity+' '+self.legend_list[column-2]
				if column == 5:
					title = self.measured_quantity+' '+self.legend_list[column-2]
				ylabel = self.ylabel
				if self.filename == 'outera':
					ylabel = self.ylabel[column-2]
				#Plotting.
				ax = Plot_pdf.fig.add_subplot(Plot_pdf.subplot_order)	
				self.pdf_plot(x_array, y_array, self.line_types[case], 'Radius r (m)', ylabel, title, ax)
				Plot_pdf.legend_line_list[1].append(self.case_legends[case+2]+' '+self.case_legends[1])	
			Plot_pdf.subplot_order += 1

#----------Time plotting at specific radius general-------------

	def time_plot(self, outer):
		for column in range(2, self.n_columns):
			ylabel = self.ylabel
			if self.filename == 'outera':
				ylabel = self.ylabel[column-2]
			#Plot legends for full page and start new page.
			if Plot_pdf.page_full == 2:	
				self.pdf_page_legend_grid_spec(outer)
				Plot_pdf.fig = plt.figure(figsize=(8, 11))
				Plot_pdf.page_full = 0
			#Creates background subplot to make common labels.
			inner = gridspec.GridSpecFromSubplotSpec(1, 1, subplot_spec=outer[column-(column-Plot_pdf.page_full)], wspace=0.2, hspace=0.2)
			axCommon = plt.Subplot(Plot_pdf.fig, inner[0])								
			self.common_axes_time_plot(inner, axCommon, ylabel)
			Plot_pdf.fig.add_subplot(axCommon)

			#Creates subplots into gridspec:
			inner = gridspec.GridSpecFromSubplotSpec(search.Search.n_cases, 1, subplot_spec=outer[column-(column-Plot_pdf.page_full)], wspace=0.2, hspace=0.2)

			for case in range(search.Search.n_cases):		
				radius_input = float(self.at_radius) #Input radius.
				radius = min(self.data_column_grid_inp[case][0], key=lambda x:abs(x-radius_input)) #Find closes data point to the indicated radius.
				radius_index = self.data_column_grid_inp[case][0].index(radius)	#Gets the index of the radius.
				x_array = [i*self.time_step_list[case] for i in range(self.time_radius_matrix_list[case][0])]
				y_array = np.reshape(self.data_columns_list[case][column], (self.time_radius_matrix_list[case][0], self.time_radius_matrix_list[case][1])).transpose()

				ax = plt.Subplot(Plot_pdf.fig, inner[case])
				Plot_pdf.legend_line_list[0].append(ax.plot(x_array, y_array[radius_index], self.line_types[case]))
				Plot_pdf.legend_line_list[1].append(self.case_legends[case+2]+' '+self.case_legends[1])
				if case == 0: #Creates a common title.
					ax.set_title(self.legend_list[column-2]+' '+self.measured_quantity+' at r = '+str(radius)+' m')	
				Plot_pdf.fig.add_subplot(ax)

			Plot_pdf.page_full += 1	

#-----------Contourf plot general------------

	def plot_contourf(self, outer):
		for column in range(2, self.n_columns):
			ylabel = self.ylabel
			if self.filename == 'outera':
				ylabel = self.ylabel[column-2]
			#Plot legends for full page and start new page.
			if Plot_pdf.page_full == 2:
				Plot_pdf.pp.savefig()
				Plot_pdf.fig = plt.figure(figsize=(8, 11))
				Plot_pdf.page_full = 0

			#Finding highest contourf levels so that all contourfs can be plotted with same colorbar scale.	
			##############################################################################################################################		
			max_bound = -np.inf
  			min_bound = np.inf
			for case in range(search.Search.n_cases):
				z_array = list(np.reshape(self.data_columns_list[case][column], (self.time_radius_matrix_list[case][0], self.time_radius_matrix_list[case][1])).transpose())
				for delete_head in range(self.contourf_delete_points[column-2][0]):	#Modify range to choose how many data points to delete from radius indexes beginning.
					del z_array[0] 													#Delete first element from z_array.
				for delete_tail in range(self.contourf_delete_points[column-2][1]):	#Modify range to choose how many data points to delete from radius indexes end.
					del z_array[-1]													#Delete last element from y_array.
				
				max_lim = np.max(z_array)
				min_lim = np.min(z_array)
				if max_lim > max_bound:
					max_bound = max_lim
					max_levels = case
				if min_lim < min_bound:
					min_bound = min_lim
					min_levels = case
			plt.figure()	
			contour_max = plt.contourf([i*self.time_step_list[max_levels] for i in range(self.time_radius_matrix_list[max_levels][0])], np.array(self.data_column_grid_inp[max_levels][0]), np.reshape(self.data_columns_list[max_levels][column], (self.time_radius_matrix_list[max_levels][0], self.time_radius_matrix_list[max_levels][1])).transpose(), 20)
			levels = contour_max.levels 
			plt.close()
			#Checking if levels are correct.
			i = 0
			difference = levels[1]-levels[0]
			while levels[0] > min_bound:
				i+= 1
				levels = np.linspace(levels[0]-difference, levels[-1], 20+i)			
			while levels[-1] < max_bound:
				i += 1
				levels = np.linspace(levels[0], levels[-1]+difference, 20+i)
			#levels = None		#If one wants seperate colorbar for each contourf.
			##############################################################################################################################

			#Creates background subplot to make common labels.
			inner = gridspec.GridSpecFromSubplotSpec(1, 1, subplot_spec=outer[column-(column-Plot_pdf.page_full)], wspace=0.2, hspace=0.2)
			axCommon = plt.Subplot(Plot_pdf.fig, inner[0])								
			self.common_axes_contourf(inner, axCommon)
			Plot_pdf.fig.add_subplot(axCommon)
			#Creates subplots into gridspec.
			inner = gridspec.GridSpecFromSubplotSpec(search.Search.n_cases, 1, subplot_spec=outer[column-(column-Plot_pdf.page_full)], wspace=0.2, hspace=0.4)	
			#Prepare common title and xlabel.	
			title = ['']*search.Search.n_cases
			xlabel = ['']*search.Search.n_cases
			#Exception for title.
			if self.filename == 'avgcden' and column == 4:	#If there is no data for impuritys then separation data comes one column before than written in the entered data.
				if self.n_columns < 6:
					self.legend_list[column-2] = self.legend_list[3]	
			title[0] = self.legend_list[column-2]+' '+ self.measured_quantity		
			xlabel[-1] = 'Timestep'	
			#Plotting contourfs.
			for case in range(search.Search.n_cases):
				z_array = list(np.reshape(self.data_columns_list[case][column], (self.time_radius_matrix_list[case][0], self.time_radius_matrix_list[case][1])).transpose())
				x_array = [i*self.time_step_list[case] for i in range(self.time_radius_matrix_list[case][0])]
				y_array = np.array(self.data_column_grid_inp[case][0])
				for delete_head in range(self.contourf_delete_points[column-2][0]):	
					del z_array[0]													
					y_array = np.delete(y_array, 0)
				for delete_tail in range(self.contourf_delete_points[column-2][1]):
					del z_array[-1]													
					y_array = np.delete(y_array, -1)
				ax = plt.Subplot(Plot_pdf.fig, inner[case])
				contour = ax.contourf(x_array, y_array, z_array, 20, levels = levels)
				ax.set_title(title[case])								 
				ax.set_xlabel(xlabel[case])	
	
				cbar_obj = Plot_pdf.fig.add_subplot(ax)
				cbar = Plot_pdf.fig.colorbar(contour, ax=cbar_obj)
				cbar.ax.yaxis.get_offset_text().set_size(7)
				cbar.ax.tick_params(labelsize=8)
				cbar.ax.set_ylabel(self.case_legends[case+2]+' '+self.case_legends[1], rotation = 360, labelpad=36)
				cbar.ax.set_xlabel(ylabel, labelpad=7)
				cbar.ax.xaxis.set_label_position('top')
			Plot_pdf.page_full += 1			

#-----Non equidistant grid derivative--------

	def derivative_non_equi(self, f, case):
		deriv_data = []
		x = self.data_column_grid_inp[case][0]
		for i in range(len(f)-1):
			dx_i = x[i+1] - x[i]
			dx_ii = x[i] - x[i-1]
			deriv_data.append(-((-dx_i*f[i-1])/(dx_ii*(dx_i+dx_ii)) + ((dx_i-dx_ii)*f[i])/(dx_i*dx_ii) + (dx_ii*f[i+1])/(dx_i*(dx_i+dx_ii))))
		return deriv_data

#--------Prepare pdf subplots----------------

	def pdf_plot(self, data_x, data_y, line_type, xlabel, ylabel, title, ax):
		Plot_pdf.legend_line_list[0].append(ax.plot(data_x, data_y, line_type))	#Plot.
		ax.set_xlabel(xlabel)													#x-label.
		ax.set_ylabel(ylabel)													#y-label.
		ax.set_title(title)														#Title.
			
#--------Common axes time plot---------------

	def common_axes_time_plot(self, inner, axCommon, ylabel):	
		#Suppresses other visibility from the background subplot.
		axCommon.spines['top'].set_color('none') 
		axCommon.spines['bottom'].set_color('none')
		axCommon.spines['left'].set_color('none')
		axCommon.spines['right'].set_color('none')
		axCommon.set_axis_bgcolor('none')
		axCommon.tick_params(labelcolor='none', top='off', bottom='off', left='off', right='off')

		axCommon.set_ylabel(ylabel)		#Creates a common y-label.
		axCommon.set_xlabel('Timestep')	#Creates a common x-label.

		axCommon.yaxis.labelpad = 28	#Moves ylabel little bit to the left so it is not overlapping with ticklabels.

#--------Common axes contourf----------------

	def common_axes_contourf(self, inner, axCommon): 
		#Suppresses other visibility from the background subplot.
		axCommon.spines['top'].set_color('none')							
		axCommon.spines['bottom'].set_color('none')
		axCommon.spines['left'].set_color('none')
		axCommon.spines['right'].set_color('none')
		axCommon.set_axis_bgcolor('none')
		axCommon.tick_params(labelcolor='none', top='off', bottom='off', left='off', right='off')

		axCommon.set_ylabel('Radius r (m)')	#Creates a common y-label.

		axCommon.yaxis.labelpad = 28		#Moves ylabel little bit to the left so it is not overlapping with ticklabels.

#--------Pdf page legend---------------------

	def pdf_page_legend(self):
		if search.Search.n_cases < 5:
			top_adjust = 0.92
		else:
			top_adjust = 0.88
		plot_list = []
		legend_list_a = []
		for n in range(search.Search.n_cases):
			plot_list.append(Plot_pdf.legend_line_list[0][n][0],)
			legend_list_a.append(Plot_pdf.legend_line_list[1][n])	
		Plot_pdf.fig.tight_layout()
		Plot_pdf.fig.subplots_adjust(top = top_adjust)
		Plot_pdf.fig.legend(plot_list, legend_list_a, bbox_to_anchor=[0.5, 0.98], loc='upper center', ncol = 4)
		Plot_pdf.pp.savefig()

#--------Pdf page legend grid spec-----------

	def pdf_page_legend_grid_spec(self, outer):
			if search.Search.n_cases < 5:
				top_adjust = 0.92
			else:
				top_adjust = 0.90
			plot_list = []
			legend_list_a = []
			for n in range(search.Search.n_cases):
				plot_list.append(Plot_pdf.legend_line_list[0][n][0],)
				legend_list_a.append(Plot_pdf.legend_line_list[1][n])		
			outer.tight_layout(Plot_pdf.fig)
			outer.update(top = top_adjust, right = 0.88)
			Plot_pdf.fig.legend(plot_list, legend_list_a, bbox_to_anchor=[0.5, 0.98], loc='upper center', ncol = 4)		
			Plot_pdf.pp.savefig()


#------Parameters text file to pdf-----------

	def makeParametersPage(self):
		for case in range(search.Search.n_cases):
			Plot_pdf.fig = plt.figure(figsize=(8, 11))
			ax = plt.subplot(111)
			#ax.spines['top'].set_color('none')							
			#ax.spines['bottom'].set_color('none')
			#ax.spines['left'].set_color('none')
			#ax.spines['right'].set_color('none')
			ax.tick_params(labelcolor='none', top='off', bottom='off', left='off', right='off')
		
			plt.text(0.05, 0.95, self.absolute_paths[2][case].split('/')[-2], fontsize=20) 
			plt.text(0.05, 0.20, ''.join(self.lines_parameters[case]), fontsize=8)

			Plot_pdf.pp.savefig()

#-------Make cover page to pdf---------------

	def makeCoverPage(self):
		Plot_pdf.fig = plt.figure(figsize=(8, 11))
		ax = plt.subplot(111)
		ax.tick_params(labelcolor='none', top='off', bottom='off', left='off', right='off')
		caseDirNamesList = []
		for case in range(search.Search.n_cases):
			caseDirNamesList.append(self.absolute_paths[2][case].split('/')[-2])

		plt.text(0.05, 0.95, 'This pdf-file contains '+str(search.Search.n_cases)+' cases. \nThe cases were found in directories: '+(', '.join(caseDirNamesList))+'.' , fontsize=12) 

		Plot_pdf.pp.savefig()
		