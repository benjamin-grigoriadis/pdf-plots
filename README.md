# pdf-plots
A Python script for post-processing simulation data and plotting the results to a single pdf-file for easy result survey. 

This Python script processes data from several simulations and plots them together in a format where comparing the results is convinient. The current post-processing of the data is designed for a specific simulation of turbulent plasma. 

The script consists of four parts:

1. search.py file consists of Search class that searches the directories of the simulation files. 
2. save_data.py consists of Data class that saves all the data to lists.
3. plot.py file consists of a Plot_pdf class that deals with all the necessary post-processing and arranging of the data, creating of figures and creating the pdf-file.
4. makePyplot.py is used for running the script. main() creates objects that have the necessary information of the simulations, and then utilizes the functions in Search, Data and Plot_pdf classes to create the pdf-file.
