import matplotlib 
matplotlib.rc('xtick', labelsize=8) 
matplotlib.rc('ytick', labelsize=8) 
matplotlib.rc('axes', titlesize=10, labelsize=8)
matplotlib.rc('legend', fontsize=10)
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
import search
import save_data
import plot
import matplotlib.gridspec as gridspec
from matplotlib.backends.backend_pdf import PdfPages

all_data = np.empty((7,0)).tolist()
settings = np.empty((5,0)).tolist()

#_______________________________________________________________________________DATA SPECIFIC INFORMATION BELOW______________________________________________________________________________________________________

#all_data[example] = ('filename', 'measured quantity', '3rd column', '4th column', '5th column', '6th column', 'ylabel', 'Numbers: To remove data points from head or tail. On default everything is zero.')
all_data[0] = ('outkhi', 	'heat transport coeff',	'Electron', 	'Ion', 	'Impurity', 	'',			'$\chi$ (m$^2$/s)', 	'100', [[2, 8], [2, 8], [2, 8]], '2D:', [[0, 0], [0, 1], [0, 1]]) 
all_data[1] = ('outpfl', 	'charge flux',			'Electron', 	'Ion', 	'Impurity', 	'',			'$\Gamma$ (A/m$^2$)', 	'100', [[0, 0], [0, 0], [0, 0]], '2D:', [[5, 0], [0, 5], [1, 0]])
all_data[2] = ('outqfl', 	'heat flux',			'Electron', 	'Ion', 	'Impurity', 	'',			'Q (J/m$^2$s)', 		'100', [[0, 0], [0, 0], [0, 0]], '2D:', [[0, 0], [0, 3], [0, 0]]) 
all_data[3] = ('avgckine', 	'temperature',			'Electron', 	'Ion', 	'Impurity', 	'',			'T (eV)',		 		'0', [[0, 0], [0, 0], [0, 0]], '2D:', [[3, 0], [0, 3], [3, 0]]) 
all_data[4] = ('avgcden', 	'Density', 				'Electron', 	'Ion', 	'Impurity', 'separation', 	'n (m$^{-3}$)',	 		'0', [[0, 0], [0, 0], [10, 25], [0, 0]],'2D',[[0, 0], [4, 0], [0, 0], [0, 0]]) 
all_data[5] = ('avgcpot', 	'Potential',			'', '', '', '',										'$\phi$ (V)',			'100', [[0, 0], [0, 0], [0, 0]], '2D:', [[0, 0], [0, 0], [0, 0]]) 
all_data[6] = ('outera', '','Neoclassical radial electric field', 'Mach number', 'Collisionality', '', ['E$_\mathrm{r}$ (V/m)', '', '$\\nu$ *'], '0', [[3, 8], [0, 0], [2, 0]], '2D:', [[15, 15], [0, 0], [3, 0]])
settings[0] = ('<no file for electric field>', '', 'Total electric field', 'Total electric field grad', '', '', ['E$_\mathrm{r}$ (V/m)', 'dE$_\mathrm{r}$/dr (V/m$^2$)'], '<same as for avgcpot>', [[0, 6], [10, 25], [0, 6], [0, 10]]) 

#_____________________________________________________________LEGEND NAMES, LINETYPES, RADIUS FOR TIME PLOT AND PDF-FILENAME BELOW___________________________________________________________________________________

