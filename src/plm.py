import numpy as np
import matplotlib.pyplot as plt
import math

def plm(gs, datam, sites):
    """Plot meteorological data"""
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
    ax3.text(0.1, 2.3, r"u = %d $m s^{-1}$"%u, fontsize=10)
    ax3.text(0.1, 2.2, r" ", fontsize=10)
    ax3.text(0.1, 2.1, r"wdir = %i degrees"%wdir, fontsize=10)
    ax3.text(0.1, 2.0, r" ", fontsize=10)
    ax3.text(0.1, 1.9, r"H = %d $Wm^{-2}$"%H, fontsize=10)
    ax3.text(0.1, 1.8, r" ", fontsize=10)
    ax3.text(0.1, 1.7, r"sbl = %d m"%sbl, fontsize=10)
    ax3.text(0.1, 1.6, r" ", fontsize=10)
    ax3.text(0.1, 1.5, r"MOLength = %d m"%MOLength, fontsize=10)
    ax3.text(0.1, 1.4, r" ", fontsize=10)
    # format returns a str
    ax3.text(0.1, 1.3, r"s1 = %d $\mu g \ m^{-3}$"%sites[0], fontsize=10,color='red')
    ax3.text(0.1, 1.2, r" ", fontsize=10)
    ax3.text(0.1, 1.1, r"s2 = %d $\mu g \ m^{-3}$"%sites[1], fontsize=10,color='green')
    ax3.text(0.1, 1.0, r" ", fontsize=10)
    ax3.text(0.1, 0.9, r"s3 = %d $\mu g \ m^{-3}$"%sites[2], fontsize=10,color='blue')
    ax3.text(0.1, 0.8, r" ", fontsize=10)
    ax3.text(0.1, 0.7, r"s4 = %d $\mu g \ m^{-3}$"%sites[3], fontsize=10,color='black')
    ax3.text(0.1, 0.5, r" ", fontsize=10)
    ax3.text(0.1, 0.4, r"-------------------------- ", fontsize=9)
    ax3.text(0.1, 0.3, r"Model: RLine V1.2", fontsize=10,color='blue')
    ax3.text(0.1, 0.2, r"Emission height = 1 m", fontsize=10)
    ax3.text(0.1, 0.1, r"Roadway ---", fontsize=10)

    fig = plt.gcf()
    fig.facecolor='white'
    plt.subplots_adjust(hspace=0.5, wspace=0.2)
    # fig.set_size_inches(10, 8)
    fig.subplots_adjust(top=0.85, left=0.1, right=0.95, bottom=0.1)
    #fig.savefig('rline_%d.png'%hour, dpi=100)

    plt.show()