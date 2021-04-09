"""
Created: Tuesday 1st December 2020
@author: John Moncrieff (j.moncrieff@ed.ac.uk)
Last Modified on 5 Feb 2021 16:30 

DESCRIPTION
===========

Plots RLINE output and weather data
"""


import numpy as np
import math
import matplotlib.pyplot as plt
# from matplotlib.mlab import griddata # deprecated since 2018
from scipy.interpolate import griddata
# https://www.reddit.com/r/Python/comments/87lbao/matplotlib_griddata_deprecation_help/
import matplotlib.gridspec as gridspec
import os
from datetime import datetime


def pls(gs, xx, yy, zz, hour, min, max, datam, sitesp, sitesn, hourly_stab):
    """Plot Line Source"""
    # define grid
    xi = np.linspace(-100., 100., 100)
    yi = np.linspace(-100., 100., 100)
    X,Y= np.meshgrid(xi,yi)
    zi = griddata((xx, yy), zz, (X, Y), method='linear')
    # plot the roadways running N-S and E-W
    fig, ax = plt.subplots(figsize=(10,8),ncols=1,nrows=1)#    2,
    #                       gridspec_kw={'height_ratios':[8,1],'hspace':0.3})
    #ax = axs[0]
    # Use indexing method for subplots
    ax.plot([5, 5], [-100, 100], color='k', linestyle='--', linewidth=1)
    ax.plot([-5, -5], [-100, 100], color='k', linestyle='--', linewidth=1)
    ax.plot([-100, 100], [-5, -5], color='k', linestyle='--', linewidth=1)
    ax.plot([-100, 100], [5, 5], color='k', linestyle='--', linewidth=1)
    ax.set_ylabel('distance (m)', fontsize=11)
    ax.set_xlabel('distance (m)', fontsize=11)
    circ1 = plt.Circle((20, 20), 1.5, color='red')
    ax.add_artist(circ1)
    circ2 = plt.Circle((20, -20), 1.5, color='green')
    ax.add_artist(circ2)
    circ3 = plt.Circle((-20, -20), 1.5, color='blue')
    ax.add_artist(circ3)
    circ4 = plt.Circle((-20, 20), 1.5, color='black')
    ax.add_artist(circ4)

    # Contours etc explained here: 
    # http://matplotlib.org/examples/pylab_examples/contourf_demo.html
    levels = np.arange(min, max, (max-min)/20)
    # contour the gridded data, plotting dots at the nonuniform data points.
    ax.contour(xi, yi, zi, levels, linewidths=0.5, colors='w')
    CS1 = ax.contourf(xi, yi, zi, levels, cmap=plt.cm.jet, vmax=abs(zi).max(), vmin=-abs(zi).max())
    #ax1.contour(xi, yi, zi, levels, linewidths=0.5, colors='w')
    #CS1 = ax1.contourf(xi, yi, zi, levels, cmap = plt.cm.jet, vmax=abs(zi).max(), vmin=-abs(zi).max())
    # Make a colorbar for the ContourSet returned by the contourf call.
    cbar = plt.colorbar(CS1)  # orientation = 'horizontal')
    cbar.ax.set_title('$\mu \ g m^{-3}$',fontsize=9)

    ax.set_xlim(-100, 100)
    ax.set_ylim(-100, 100)

    ax.set_title('PM10 Ground-Level Concentration '+ '\n'
        + hourly_stab + '\n' + 'wind direction = '+str(int(float(datam['dir']))) +
         '$ ^o$,  ' + 'windspeed = '+ str(float(datam['u'])) + ' m $s^{-1}$', fontsize=14, color='blue')

    #  Create a Table of data below Figure
    # https://stackoverflow.com/questions/43744354/matplotlib-create-table-data-for-one-row-multiple-columns
    #fig.subplots_adjust(bottom=0.1)  # make room for the table
    # rows = ['PM10', 'NOx']