settings[1] = ('<case_temperatures>', 'eV', 'T = 228', 'T = 285', 'T = 342', 'T = 399', 'T = 200', 'T = 220', 'T = 240', '8', '9', '10', '', '', '')	#'<case temperature>','eV', 'temp case1', 'temp case2...'
settings[2] = ('c-', 'b-.', 'r--', 'g--', 'c-s', 'b-^', 'r-d', 'g->' ,'c-<', '-x', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-')		#Line types for different cases.
settings[3] = ('2.75E-02')				#Radius (m) to plot for time dependent plots.
settings[4] = ('pdf_name.pdf')			#Name of pdf-file.


class Make_plot(plot.Plot_pdf, save_data.Data, search.Search):
	'This class inherits class attributes from Plot_pdf, Data and Search classes. main() creates Make_plot objects that have information given in Enter data section. main() then uses Plot_pdf, Data and Search classes to plot the data to a pdf file.'
	def __init__(self, plottingDetails, settings): 
		self.filename = plottingDetails[0]
		self.measured_quantity = plottingDetails[1]
		self.legend_list = [plottingDetails[2], plottingDetails[3], plottingDetails[4], plottingDetails[5]]
		self.ylabel = plottingDetails[6]
		self.cut_from_beginning = plottingDetails[7]
		self.n_delete_points = plottingDetails[8]
		self.contourf_delete_points = plottingDetails[10]
		self.electric_field_settings = settings[0]
		self.case_legends = settings[1]
		self.line_types = settings[2]
		self.at_radius = settings[3]
		self.data_columns_list = [] 
		self.data_column_grid_inp = [] 
		self.lines_parameters = []
		self.time_step_list = [] 
def main():
	#Makes Plot_pdf class objects:
	allData = [Make_plot(data, settings) for data in all_data]
	#Setting up the data:
	plot.Plot_pdf.pp = PdfPages(settings[4])
	for setUpData in allData:						
		setUpData.abs_path()
		setUpData.lines()
	plot.Plot_pdf.legend_line_list = np.empty((2, 0)).tolist() 
	plot.Plot_pdf.neoclassical_data = allData[6]
	print('Creating pdf...')
	
	#Creates a cover page for the pdf-file.
	#allData[0].makeCoverPage()


	###################################	TIME AVERAGED PLOTS	#################################################
	plot.Plot_pdf.fig = plt.figure(figsize=(8, 11))
	plot.Plot_pdf.subplot_order = 421
		
	for plotting in allData:
		plotting.plot()				
	#allData[5].plot_electric_field()		
	#allData[5].plot_gradient()
	#allData[5].plot_neoclassical()

	makeLegend = plot.Plot_pdf(all_data[0]) 	
	makeLegend.pdf_page_legend()
	#################################################################################################################
	#Comment out this whole block above to not plot any time averaged plots.


	############################################	TIME PLOTS	#################################################
	plot.Plot_pdf.fig = plt.figure(figsize=(8, 11))
	plot.Plot_pdf.page_full = 0
	outer = gridspec.GridSpec(2, 1, wspace=0.25, hspace=0.2)
	
#	allData[0].time_plot(outer)	
	allData[1].time_plot(outer)	
	allData[2].time_plot(outer)
#	allData[3].time_plot(outer)
#	allData[4].time_plot(outer)
#	allData[6].time_plot(outer)
#	allData[5].time_plot_electric_field(outer)
#	allData[5].time_plot_gradient(outer)

	makeLegend = plot.Plot_pdf(all_data[0]) 
	makeLegend.pdf_page_legend_grid_spec(outer)
	#################################################################################################################
	#Comment out this whole block above to not plot any time plots.


	############################################	CONTOURF PLOTS	#################################################
	plot.Plot_pdf.fig = plt.figure(figsize=(8, 11))
	plot.Plot_pdf.page_full = 0
	outer = gridspec.GridSpec(2, 1, wspace=0.25, hspace=0.2)
		
#	allData[0].plot_contourf(outer)	
	allData[1].plot_contourf(outer)	
	allData[2].plot_contourf(outer)
	allData[3].plot_contourf(outer)
	allData[4].plot_contourf(outer)
	allData[6].plot_contourf(outer)
#	allData[5].plot_contourf_derivative(outer)
#	allData[5].plot_contourf_gradient(outer)

	plot.Plot_pdf.pp.savefig()
	#################################################################################################################
	#Comment out this whole block above to not plot any contourf plots.


	#Creates text pages from parameters text files of the cases.
	allData[0].makeParametersPage()

	plot.Plot_pdf.pp.close()
	print('Pdf-file done.')
	plt.show()
main()




