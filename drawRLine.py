#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 15:07:55 2017

@author: jbm
"""

# drawRLine.py
# 1. Draws contours from RLine source model

<<<<<<< HEAD
# Version 0.14
# Date 17 March 2017
# Author: jbm
# Latest: 17:15 1/12/20
=======
# Version 0.1
# Date 17 March 2017
# Author: jbm
# Latest: 15:19 1/04/17
>>>>>>> cd52a171d0847415a590d9be1528a28c3405e7fc
#
import csv
import numpy as np
import matplotlib.pyplot as plt  
<<<<<<< HEAD
# from matplotlib.mlab import griddata # deprecated since 2018
from scipy.interpolate import griddata
# https://www.reddit.com/r/Python/comments/87lbao/matplotlib_griddata_deprecation_help/
import matplotlib.gridspec as gridspec
import math
import sys
import pandas as pd


sites = []
=======
from matplotlib.mlab import griddata
import matplotlib.gridspec as gridspec
import math
import sys

X1 = []
Y1 = []
Z1 = []
s1z = s2z = s3z = s4z = 0
xcoords = [-100,-75,-50,-40,-30,-20,-10,10,20,30,40,50,75,100]
ycoords = [-100,-75,-50,-40,-30,-20,-10,10,20,30,40,50,75,100]
xsites = [20,20]
ysites = [20,20]
fnames = [' Year', ' Julian_Day', ' Hour', ' X-Coordinate', ' Y-Coordinate', ' Z-Coordinate', ' C_G1', ' C_G2']
fnamesm = ['Year','Month','Day','Jday','Hour','Hs','u*','w*','VPTG','CBL','SBL','L','z0','B','alb','u','dir','zref	T','ztemp','s1','s2','s3','s4','s5','s6']
data = []
datam = []
sites=[]
>>>>>>> cd52a171d0847415a590d9be1528a28c3405e7fc
max = min = 0
gs = gridspec.GridSpec(4, 4)
gs.update(left=0.10, right=0.95, hspace=0.05)
hourly_stab = ['stable','weakly stable','weakly convective','convective']

<<<<<<< HEAD

def plot_line_source(xx, yy, zz, hour):
    """Docstring"""
    # define grid
    xi = np.linspace(-100., 100., 100)
    yi = np.linspace(-100., 100., 100)
    print(xx.shape, yy.shape, zz.shape)
    print(len(xi), len(xx), len(zz))
    X,Y= np.meshgrid(xi,yi)
    #Z = griddata((x, y), z, (X, Y),method='nearest')
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
=======
def extract_hourly_data():
    # get data into format suitable for contouring
    # Will do this by HOUR into separate files.
    old_hour = 1
    X1 = []
    Y1 = []
    Z1 = []
    s1z = s2z = s3z = s4z = 0
    for row in data:
        if old_hour == int(float(row[' Hour'])):
            hour = int(float(row[' Hour']))
            #print('hour = ',old_hour,'row[Hour] = ',float(row[' Hour']))
            for x in xcoords:
                for y in ycoords:
                    if ((y == int(float(row[' Y-Coordinate']))) and (x == int(float(row[' X-Coordinate'])))):
                        z = float(row[' C_G1'])/1e3 + float(row[' C_G2'])/1e3
                        X1.append(x)
                        Y1.append(y)
                        Z1.append(z)
                        if (x == 20 and y == 20):
                            s1z = z
                        if (x == 20 and y == -20):
                            s2z = z
                        if (x == -20 and y == -20):
                            s3z = z
                        if (x == -20 and y == 20):
                            s4z = z
        else:
            hour = old_hour
            sites=[s1z,s2z,s3z,s4z]
            plot_line_source(X1,Y1,Z1,hour)
            plot_met_data(datam,sites,hour)
            old_hour = old_hour + 1
            X1 = []
            Y1 = []
            Z1 = []
    # make sure final hour is done - must be a neater way of doing this though!
    if hour == 4:
        sites=[s1z,s2z,s3z,s4z]
        plot_line_source(X1,Y1,Z1,hour)
        plot_met_data(datam,sites,hour)

def plot_line_source(X1,Y1,Z1,hour):
    # define grid.                
    xi = np.linspace(-100., 100., 100)
    yi = np.linspace(-100., 100., 100)
    # grid the data.
    # need to do this differently if Windoze or macOS
    if platform == "macOS" or "OS X" or "linux" or "linux2":
        zi = griddata(X1, Y1, Z1, xi, yi, interp='linear')
    else:
        zi = griddata(X1, Y1, Z1, xi, yi)
    # plot the roadways running N-S and E-W
    ax1 = plt.subplot(gs[:, :-1])
    ax1.plot([5,5],[-100,100],color='k', linestyle='--', linewidth=1)
    ax1.plot([-5,-5],[-100,100],color='k', linestyle='--', linewidth=1)
    ax1.plot([-100,100],[-5,-5],color='k', linestyle='--', linewidth=1)
    ax1.plot([-100,100],[5,5],color='k', linestyle='--', linewidth=1)
    ax1.set_ylabel('distance (m)',fontsize=11)
    ax1.set_xlabel('distance (m)',fontsize=11)
    circ1 = plt.Circle((20,20), 1.5, color='red')
    ax1.add_artist(circ1)
    circ2 = plt.Circle((20,-20), 1.5, color='green')
    ax1.add_artist(circ2)
    circ3 = plt.Circle((-20,-20), 1.5, color='blue')
    ax1.add_artist(circ3)
    circ4 = plt.Circle((-20,20), 1.5, color='black')
    ax1.add_artist(circ4)

    # Contours etc explained here: 
    #  http://matplotlib.org/examples/pylab_examples/contourf_demo.html
    levels = np.arange(min,max,(max-min)/20)
    # contour the gridded data, plotting dots at the nonuniform data points.
    ax1.contour(xi, yi, zi, levels, linewidths=0.5, colors='w')
    
    CS1 = ax1.contourf(xi, yi, zi, levels,
                  cmap=plt.cm.jet,
                  vmax=abs(zi).max(), 
                  vmin=-abs(zi).max()
                  )
    # Make a colorbar for the ContourSet returned by the contourf call.
    cbar = plt.colorbar(CS1)#,orientation = 'horizontal')
>>>>>>> cd52a171d0847415a590d9be1528a28c3405e7fc
    cbar.ax.set_title('$ng m^{-3}$',fontsize=9)

    ax1.set_xlim(-100, 100)
    ax1.set_ylim(-100, 100)
    ax1.set_title('PM10 Ground-Level Concentration \n (%s)'%hourly_stab[hour-1], fontsize=11, color='blue')
<<<<<<< HEAD
    plt.show()


def plot_met_data(datam, sites):
    """Docstring"""
    hour = datam['Hour']
    u = float(datam['u'])
    wdir = int(float(datam['dir']))
    MOLength = int(float(datam['L']))
    H = int(float(datam['Hs']))
    sbl = int(float(datam['SBL']))
    # print u,wdir,MOLength,H,sbl
    # convert wdir to radians
    wdirr = wdir * math.pi /180
    # Compute pie slices
    # from MatplotlIb web page of examples
    theta = wdirr
    radii = 8
    width = np.pi / 16
    # go clockwise as in a compass
    ax2 = plt.subplot(gs[:-1, -1], projection='polar')
    ax2.set_theta_direction(-1)
    # Make sure North points to top of page
    ax2.set_theta_offset(90*math.pi /180)
    ax2.bar(theta, radii, width=width, bottom=0.0)
    ax2.set_title('Met conditions')
    ax3 = plt.subplot(gs[-1, -1])
    ax3.set_frame_on(False)
    ax3.axes.get_xaxis().set_visible(False)
    ax3.axes.get_yaxis().set_visible(False)
    ax3.text(0.1, 1.5, r'u = %d $m s^{-1}$'%u, fontsize=9)
    ax3.text(0.1, 1.4, r'wdir = %i degrees'%wdir, fontsize=9)
    ax3.text(0.1, 1.3, r'H = %d $Wm^{-2}$'%H, fontsize=9)
    ax3.text(0.1, 1.2, r'sbl = %d m'%sbl, fontsize=9)
    ax3.text(0.1, 1.1, r'MOLength = %d m'%MOLength, fontsize=9)
    ax3.text(0.1, 1.0, r' ', fontsize=10)
    # format returns a str
    ax3.text(0.1, 0.9, r's1 = %s $ng m^{-3}$' % '{0:.2f}'.format(sites[0]), fontsize=9,color='red')
    ax3.text(0.1, 0.8, r's2 = %s $ng m^{-3}$' % '{0:.2f}'.format(sites[1]), fontsize=9,color='green')
    ax3.text(0.1, 0.7, r's3 = %s $ng m^{-3}$' % '{0:.2f}'.format(sites[2]), fontsize=9,color='blue')
    ax3.text(0.1, 0.6, r's4 = %s $ng m^{-3}$' % '{0:.2f}'.format(sites[3]), fontsize=9,color='black')
    ax3.text(0.1, 0.5, r' ', fontsize=10)
    ax3.text(0.1, 0.4, r'-------------------------- ', fontsize=9)
    ax3.text(0.1, 0.3, r'Model: RLine V1.2', fontsize=10,color='blue')
    ax3.text(0.1, 0.2, r'Emission height = 1 m', fontsize=10)
    ax3.text(0.1, 0.1, r'Roadway ---', fontsize=10)

    fig = plt.gcf()
    fig.facecolor='white'
    plt.subplots_adjust(hspace=0.5, wspace=0.2)
    # fig.set_size_inches(10, 8)
    fig.subplots_adjust(top=0.85, left=0.1, right=0.95, bottom=0.1)
    fig.savefig('rline_%d.png'%hour, dpi=100)

    plt.show()


def find_maxmin():
    """Docstring"""
=======
    #plt.show()
    
def plot_met_data(datam,sites,hour):
    for row in datam:
        if (hour == int(float(row['Hour']))):
            u = float(row['u'])
            wdir = int(float(row['dir']))
            MOLength = int(float(row['L']))
            H = int(float(row['Hs']))
            sbl = int(float(row['SBL']))
            #print u,wdir,MOLength,H,sbl
            # convert wdir to radians
            wdirr = wdir * math.pi /180
            # Compute pie slices
            # from MatplotlIb web page of examples
            theta = wdirr
            radii = 8
            width = np.pi / 16
            # go clockwise as in a compass
            ax2 = plt.subplot(gs[:-1, -1], projection='polar')
            ax2.set_theta_direction(-1)
            # Make sure North points to top of page
            ax2.set_theta_offset(90*math.pi /180)
            ax2.bar(theta, radii, width=width, bottom=0.0)
            ax2.set_title('Met conditions')
            ax3 = plt.subplot(gs[-1, -1])
            ax3.set_frame_on(False)
            ax3.axes.get_xaxis().set_visible(False)
            ax3.axes.get_yaxis().set_visible(False)
            ax3.text(0.1,1.5,r'u = %d $m s^{-1}$'%u, fontsize=9)
            ax3.text(0.1,1.4,r'wdir = %i degrees'%wdir, fontsize=9)
            ax3.text(0.1,1.3,r'H = %d $Wm^{-2}$'%H, fontsize=9)
            ax3.text(0.1,1.2,r'sbl = %d m'%sbl, fontsize=9)
            ax3.text(0.1,1.1,r'MOLength = %d m'%MOLength, fontsize=9)
            ax3.text(0.1,1.0,r' ', fontsize=10)
            # format returns a str
            ax3.text(0.1,0.9,r's1 = %s $ng m^{-3}$' % '{0:.2f}'.format(sites[0]), fontsize=9,color='red')
            ax3.text(0.1,0.8,r's2 = %s $ng m^{-3}$' % '{0:.2f}'.format(sites[1]), fontsize=9,color='green')
            ax3.text(0.1,0.7,r's3 = %s $ng m^{-3}$' % '{0:.2f}'.format(sites[2]), fontsize=9,color='blue')
            ax3.text(0.1,0.6,r's4 = %s $ng m^{-3}$' % '{0:.2f}'.format(sites[3]), fontsize=9,color='black')
            ax3.text(0.1,0.5,r' ', fontsize=10)
            ax3.text(0.1,0.4,r'-------------------------- ', fontsize=9)
            ax3.text(0.1,0.3,r'Model: RLine V1.2', fontsize=10,color='blue')
            ax3.text(0.1,0.2,r'Emission height = 1 m', fontsize=10)
            ax3.text(0.1,0.1,r'Roadway ---', fontsize=10)

            fig = plt.gcf()
            fig.facecolor='white'
            plt.subplots_adjust(hspace=0.5, wspace=0.2)
            #fig.set_size_inches(10, 8)
            fig.subplots_adjust(top=0.85,left=0.1, right=0.95,bottom=0.1)
            fig.savefig('rline_%d.png'%hour, dpi=100)

            plt.show()
            
def find_maxmin():
>>>>>>> cd52a171d0847415a590d9be1528a28c3405e7fc
    max = min = 0.0
    for row in data:
        temp = float(row[' C_G1'])/1e3 + float(row[' C_G2'])/1e3  # ng m-3
        if row == 1:
<<<<<<< HEAD
            min = temp
        if temp > max:
            max = temp
        if temp < min:
            min = temp
    return max, min


def get_platform():
    """Docstring"""
=======
            min =  temp
        if temp>max:
            max = temp
        if temp<min:
            min = temp
    return max,min

def get_platform():
>>>>>>> cd52a171d0847415a590d9be1528a28c3405e7fc
    platforms = {
        'linux1' : 'Linux',
        'linux2' : 'Linux',
        'darwin' : 'OS X',
        'win32' : 'Windows'
    }
    if sys.platform not in platforms:
        return sys.platform
    
    return platforms[sys.platform]
<<<<<<< HEAD

# ----------------------------------------------------------------------


=======
#----------------------------------------------------------------------
>>>>>>> cd52a171d0847415a590d9be1528a28c3405e7fc
if __name__ == "__main__":
    # which OS is this running on?
    platform = get_platform()
    """
    Read the csv file
    """
<<<<<<< HEAD
    # inpath = '/Users/jbm/Documents/python/RLine/'
    inpath = ""
    infilename = 'Output_Example_Numerical_09-12.csv'
    infilename2 = 'Met_Example.csv'   
    # use Pandas to read in emissions data
    dfe=pd.read_csv("Output_Example_Numerical_09-12.csv", header=10, skipinitialspace=True)
    # Split into hourly dataframes for graphing
    # https://stackoverflow.com/questions/54046707/pandas-split-one-dataframe-into-multiple-dataframes
    for h in dfe['Hour'].unique():
        temp = 'dfe_{}'.format(h)    
        vars()[temp] = dfe[dfe['Hour']==h]
    #print(dfe_1.head(5))
    
    # extract the x, y, z-values to 1-D arrays for plotting
    xx = dfe_1['X-Coordinate'].to_numpy()
    yy = dfe_1['Y-Coordinate'].to_numpy()
    zz = (dfe_1['C_G1']+dfe_1['C_G2']).to_numpy()
    
    max = (dfe_1['C_G1']+dfe_1['C_G2']).max()
    min = (dfe_1['C_G1']+dfe_1['C_G2']).min()
    #print(min,max)
    # get the concentration values at the 4 receptor sites
    dfs1 = dfe_1[((dfe_1['X-Coordinate'] == 20.000) & (dfe_1['Y-Coordinate'] == 20.000))]
    dfs2 = dfe_1[((dfe_1['X-Coordinate'] == 20.000) & (dfe_1['Y-Coordinate'] == -20.000))]
    dfs3 = dfe_1[((dfe_1['X-Coordinate'] == -20.000) & (dfe_1['Y-Coordinate'] == -20.000))]
    dfs4 = dfe_1[((dfe_1['X-Coordinate'] == -20.000) & (dfe_1['Y-Coordinate'] == 20.000))]
    #print(dfs1)
    s1z = dfs1.iloc[0]['C_G1']+dfs1.iloc[0]['C_G2']
    s2z = dfs2.iloc[0]['C_G1']+dfs2.iloc[0]['C_G2']
    s3z = dfs3.iloc[0]['C_G1']+dfs3.iloc[0]['C_G2']
    s4z = dfs4.iloc[0]['C_G1']+dfs4.iloc[0]['C_G2']
    
    #print(s1z)
    sites = [s1z, s2z, s3z, s4z]
    # pass to plotting routine
    plot_line_source(xx, yy, zz, 1)
    
    # use Pandas to read in meteorology data
    dfm=pd.read_csv("Met_Example.csv", skip_blank_lines=True, skipinitialspace=True)
    print(dfm.head(4))
    for h in dfm['Hour'].unique():
        temp = 'dfm_{}'.format(h)    
        vars()[temp] = dfm[dfm['Hour']==h]
    plot_met_data(dfm_1, sites)
=======
    #inpath = '/Users/jbm/Documents/python/RLine/'
    inpath = ""
    infilename = 'Output_Example_Numerical_09-12.csv'
    infilename2 = 'Met_Example.csv'
    
    # read emissions file
    csvReader1=csv.DictReader(open(infilename,'rU'))
    rfieldnames = csvReader1.fieldnames
    for row in csvReader1:
        data.append(row)
    # Find max,min so we can set appropriate contour intervals
    max,min = find_maxmin()
    
    # read meteorology file    
    csvReader2=csv.DictReader(open(infilename2, 'rU'))
    rfieldnames2 = csvReader2.fieldnames
    #print rfieldnames2
    for row in csvReader2:
        datam.append(row)
    
    #print(datam)    
    extract_hourly_data()
>>>>>>> cd52a171d0847415a590d9be1528a28c3405e7fc

            

    