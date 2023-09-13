import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('output.csv')

#XY PLOT
# Filter your data here if needed
#df = df[df['x_axis'] >= 5000]
#df = df[df['y_axis'] == 0]
df = df[df['z_axis'] == 0]
#df = df[df['concentration'] >= 1]

# Extract the data columns
x = df['x_axis'].values
y = df['y_axis'].values
conc = df['concentration'].values

plt.rcParams["figure.figsize"] = [16, 9]
plt.rcParams["figure.autolayout"] = True
fig, ax = plt.subplots()

# Create a grid of values for the filled contour plot
x_range = np.linspace(min(x), max(x), 100)
y_range = np.linspace(min(y), max(y), 100)
X, Y = np.meshgrid(x_range, y_range)

# Interpolate the concentration values to the grid using griddata
from scipy.interpolate import griddata
Z = griddata((x, y), conc, (X, Y), method='linear')

# Create the filled contour plot
contour = ax.contourf(X, Y, Z, cmap='seismic', levels=100, extend='both')  # Adjust the levels as needed

ax.set_xlabel("Direction Downwind from Stack, m")
ax.set_ylabel("Direction Crosswind from Stack, m")

fig.colorbar(contour, label="Concentration")
fig.savefig('output_contour_xy.png', dpi=480)
plt.show()

#XZ PLOT
df = pd.read_csv('output.csv')
# Filter your data here if needed
#df = df[df['x_axis'] >= 5000]
df = df[df['y_axis'] == 0]
#df = df[df['concentration'] >= 1]

# Extract the data columns
x = df['x_axis'].values
y = df['z_axis'].values
conc = df['concentration'].values

plt.rcParams["figure.figsize"] = [16, 9]
plt.rcParams["figure.autolayout"] = True
fig, ax = plt.subplots()

# Create a grid of values for the filled contour plot
x_range = np.linspace(min(x), max(x), 100)
y_range = np.linspace(min(y), max(y), 100)
X, Y = np.meshgrid(x_range, y_range)

# Interpolate the concentration values to the grid using griddata
from scipy.interpolate import griddata
Z = griddata((x, y), conc, (X, Y), method='linear')

# Create the filled contour plot
contour = ax.contourf(X, Y, Z, cmap='seismic', levels=100, extend='both')  # Adjust the levels as needed

ax.set_xlabel("Direction Downwind from Stack, m")
ax.set_ylabel("Direction Crosswind from Stack, m")

fig.colorbar(contour, label="Concentration")
fig.savefig('output_contour_xz.png', dpi=480)
plt.show()