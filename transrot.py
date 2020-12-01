def transrot():

# 
#      This program traslates and rotates the cordinates so that x-axis lies 
#            along the wind
#      X0=Xsource(1), Y0=Ysource(1) are the origins of the coordinate system
#      Xs_tran, Ys_tran are the translated coordinates of the source
#      Xs_rot, Ys_rot are the translated coordinates of the source
#      Xr_tran, Yr_tran are the translated coordinates of the receptor
#      Xr_rot, Yr_rot are the translated coordinates of the receptor
# 
#      In addition, this subroutine allows the user to specify sources based on a 
#      centerline and the distance from the centerline (dCL).. ie an offset
# 
# 

# Translate line source origin
    X0=Source(1)%Xsb    
    Y0=Source(1)%Ysb

# Translate source and receptor coordinates and then rotate them along wind direction
 
    for index in range (1, Number_Sources):  
        # Intialize variables used
        dCL=Source(index)%dCL
  
        # Move initial user coordinate system so the origin is 
        # at the begining of first source             
        Xsb_tran   = Source(index)%Xsb-X0
        Ysb_tran   = Source(index)%Ysb-Y0
        Xse_tran   = Source(index)%Xse-X0
        Yse_tran   = Source(index)%Yse-Y0
        theta_line = atan2(Yse_tran-Ysb_tran,Xse_tran-Xsb_tran)

        if (sin(theta_line) == 0):
          dCL = -dCL # this is needed for due east lines; it defines + as 
                     # north for dCL in following equations
        

        # Needed to find the location of the line that is not within a depression,
        # but is specified in source file with the centerline and distance 
        # from the centerline
        if (dCL != 0.0 && Source(index)%Depth == 0.0): 
          Xse_tran = Xse_tran+dCL*sin(theta_line)*sign(DBLE(1.0),sin(theta_line))
          Yse_tran = Yse_tran-dCL*cos(theta_line)*sign(DBLE(1.0),sin(theta_line))
          Xsb_tran = Xsb_tran+dCL*sin(theta_line)*sign(DBLE(1.0),sin(theta_line))
          Ysb_tran = Ysb_tran-dCL*cos(theta_line)*sign(DBLE(1.0),sin(theta_line))
    
        Xsb_rot(index) =  Xsb_tran*cos(thetaw)+Ysb_tran*sin(thetaw)    
        Ysb_rot(index) = -Xsb_tran*sin(thetaw)+Ysb_tran*cos(thetaw)
        Xse_rot(index) =  Xse_tran*cos(thetaw)+Yse_tran*sin(thetaw)
        Yse_rot(index) = -Xse_tran*sin(thetaw)+Yse_tran*cos(thetaw)  

    for index in range (1, Number_Receptors):
        Xr_tran         =  Receptor(index)%Xr-X0
        Yr_tran         =  Receptor(index)%Yr-Y0
        Xrcp_rot(index) =  Xr_tran*cos(thetaw)+Yr_tran*sin(thetaw)
        Yrcp_rot(index) = -Xr_tran*sin(thetaw)+Yr_tran*cos(thetaw)
