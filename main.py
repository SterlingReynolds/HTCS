#*******************************************************************************
# NAME OF THE PROJECT:  main.py
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PURPOSE OF THIS MODULE :
#                          Main input script to execute the heat transfer
#					       project.
#
# REQIREMENTS :            (Linux/Mac/Windows) Python 3.x
#
# Developer: Sterling Reynolds , Undergraduate student
# 		     Contact: icu327@my.utsa.edu
#            Department of Mechanical Engineering, UTSA Texas
#
# License:  MIT 
#			If you're using this for academic work, a donation of coffee to the 
#			developer would be much appreciated. 
# DATE:     March 2020 (SR)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Process
import pandas as pd 
from Project_HT.analysis_class import *
from Project_HT.input  import * 

def main():
	#***************************************************************************
	#						  Insulated
	#     _     _      _      _      _      _     _
	#          | |    | |    | |    | |    | |   | |	/ ______ Vf    = 10 (m/s)
	#          | |    | |    | |    | |    | |   | |  	\
	#    Lp    | |    | |    | |    | |    | |   | |	/ ______ Tf_inf = 20 (C)
	#          | |    | |    | |    | |    | |   | |	\
	#          | |    | |    | |    | |    | |   | |
	#     -   *-------------------------------------*  
	#         |/////////////////////////////////////|	R_pp = 10^-4 (m^2K / W)
	#     -   *-------------------------------------*
	#         |                                     |
	#  0.005m |                                     |
	#         |                                     |
	#     -   *-------------------------------------*
	#													/ ______ Vb    = 10 (m/s)
	#													\
	#													/ ______ Tb_inf = 20 (C)
	#													\
	#							12.7mm
	#		  |~~~~~~~~~~~~~~~~~ W ~~~~~~~~~~~~~~~~~|
	#***************************************************************************

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	# Start: Retrieve properties from input file 
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	init_prop = init_properties()
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	# Start:  Retrieve properties from input file 
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	# Brass ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	thermal_conductivity  = 64  # W/(m*k)
	density               = 8400  # (Kg/m^3)
	Brass_analysis= analysis(init_prop,thermal_conductivity,density)
	# Brass ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	# Copper ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	thermal_conductivity  = 413  # W/(m*k)
	density               = 8940 # (Kg/m^3)
	CU_analysis= analysis(init_prop,thermal_conductivity,density)
	# Copper ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	# Bronze ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	thermal_conductivity  = 15  # W/(m*k)
	density               = 7700  # (Kg/m^3)
	Bronze_analysis= analysis(init_prop,thermal_conductivity,density)
	# Bronze ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


	# Start analysis ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	p_Brass = Process(target=Brass_analysis.main()  , args=())
	p_CU = Process(target=CU_analysis.main()  , args=())
	p_Bronze = Process(target= Bronze_analysis.main(), args=())
	p_Brass.start()
	p_CU.start()
	p_Bronze.start()
	p_Brass.join()
	p_CU.join()
	p_Bronze .join()
	# End of analysis ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	
	# Get data from objects
	results_Brass  =  np.concatenate(Brass_analysis.results   )
	results_CU     =  np.concatenate(CU_analysis.results   )
	results_Bronze =  np.concatenate(Bronze_analysis.results)
	
	fig    = plt.figure(1)
	ax1     = fig.add_subplot(111, projection='3d')
	#surf   = ax1.plot_trisurf(results_Brass[:,1], results_Brass[:,2], results_Brass[:,0], cmap=cm.terrain, linewidth=0, alpha=0.55 )
	#surf11 = ax1.plot_trisurf(results_CU[:,1], results_CU[:,2], results_CU[:,0], cmap=cm.jet, linewidth=0, alpha=.55            )
	#surf1  = ax1.plot_trisurf(results_Bronze[:,1], results_Bronze[:,2], results_Bronze[:,0], cmap=cm.brg, linewidth=0, alpha=0.55)
	#cbar = fig.colorbar(surf11)
	#cbar.set_label('Qc (W)',labelpad=30, rotation=270)

	surf   = ax1.plot_trisurf(results_Brass[:,1], results_Brass[:,2]  ,  results_Brass[:,3] * 10**3, cmap=cm.terrain, linewidth=0, alpha=1 )
	surf11 = ax1.plot_trisurf(results_CU[:,1], results_CU[:,2]        ,     results_CU[:,3] * 10**3, cmap=cm.jet, linewidth=0, alpha=.55            )
	surf1  = ax1.plot_trisurf(results_Bronze[:,1], results_Bronze[:,2], results_Bronze[:,3] * 10**3, cmap=cm.brg, linewidth=0, alpha=0.55)
	cbar = fig.colorbar(surf11)
	cbar.set_label('Mass (Grams)',labelpad=30, rotation=270)

	plt.xlabel('Lp (mm)')
	plt.ylabel('Dp (mm)')

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	two_d_results_Brass  =  np.concatenate( Brass_analysis.last_res   )
	two_d_results_CU     =  np.concatenate(    CU_analysis.last_res   )
	two_d_results_Bronze =  np.concatenate(Bronze_analysis.last_res   )

	fig1 = plt.figure(3)
	plt.plot(two_d_results_Brass[:,2], two_d_results_Brass[:,0]  ,label='Brass' )
	plt.plot(two_d_results_CU[:,2], two_d_results_CU[:,0]        ,label='Copper')
	plt.plot(two_d_results_Bronze[:,2], two_d_results_Bronze[:,0],label='Bronze')
	plt.legend()
	plt.xlabel('Lp (mm)')
	plt.ylabel('Qc (W)')
	title = 'Maximum diameter for N = ' + str(init_prop[0])
	plt.title(title)
	plt.show()



	df_results_Brass  = pd.DataFrame(results_Brass )
	df_results_CU     = pd.DataFrame(results_CU    )
	df_results_Bronze = pd.DataFrame(results_Bronze)
	df_results_Brass.to_excel('Excel/Brass.xlsx')
	df_results_CU.to_excel('Excel/Copper.xlsx')
	df_results_Bronze.to_excel('Excel/Bronze.xlsx')


if __name__ == "__main__":
	main()


