#*******************************************************************************
# NAME OF THE PROJECT:  input.py
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PURPOSE OF THIS MODULE :
#                          Input file for heat transfer project
#					       : Initialize analysis properties 
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

def init_properties():
	#***************************************************************************
	#						  Insulated
	#     _     _      _      _      _      _     _
	#          | |    | |    | |    | |    | |   | |	/ ______ Vf    = 10 (m/s)
	#          | |    | |    | |    | |    | |   | |  	\
	#    Lp    | |    | |    | |    | |    | |   | |	/ ______ Tf_inf = 20 (C)
	#          | |    | |    | |    | |    | |   | |	\
	#          | |    | |    | |    | |    | |   | |
	#     -   *-------------------------------------*  
	#         |/////////////////////////////////////|	R_pp = 10^-4 (m^2K / W) & Tc 
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
	# Start: Define parameters for analysis 
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	# Geometry
	N        = 22     # number of fins (Reynolds)
	W 		 = 0.0127  # (m) width of base 
	Rpp_chip = 10**-4  # ((m^2K / W)) thermal contact resistance per unit area
	Lb       = 0.005   # (m) Height of base 
	Kb       = 1       # (W/m.K) Thermal conductivity

	# Velocity and temperature of convection cooling
	Vf      = 10               # (m/s) Velocity over fins 
	Tf_inf  = 20 + 273.15      # (K)   T infinity over fins 
	Vb      = 10               # (m/s) Velocity at base 
	Tb_inf  = 20 + 273.15      # (K)   T infinity at base


	# Temperature of chip 
	Tc = 75 + 273.15           # (K)  


	# Varied parameters 
	# Dp = Pin diameter 
	# Lp = Length of pin
	#
	# Number of pins multiplied by the diameter of the pins cannot exceed 9 mm
	# Thus: (N)Dp = 9mm 
	Dp_max = (0.009) / (N)  # (m Max)
	Lp = None 			# (m) Unknown parameters 
	Qc = None 			# (W) Unknown parameters 
	Qb = None           # (W) Unknown parameters 
	Qf = None 			# (W) Unknown parameters 
	hb = None 			# (W/m*2*K) Unknown parameters 

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	# End: Define parameters for analysis 
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
	init_prop = np.array((N, W, Rpp_chip, Lb, Kb, Vf, Tf_inf, Vb, Tb_inf, Tc, Dp_max, Lp, Qc, Qb, Qf, hb ))

    # return initialized analysis properties main function
	return(init_prop)
