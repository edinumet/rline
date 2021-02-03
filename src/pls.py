import numpy as np
import matplotlib.pyplot as plt
# from matplotlib.mlab import griddata # deprecated since 2018
from scipy.interpolate import griddata
# https://www.reddit.com/r/Python/comments/87lbao/matplotlib_griddata_deprecation_help/
import matplotlib.gridspec as gridspec

def pls(gs, xx, yy, zz, hour, min, max, hourly_stab):
    """Plot Line Source"""
    # define grid
    xi = np.linspace(-100., 100., 100)
    yi = np.linspace(-100., 100., 100)
    X,Y= np.meshgrid(xi,yi)
    zi = griddata((xx, yy), zz, (X, Y), method='linear')

    # plot the roadways running N-S and E-W
    ax1 = plt.subplot(gs[:, :-1])
    ax1.plot([5, 5], [-100, 100], color='k', linestyle='--', linewidth=1)
    ax1.plot([-5, -5], [-100, 100], color='k', linestyle='--', linewidth=1)
    ax1.plot([-100, 100], [-5, -5], color='k', linestyle='--', linewidth=1)
    ax1.plot([-100, 100], [5, 5], color='k', linestyle='--', linewidth=1)
    ax1.set_ylabel('distance (m)', fontsize=11)
    ax1.set_xlabel('distance (m)', fontsize=11)
    circ1 = plt.Circle((20, 20), 1.5, color='red')
    ax1.add_artist(circ1)
    circ2 = plt.Circle((20, -20), 1.5, color='green')
    ax1.add_artist(circ2)
    circ3 = plt.Circle((-20, -20), 1.5, color='blue')
    ax1.add_artist(circ3)
    circ4 = plt.Circle((-20, 20), 1.5, color='black')
    ax1.add_artist(circ4)

    # Contours etc explained here: 
    # http://matplotlib.org/examples/pylab_examples/contourf_demo.html
    levels = np.arange(min, max, (max-min)/20)
    # contour the gridded data, plotting dots at the nonuniform data points.
    ax1.contour(xi, yi, zi, levels, linewidths=0.5, colors='w')
    CS1 = ax1.contourf(xi, yi, zi, levels, cmap=plt.cm.jet, vmax=abs(zi).max(), vmin=-abs(zi).max())
    #ax1.contour(xi, yi, zi, levels, linewidths=0.5, colors='w')
    #CS1 = ax1.contourf(xi, yi, zi, levels, cmap = plt.cm.jet, vmax=abs(zi).max(), vmin=-abs(zi).max())
    # Make a colorbar for the ContourSet returned by the contourf call.
    cbar = plt.colorbar(CS1)  # orientation = 'horizontal')
    cbar.ax.set_title('$\mu \ g m^{-3}$',fontsize=9)

    ax1.set_xlim(-100, 100)
    ax1.set_ylim(-100, 100)
    ax1.set_title('PM10 Ground-Level Concentration \n (%s)'%hourly_stab[hour-1], fontsize=11, color='blue')
    plt.show()