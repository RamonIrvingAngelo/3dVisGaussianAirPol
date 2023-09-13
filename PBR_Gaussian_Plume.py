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
Q = 100. # g/s, Source emission rate
U = 6. # m/s, Average wind speed at stack height
H = 41. # m, Effective Stack Height plus plume rise

#Stability classes A, B, C, DD, DN, E, F
stability = "DD"

# How wide is the analysis for the plume?
y_max = 100. # m
y_min = -y_max # m
y = -y_max #for iteration purposes only

# How long is the analysis for the plume?
x_max = 3000. # m
x_min = 0.1 # m, default to non zero, minimum of 0.1m
x = 0.1 # this is for iteration purposes only

# How high is the analysis for the plume?
z_max = H + 5. # m
z = 0. # m, noting that this is ground level

res = 5. # m, resolution and iteration step
res_z = 5. # m, resolution and iteration step
conc_limiter = 1. #concentration limiter for faster rendering

#coefficients for sigmas
match stability:
    case "A":
        a1 = 0.0383
        b1 = 1.281
        a2 = 0.0002539
        b2 = 2.089
        a3 = 0.0002539
        b3 = 2.089
        c = 0.495
        d = 0.873
    case "B":
        a1 = 0.1393
        b1 = 0.9467
        a2 = 0.04936
        b2 = 1.114
        a3 = 0.04936
        b3 = 1.114
        c = 0.310
        d = 0.897
    case "C":
        a1 = 0.1120
        b1 = 0.9100
        a2 = 0.1014
        b2 = 0.926
        a3 = 0.1154
        b3 = 0.9109
        c = 0.197
        d = 0.908
    case "DD":
        a1 = 0.0856
        b1 = 0.8650
        a2 = 0.2591
        b2 = 0.6869
        a3 = 0.7368
        b3 = 0.5642
        c = 0.122
        d = 0.916
    case "DN":
        a1 = 0.0818
        b1 = 0.8155
        a2 = 0.2527
        b2 = 0.6341
        a3 = 1.297
        b3 = 0.4421
        c = 0.122
        d = 0.916
    case "E":
        a1 = 0.1094
        b1 = 0.7657
        a2 = 0.2452
        b2 = 0.6355
        a3 = 0.9204
        b3 = 0.4805
        c = 0.0934
        d = 0.912
    case "F":
        a1 = 0.05645
        b1 = 0.8050
        a2 = 0.1930
        b2 = 0.6072
        a3 = 1.505
        b3 = 0.3662
        c = 0.0625
        d = 0.911
    case _:
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
    
# Compute Total Number of Iterations
total_iterations = int((x_max - x_min) / res + 1) * int((y_max - y_min) / res + 1) * int((z_max / res_z + 1))
completed_iterations = 0

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
            
            completed_iterations += 1
            percentage_complete = (completed_iterations / total_iterations) * 100
            print(f"Percentage Completion: {percentage_complete:.5f}%")
            
            sigmaz = a * x ** b
            sigmay = c * x ** d
            
            eq_a = math.exp(- ((z + H)**2)/(2*sigmaz**2))
            eq_b = math.exp(- ((z - H)**2)/(2*sigmaz**2))
            eq_c = math.exp(- (y)**2/(2*sigmay**2))
            
            conc = 10000*(Q/(2*math.pi*U*sigmay*sigmaz))*(eq_c)*(eq_b + eq_a)    
            
            #writing to csv
            #if conc >= conc_limiter:
            xyz_conc = [x, y, z, conc]
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
print("Done")    