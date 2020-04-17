# -*- coding: utf-8 -*-
#**************************************************************************
# NAME OF THE PROJECT: analysis_class.py
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PURPOSE OF THIS MODULE :
#                          Private class to hold parameters for project 
#					      
#
# REQIREMENTS :            (Linux/Mac/Windows) Python 3.x 
#                               
# Developer: Sterling Reynolds , Undergraduate student 
# 		     Contact: icu327@my.utsa.edu
#            Department of Mechanical Engineering, UTSA Texas
#
# DATE:     March 2020 (SR)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import numpy as np 
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import sys
import math 
from numba import jit
import time
from Project_HT.Analysis_properties.air import * 
from Project_HT.Analysis_properties.table_7p6 import * 

class analysis():

		def __init__(self, init_prop,Kf,pf):

			self.__N         = init_prop[0]   # number of fins (Reynolds)
			self.__W 		 = init_prop[1]   # (m) width of base 
			self.__Rpp_chip  = init_prop[2]   # ((m^2K / W)) thermal contact resistance per unit area
			self.__Lb        = init_prop[3]   # (m) Height of base 
			self.__Kb        = init_prop[4]   # (W/m.K) Thermal conductivity base 
			self.__Vf        = init_prop[5]   # (m/s) Velocity over fins 
			self.__Tf_inf    = init_prop[6]   # (K)   T infinity over fins 
			self.__Vb        = init_prop[7]   # (m/s) Velocity at base 
			self.__Tb_inf    = init_prop[8]   # (K)   T infinity at base
			self.__Tc 	     = init_prop[9]   # (K) Temperature of chip 
			self.__Dp_max 	 = init_prop[10]  # (m) Max diameter of fin 
			self.__Dp        = 0              # init value 
			self.__Lp        = init_prop[11]  # (m) Unknown parameters 
			self.__Qc        = init_prop[12]  # (W) Unknown parameters 
			self.__Qb        = init_prop[13]  # (W) Unknown parameters 
			self.__Qf        = init_prop[14]  # (W) Unknown parameters 
			self.__hb        = init_prop[15]  # (W/m*2*K) Unknown parameters 

			self.__Kf        = Kf 			  # (W/m.K)  Thermal conductivity of fin
			self.__pf        = pf             # (Kg/m^3) Density 
			self.__results   = []			  # Empty list to hold results 
			self.last_res    = []		      # for 2d plot

		#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		# Purpose of function: run analysis within class 
		#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		def main(self):

			self.base_conv_heat_transfer_coeff()
			self.base_heat_rate()

			# Optimize parameters via gradient decent to find local minima
			Dp_range = np.arange((0.009/50) , self.__Dp_max, (5*10**-6) )
			Lp_range = np.arange((0.001 * 10**-3) , (2* 10**-3), (5*10**-5) )

			for i in range(len(Dp_range)):
				self.__Dp = Dp_range[i]
				for x in range(len(Lp_range)): 
					self.__Lp = Lp_range[x]

					self.fin_heat_rate()

					mass = ((self.__Lp * ((math.pi /4) * self.__Dp**2)) * self.__pf) * self.__N

					self.__results.append([(self.__Qc[0],self.__Dp * 10**3,self.__Lp * 10**3, mass)])
					if i == len(Dp_range)-1:
						self.last_res.append([(self.__Qc[0],self.__Dp * 10**3,self.__Lp * 10**3,mass)])
	

		#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		# Purpose: Compute convection heat transfer coefficent at the base
		#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		def base_conv_heat_transfer_coeff(self):
			# Base convection heat transfer coefficent at base 
			#  Assumptions: Steady state, isothermal, flat plate 
			#
			#		  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			#  0.005m |                                     |
			#         |                                     |
			#     -   *-------------------------------------*
			#													/ ______ Vb    = 10 (m/s)
			#													\
			#													/ ______ Tb_inf = 20 (C)
			#													\
			# Interpolate air tables for Density and Viscosity based on termperature 
			air_tablea_4 = air_a4()
			density_base   = np.interp([self.__Tb_inf], air_tablea_4[:,0], air_tablea_4[:,1])
			viscosity_base = np.interp([self.__Tb_inf], air_tablea_4[:,0], air_tablea_4[:,3])
			K_base         = np.interp([self.__Tb_inf], air_tablea_4[:,0], air_tablea_4[:,5])
			Prandtl_base   = np.interp([self.__Tb_inf], air_tablea_4[:,0], air_tablea_4[:,7])

			# Compute Reynolds number ****************************************
			# Re = (VpX / U)
			Re_base = (self.__Vb * density_base * self.__W) / (viscosity_base)
			if Re_base >= (5*10**5):
				print('\n\nTurbulent flow Qf is not programmed: you can program it if you want :) ')
				print('Breaking program: please reduce parameters to ensure laminar flow\n')
				print('Bye')
				sys.exit()
			
			# Compute Nusselt number ****************************************
			# Local_Nu_base = 0.332 * Re^(0.5) * Pr^(1/3)
			local_Nu_base = 0.332 * (Re_base**(1/2)) * (Prandtl_base**(1/3))
			
			# Compute convection heat transfer coefficent at base 
			# h = Nu * (k/x)
			self.__hb = local_Nu_base * (K_base / self.__W) 

			return()


		#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		# Purpose of function: Compute Qc of the chip
		#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		def base_heat_rate(self):
			# Thermal circuit of the base: 
			#
			#   Tb_inf           Tb              Tb1               Tc  / ______ Qpp
			#    *---\/\/\/\/\/---*---\/\/\/\/\/---*---\/\/\/\/\/---*  \
			#          RConv            RCond1             Cond 
			#          1/hb              Lb/K              Rpp
			#
			# Thus Qpp = (Tc - Tb_inf) / (Rconv + Rcond + Rcond)
			# 	   Converting to Qc 
			# 	   Qc = Ac(Tc - Tb_inf) / (Rconv + Rcond + Rcond)
			#			where Ac = W**2 

			Ac = self.__W**2

			RConv = (1/self.__hb) 
			RCond = (self.__Lb / self.__Kb)
			
			self.__Qb = (Ac * (self.__Tc - self.__Tb_inf) ) / ((self.__Rpp_chip) + (RCond) + (RConv))
			

		def fin_heat_rate(self):
				#***************************************************************************
				#					   	Insulated 
				#     _     _      _      _      _      _     _
				#          | |    | |    | |    | |    | |   | |	/ ______ Vf    = 10 (m/s)
				#          | |    | |    | |    | |    | |   | |  	\
				#    Lp    | |    | |    | |    | |    | |   | |	/ ______ Tf_inf = 20 (C)
				#          | |    | |    | |    | |    | |   | |	\
				#          | |    | |    | |    | |    | |   | |
				#     -   *-------------------------------------*  
				#				 Chip and board below
				#***************************************************************************
				# Computing Qf of the fin configuration 

				# Compute Reynolds Number for Flow 
				air_tablea_4    = air_a4()
				density_fin     = np.interp([self.__Tf_inf], air_tablea_4[:,0], air_tablea_4[:,1])
				Cp_fin          = np.interp([self.__Tf_inf], air_tablea_4[:,0], air_tablea_4[:,2])
				viscosity_fin   = np.interp([self.__Tf_inf], air_tablea_4[:,0], air_tablea_4[:,3])
				K_fin           = np.interp([self.__Tf_inf], air_tablea_4[:,0], air_tablea_4[:,5])
				Pr_fin_air      = np.interp([self.__Tf_inf], air_tablea_4[:,0], air_tablea_4[:,7])
				Pr_fin_s        = np.interp([self.__Tc]    , air_tablea_4[:,0], air_tablea_4[:,7])


				Lc = self.__Lp + (self.__Dp / 4 )
				Af = math.pi * self.__Dp * Lc 
				Ac = (math.pi * (self.__Dp ** 2)) / 4 
				Ab = (self.__W**2) - ((self.__N**2) * Ac)
				At = ((self.__N**2) * Af) + Ab



				# Compute St, SL, and max velocity ******************************
				St = (1/ (self.__N + 1)) * self.__W
				SL = St
				if St <= self.__Dp:
					print('This config is not logical, diameter is larger than St spacing')
					sys.exit()

				Vmax = (St / (St - self.__Dp)) * self.__Vf

				# Compute Reynolds number ****************************************
				# Re = (VpD / U)
				Re_fin_max = (Vmax * density_fin * self.__Dp) / (viscosity_fin)
				
				# Determine Constants of Equation 7.58 for the tube bank in cross flow (Table 7.5)
				# These if statments are not good although I would like to finish this project faster
				# Thus, don't look at them and you'll be happier :)
				if (Re_fin_max >= 10 and Re_fin_max < 100):
					C1 = 0.80 
					m = 0.40 
				elif (Re_fin_max >= 100 and Re_fin_max < 10**3):
					C1 = 0.51 
					m = 0.5 
				elif (Re_fin_max >= 10**3 and Re_fin_max < 2*10**5):
					C1 = 0.21
					m = 0.63 	
				elif (Re_fin_max >= 2*10**5 and Re_fin_max < 2*10**6):
					C1 = 0.021
					m = 0.84
				else:
					print('Your Reynolds number is pretty big')
					print('Please check your parameters')
					print('Breaking the program, bye')
					sys.exit()

				
				# Compute Nusselt number ****************************************
				if self.__N < 20:
					Correction_factor_C2_table = table_7p6_C2()
					C2   = np.interp([self.__N], Correction_factor_C2_table[0,:], Correction_factor_C2_table[1,:])
					Nu_bar_fin = C2 * C1 * (Re_fin_max**m) * (Pr_fin_air**0.36) * ((Pr_fin_air/Pr_fin_s)**0.25)
				else:
					Nu_bar_fin = C1 * (Re_fin_max**m) * (Pr_fin_air**0.36) * ((Pr_fin_air/Pr_fin_s)**0.25)

				# Compute average heat transfer coeff ****************************
				#h_bar_fin = Nu_bar_fin * (self.__Kf / self.__Dp)
				h_bar_fin = Nu_bar_fin * (K_fin / self.__Dp)

				# Compute parameters for n_o ***********************************
				# Lc = L + (D/4)
				# Af = 𝜋𝐷(𝐿c)
				# Ac = (𝜋𝐷^2) /4
				# Ab = (W^2) - (N^2 * Ac)
				# At = ( N^2 * Af) + Ab
				#
				# m   = sqrt((hbar*p / k*Ac))
				# nf  = tanh(m*Lc) / (m*Lc)
				# n_o = (1 - (N*Af / At))(1-nf)

				#m = math.sqrt( (h_bar_fin * self.__pf) / (self.__Kf * Ac) )
				m = math.sqrt( ( 4 * h_bar_fin) / (self.__Kf * self.__Dp) )


				
				# Check if ml is larger than 2.65 pg 163 in textbook
				if self.__Lp > (2.65 / m):
					print('Max length is reached, returning to main')
					return()

				nf = math.tanh(m * self.__Lp) /( m * self.__Lp)
				ex = ((self.__N**2 * Af)/(At))*(1 - nf)
				n_o = (1 - ex)

				res = (n_o * h_bar_fin * At)**-1

				self.__Qf = (self.__Tc - self.__Tf_inf) / res
				self.__Qc = self.__Qf + self.__Qb
				return()

				

		@property
		def N(self):  
			return(self.__N)
		@property       
		def W(self):  		
			return(self.__W)
		@property	 
		def Rpp_chip(self): 
			return(self.__Rpp_chip)
		@property
		def Lb(self):       
			return(self.__Lb)
		@property
		def Kb(self):     
			return(self.__Kb)
		@property
		def Vf(self):      
			return(self.__Vf)
		@property
		def Tf_inf(self):   
			return(self.__Tf_inf)
		@property
		def Vb(self):       
			return(self.__Vb)
		@property
		def Tb_inf(self):   
			return(self.__Tb_inf)
		@property
		def Tc(self):  	   
			return(self.__Tc)
		@property
		def Dp_max(self):  	   
			return(self.__Dp_max)
		@property
		def Dp(self):  	   
			return(self.__Dp)
		@property
		def Lp(self):       
			return(self.__Lp)
		@property
		def Qc(self):       
			return(self.__Qc)
		@property
		def Qb(self):       
			return(self.__Qb)
		@property
		def Qf(self):       
			return(self.__Qf)
		@property
		def hb(self):       
			return(self.__hb)
		@property
		def Kf(self):       
			return(self.__Kf)
		@property
		def pf(self):       
			return(self.__pf)
		@property
		def results(self):
			return(self.__results)



		@N.setter
		def N(self,N):  
			self.__N = N 
		@W.setter       
		def W(self,W):  		
			self.__W = W
		@Rpp_chip.setter
		def Rpp_chip(self,Rpp_chip): 
			self.__Rpp_chip = Rpp_chip
		@Lb.setter
		def Lb(self,Lb):       
			self.__Lb
		@Kb.setter
		def Kb(self,Kb):     
			self.__Kb = Kb 
		@Vf.setter
		def Vf(self,Vf):      
			self.__Vf = Vf
		@Tf_inf .setter
		def Tf_inf(self,Tf_inf):   
			self.__Tf_inf = Tf_inf
		@Vb.setter
		def Vb(self,Vb):       
			self.__Vb = Vb 
		@Tb_inf.setter
		def Tb_inf(self,Tb_inf):   
			self.__Tb_inf = Tb_inf
		@Tc.setter
		def Tc(self,Tc):  	   
			self.__Tc = Tc 
		@Dp_max.setter
		def Dp(self,Dp_max):  	   
			self.__Dp_max = Dp_max
		@Dp.setter
		def Dp(self, Dp):  	   
			self.Dp = Dp
		@Lp.setter
		def Lp(self,Lp):       
			self.__Lp = Lp 
		@Qc.setter
		def Qc(self,Qc):       
			self.__Qc = Qc 
		@Qb.setter
		def Qb(self,Qb):       
			self.__Qb = Qb 
		@Qf.setter
		def Qf(self,Qf):       
			self.__Qf = Qf 
		@hb.setter
		def hb(self,hb):       
			self.__hb = hb 
		@Kf.setter
		def Kf(self,Kf):       
			self.__Kf = Kf 
		@pf.setter
		def Kf(self,pf):       
			self.__pf = pf 
		@results.setter
		def results(self,results):
			self.__results = results
