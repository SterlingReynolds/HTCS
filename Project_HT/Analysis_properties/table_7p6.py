#*******************************************************************************
# NAME OF THE PROJECT:  table_7p6.py
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PURPOSE OF THIS MODULE :
#                          
#					       Hold table 7.6
#
# REQIREMENTS :            (Linux/Mac/Windows) Python 3.x
#
# Developer: Sterling Reynolds , Undergraduate student
# 		     Contact: icu327@my.utsa.edu
#            Department of Mechanical Engineering, UTSA Texas
#
# DATE:     March 2020 (SR)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import numpy as np

def table_7p6_C2():
	#***************************************************************************
	#	 Table 7.6 from "Fundamentals of Heat and Mass Transfer 8th ED"
	#    			( Photo of table provided in same directory :) )
	#***************************************************************************
	Correction_factor_C2 = np.array([ [1, 2, 3, 4, 5, 7, 10, 13, 16],
									  [0.70, 0.80, 0.86, 0.90, 0.92, 0.95, 0.97, 0.98, 0.99] ])

	# return initialized analysis properties main function
	return(Correction_factor_C2)
