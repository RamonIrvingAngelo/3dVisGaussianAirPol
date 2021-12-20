# -*- coding: utf-8 -*-
"""
Created on Mon Dec 20 18:40:03 2021

@author: rddejesus
"""

import pandas as pd
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D

df = pd.read_csv('output.csv')
#df = df[df['concentration'] >= 1]
x = list(df['x_axis'])
y = list(df['y_axis'])
z = list(df['z_axis'])
conc = list(df['concentration'])

#color settings
#c_white = clrs.colorConverter.to_rgba('white',alpha = 0)
#c_black= clrs.colorConverter.to_rgba('black',alpha = 1)
#cmap_rb = clrs.LinearSegmentedColormap.from_list('rb_cmap',[c_white,c_black],512)

plt.rcParams["figure.figsize"] = [7.00, 3.50]
plt.rcParams["figure.autolayout"] = True
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
img = ax.scatter(x, y, z, c=conc, cmap= 'YlOrRd' , s = 50, edgecolors = None, alpha = 0.5)

# Plot settings:
ax.set_xlim3d(0,max(x))
ax.set_ylim3d(min(y),max(y))
ax.set_zlim3d(0,max(z))
ax.set_xlabel("Direction Downwind from Stack, m")
ax.set_ylabel("Direction Crosswind from Stack, m")
ax.set_zlabel("Height of Plume, m")
#ax.invert_xaxis()
fig.colorbar(img)
plt.show()