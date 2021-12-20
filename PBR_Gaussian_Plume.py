# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 15:37:12 2021

@author: rddejesus
"""
import math
from csv import writer
import os

#removes output.csv file and/or output.xlsx file
if os.path.exists('output.csv'):
    os.remove('output.csv')

#variables
Q = 94.5 # g/s, Source emission rate
U = 2.78 # m/s, Average wind speed at stack height
H = 58.8 # m, Effective Stack Height plus plume rise

# How wide is the analysis for the plume?
y_max = 200. # m
y_min = -y_max # m
y = -y_max #for iteration purposes only

# How long is the analysis for the plume?
x_max = 3000. # m
x_min = 0.1 # m, default to non zero, minimum of 0.1m
x = 0.1 # this is for iteration purposes only

# How high is the analysis for the plume?
z_max = 70. # m
z = 0. # m, noting that this is ground level

res = 5. # m, resolution and iteration step
res_z = 5. # m, resolution and iteration step
conc_limiter = 1. #concentration limiter for faster rendering

#coefficients for sigmas
a1 = 0.0856
b1 = 0.8650
a2 = 0.2591
b2 = 0.6869
a3 = 0.7368
b3 = 0.5642
c = 0.122
d = 0.916

#writing header to output
header_list = ['x_axis', 'y_axis', 'z_axis', 'concentration']
with open('output.csv', 'a', newline='') as f_object:
    writer_object = writer(f_object)
    writer_object.writerow(header_list)
    f_object.close()

#percent completion divisor
x_percent = (x_max - x_min)/res
y_percent = (y_max - y_min)/res
z_percent = z_max
div_per = x_percent * y_percent * z_percent

#GET READY FOR LOOPING HERE
while z <= z_max:
    while y <= y_max:
        while x <= x_max:
            if x == 5.1:
                x = 5.0
                
            if x > 5000:
                a = a3
                b = b3
            elif x > 500 and x <= 5000:
                a = a2
                b = b2
            else:
                a = a1
                b = b1
                    
            sigmaz = a * x ** b
            sigmay = c * x ** d
            
            eq_a = math.exp(- ((z + H)**2)/(2*sigmaz**2))
            eq_b = math.exp(- ((z - H)**2)/(2*sigmaz**2))
            eq_c = math.exp(- (y)**2/(2*sigmay**2))
            
            conc = 10000*(Q/(2*math.pi*U*sigmay*sigmaz))*(eq_c)*(eq_b + eq_a)    
            
            #writing to csv
            if conc >= conc_limiter:
                percent_completion = abs(x * y * z)/div_per *100
                xyz_conc = [x, y, z, conc]
                print(x,' ',y,' ',z,' ',conc,' ',percent_completion,'%')
                with open('output.csv', 'a', newline='') as f_object:
                    writer_object = writer(f_object)
                    writer_object.writerow(xyz_conc)
                    f_object.close()
            x += res
        x = x_min
        y += res
    x = x_min
    y = -y_max
    z += res_z
    