#     columns = ['Site 1', 'Site 2', 'Site 3', 'Site 4']
#     t_data = np.array([[sitesp[0],sitesp[1],sitesp[2],sitesp[3]],
#                        [sitesn[0],sitesn[1],sitesn[2],sitesn[3]]])
#     ax=axs[1]
#     ax.set_frame_on(False) # turn off frame for the table subplot
#     ax.set_xticks([]) # turn off x ticks for the table subplot
#     ax.set_yticks([]) # turn off y ticks for the table subplot
#     ax.table(cellText=t_data,
#                  rowLabels=rows,
#                  colLabels=columns,
#                  loc='top',
#                  colWidths=[0.25 for x in columns])
    #table.scale(2, 2)
    # Adjust layout to make room for the table:
    #plt.subplots_adjust(left=0.1, bottom=0.8)
    # output results 
    now = datetime.now()    # datetime object containing current date and time
    # print("now =", now)
    dt_string = now.strftime("%Y%m%d_%H%M%S")  # YY/mm/dd_H:M:S
    # print("date and time =", dt_string)   
    outfile=hourly_stab+'_'+dt_string
    #fig.tight_layout()
    path = './results'
    plt.savefig(os.path.join(path,outfile))
    plt.show()
    
    
    # To be completed
    # """Plot meteorological data"""
#     hour = int(datam['Hour'])
#     u = float(datam['u'])
#     wdir = int(float(datam['dir']))
#     MOLength = int(float(datam['L']))
#     H = int(float(datam['Hs']))
#     sbl = int(float(datam['SBL']))
#     # print u,wdir,MOLength,H,sbl
#     # convert wdir to radians
#     wdirr = wdir * math.pi /180
#     # Compute pie slices
#     # from MatplotlIb web page of examples
#     theta = wdirr
#     radii = 8
#     nwidth = np.pi / 16
    # go clockwise as in a compass
    #ax[1] = plt.subplot(1,2)   #(gs[:-1, -1], projection='polar')
    #ax[1].projection='polar'
    #ax[1].set_theta_direction(-1)
    # Make sure North points to top of page
    #ax[1].set_theta_offset(90*math.pi /180)
    #ax[1].bar(theta, radii, width=nwidth, bottom=0.0)
    #ax[1].set_title('Met conditions')
    # ax3 = plt.subplot(gs[-1, -1])
#     ax3.set_frame_on(False)
#     ax3.axes.get_xaxis().set_visible(False)
#     ax3.axes.get_yaxis().set_visible(False)
#     ax3.text(0.1, 2.3, r"u = %d $m s^{-1}$"%u, fontsize=10)
#     ax3.text(0.1, 2.2, r" ", fontsize=10)
#     ax3.text(0.1, 2.1, r"wdir = %i degrees"%wdir, fontsize=10)
#     ax3.text(0.1, 2.0, r" ", fontsize=10)
#     ax3.text(0.1, 1.9, r"H = %d $Wm^{-2}$"%H, fontsize=10)
#     ax3.text(0.1, 1.8, r" ", fontsize=10)
#     ax3.text(0.1, 1.7, r"sbl = %d m"%sbl, fontsize=10)
#     ax3.text(0.1, 1.6, r" ", fontsize=10)
#     ax3.text(0.1, 1.5, r"MOLength = %d m"%MOLength, fontsize=10)
#     ax3.text(0.1, 1.4, r" ", fontsize=10)
#     # format returns a str
#     ax3.text(0.1, 1.3, r"s1 = %d $\mu g \ m^{-3}$"%sites[0], fontsize=10,color='red')
#     ax3.text(0.1, 1.2, r" ", fontsize=10)
#     ax3.text(0.1, 1.1, r"s2 = %d $\mu g \ m^{-3}$"%sites[1], fontsize=10,color='green')
#     ax3.text(0.1, 1.0, r" ", fontsize=10)
#     ax3.text(0.1, 0.9, r"s3 = %d $\mu g \ m^{-3}$"%sites[2], fontsize=10,color='blue')
#     ax3.text(0.1, 0.8, r" ", fontsize=10)
#     ax3.text(0.1, 0.7, r"s4 = %d $\mu g \ m^{-3}$"%sites[3], fontsize=10,color='black')
#     ax3.text(0.1, 0.5, r" ", fontsize=10)
#     ax3.text(0.1, 0.4, r"-------------------------- ", fontsize=9)
#     ax3.text(0.1, 0.3, r"Model: RLine V1.2", fontsize=10,color='blue')
#     ax3.text(0.1, 0.2, r"Emission height = 1 m", fontsize=10)
#     ax3.text(0.1, 0.1, r"Roadway ---", fontsize=10)
    
   
    